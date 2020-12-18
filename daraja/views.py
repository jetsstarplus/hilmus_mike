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

 
#This is the form submission view
def lipa_na_mpesa_view(request):
    if request.is_ajax():
        phone_number = request.POST.get("phone", None)
        amount = request.POST.get("amount", None)
        
        
        submitted_phone = "254"+str(phone_number)
        
        data = {
            
        }
        
        if(amount == None):
            data = {
                'message': "No amount entered"
            }
            
        else:
            # desiralizing the response
            message = json.loads(lipa_na_mpesa(int(submitted_phone), amount))
            
            # checking if the request was successful from mpesa
            if message["ResponseCode"] =='0':
                data = {
                    'message':"OK",
                    'text':message['CustomerMessage'],
                }
                
            else:
                data={
                    'message':message['errorMessage']
                }
            print(message)
            
           
        # try:
        #     Contact.objects.create(email=email, full_name = name, subject=subject, content=message)
        #     data = {
        #         'message': "OK"
        #     }
            
        # except:
        #     data = {
        #         'message': "There was an error in our side"
        #     }
        
        # finally:              
        return JsonResponse(data) 

def lipa_mpesa(request):
    template_name="lipa.html"
    error=None
    message=None
    state=False
    user=request.user
    services= Service.objects.all()
    
    
    if request.method=='POST' and user:
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
                error=" Enter the correct phone number"                
                messages.add_message(request, messages.WARNING,  "Enter the correct phone number")
                state=False
        else:
            if phone==13:
                phone_number== phone_number[4:phone]
                print(phone_number)
                state=True
            else:
                error=" Enter the correct phone number"
                messages.add_message(request, messages.WARNING,  "Enter the correct phone number")
                state=False
        if state:  
            try:      
                phone_number=int('254'+phone_number) 
            except:
                error="Phone number was not correct"                 
                messages.add_message(request, messages.WARNING,  "Enter the correct phone number")
            
            test = lipa_na_mpesa(phone_number, str(selected_service.pricing), str(user.id), str(selected_service.title))
            if test.status_code ==200:                        
                message = " You can now enter the pin in your phone to finish the payment"
                messages.add_message(request, messages.SUCCESS,  " You can now enter the pin in your phone to finish the payment")                
                r_json=test.json()
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
            else:
                error="Enter a Valid Phone Number"
                messages.add_message(request, messages.WARNING,  "Enter the correct phone number")
                
       
            # print(jfile)
            # new_data=ast.literal_eval(test)
            # print(new_data)
            # # result = json.loads(jfile)
            # print(result)
           
            # print(merchant)
        
    context={
        'error':error,
        'message':message,
        'services':services
    }
    return render(request, template_name=template_name, context=context)


def paybill(request, id):
    template_name="paybill.html"
    error=None
    message=None
    user=request.user
    id=None
    
    service = Service.objects.get(pk=id)
    account='{}+{}'.format(user.id,service.id)
    # account='959090+10'
    string=base64.b64encode(account.encode('utf-8')).decode("utf-8") 
    paybill=env('PAYBILL')
    # print(string)
    # base=base64.b64decode(string.encode('ascii')).decode('ascii')
    # print(base)
    if request.method=='POST' and user:
        id=service.id
        trans = str(request.POST.get("trans", None))
        # messages.add_message(request, messages.INFO, f"Hello {username}")
        transaction=C2BPaymentModel.objects.filter(TransID=trans)        
        if transaction:
            if transaction.Status:
                error="The transaction had already been confirmed"                   
                messages.add_message(request, messages.WARNING,  "The transaction had already been confirmed")
            else:
                transaction.update(Status=True)
                user.is_payed= True
                user.save(update_fields=['is_payed'])
                message = " You Can Now Proceed with uploading your content"
                messages.add_message(request, messages.SUCCESS,  " Confirmation Successful")                 
                
        else:
            error="Transaction ID Not Found!"
            messages.add_message(request, messages.WARNING,  "Transaction ID Not Found!")

        
    context={
        'error':error,
        'message':message,
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
