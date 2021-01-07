import ast
import json
import requests
import base64
import environ

env = environ.Env(
    PAYBILL=(str, '601393')
)


from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
# from django.contrib.auth.models import User
from rest_framework import viewsets
from . import serializers
from mpesa.daraja import lipa_na_mpesa
from mike_admin.models import Service
from .models import Initiate, C2BPaymentModel

# #viewsets define the behavior of the view
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializers

 
def lipa_mpesa(request):
    template_name="lipa.html"
    error=None
    message=None
    state=False
    user=request.user
    services= Service.objects.all()
    
    
    if request.is_ajax() and user:
        phone_number = str(request.POST.get("phone", None))
        service = request.POST.get("amount", None)
        # messages.add_message(request, messages.INFO, f"Hello {username}")

        # print(service)
        
        selected_service = Service.objects.get(id=service)
        # print(selected_service)
                                
        phone_number=phone_number.strip()
        phone = len(phone_number)
        if phone_number.isdigit():
            if phone == 10:
                phone_number= phone_number[1:phone]
                state=True
            elif phone==12:
                phone_number= phone_number[3:phone]
                # print(phone_number)
                state=True
            elif phone==9:
                phone_number= phone_number
                state=True
            else:
                message=" Enter the correct phone number!"         
                state=False
        else:
            if phone==13:
                phone_number=phone_number.split('+')
                phone_number = phone_number[1][3:phone]
                # print(phone_number)
                state=True
            else:
                message=" Enter the correct phone number!"
                state=False
        if state:  
            try:      
                phone_number=int('254'+phone_number) 
            except:
                message="Your Phone number was not correct!"                 
                messages.add_message(request, messages.WARNING,  error)
            try:
                test = lipa_na_mpesa(phone_number, str(selected_service.pricing), str(user.id), str(selected_service.title))
                if test.status_code ==200:                        
                    message = " You can now enter the pin in your phone to finish the payment!"
                    merchant= r_json['MerchantRequestID']
                    code=r_json['ResponseCode']
                    description= r_json['ResponseDescription']
                    checkout= r_json['CheckoutRequestID']
                    
                    initiated = Initiate(
                        MerchantRequestID=merchant, 
                        CheckoutRequestID=checkout, 
                        ResultCode=code, 
                        ResultDescription=description, 
                        user=user, 
                        service=selected_service)
                    initiated.save()
                    # print(initiated.user)
                    # print(r_json)
                    data = {
                    'message':message,
                    'status':200,
                } 
                else:
                    if error:
                        error=error
                    else:
                        error="Transaction Initiation Failed!"
                    print(error)
                    data = {
                        'message':error,
                        'status':200,
                    } 
            except: 
                message="There Was A Connection Error!"
                data = {
                    'message':message,
                    'status':500,
                }     
            
            return JsonResponse(data)
       
            # print(jfile)
            # new_data=ast.literal_eval(test)
            # print(new_data)
            # # result = json.loads(jfile)
            # print(result)
           
            # print(merchant)
        
    context={
        'error':error,
        'services':services
    }
    return render(request, template_name=template_name, context=context)


def paybill(request, id):
    template_name="paybill.html"
    message=None
    user=request.user
      
    service = Service.objects.get(pk=id)
    account='{}+{}'.format(user.id,service.id)
    # account='959090+10'
    string=base64.b64encode(account.encode('utf-8')).decode("utf-8") 
    paybill=env('PAYBILL')
    
    # print(string)
    # base=base64.b64decode(string.encode('ascii')).decode('ascii')
    # print(base)
    if request.is_ajax() and user:
        id=service.id
        trans = str(request.POST.get("trans", None))
        # messages.add_message(request, messages.INFO, f"Hello {username}")
        transaction=C2BPaymentModel.objects.filter(TransID=trans)        
        if transaction:
            if transaction.Status:
                message="The transaction ID had already been confirmed!"                   
                data={
                    'message':message,
                    'status':403
                }
            else:
                payed_service=base64.b64decode(transaction.BillRefNumber.encode('ascii')).decode('ascii')
                payed_service=payed_service.split('+')
                # print(payed_service)
                payed_service=Service.objects.filter(pk=payed_service[1])
                transaction.update(Status=True, user=user, service=payed_service)
                user.is_payed= True
                user.save(update_fields=['is_payed'])
                message = " You Can Now Proceed with uploading your content!"  
                data={
                    'message':message,
                    'status':200
                }              
                
        else:
            data={
                'message':'Transaction ID Not Found!',
                'status':404
            }
        return JsonResponse(data)
        
    context={
        'service':service,
        'account':string,
        'paybill':paybill,
        'id':id,
    }
    return render(request, template_name=template_name, context=context)


def select_service(request):
    template_name="select.html"
    error=None
    message=None
    user=request.user
    services= Service.objects.all()
        
    if request.method=='POST' and user:          
        service = request.POST.get("amount", None)   
        selected_service = Service.objects.get(id=service)
        # print(selected_service)
        return redirect('home:paybill',id = selected_service.id)
        
    context={
        'error':error,
        'message':message,
        'services':services
    }
    return render(request, template_name=template_name, context=context)
