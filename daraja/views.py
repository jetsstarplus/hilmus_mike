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
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin
from django.core.mail import send_mail
from django.conf import settings

# from django.contrib.auth.models import User
from rest_framework import viewsets
from . import serializers
from mpesa.daraja import lipa_na_mpesa
from mike_admin.models import Service
from .models import Initiate, C2BPaymentModel, Paypal

# #viewsets define the behavior of the view
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializers

 
def lipa_mpesa(request):
    """This method confirms the the mpesa online transaction and stores initiates the online mpesa"""
    template_name="lipa.html"
    error=None
    message=None
    state=False
    user=request.user
    services= Service.objects.all()
    
    """The data is submitted with ajax"""
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
                    
                    """Storing the started transaction for future confirmation with the checkout and merchant Id"""
                    initiated = Initiate(
                        MerchantRequestID=merchant, 
                        CheckoutRequestID=checkout, 
                        ResultCode=code, 
                        ResultDescription=description, 
                        user=user, 
                        service=selected_service,
                        mode='mpesa-stk-push')
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
    """An admin method for taking the mpesa transaction from c2b and confirm with the ones stored
    in the confirmation endpoint
    The method also checks if the transaction has already been confirmed for more security reasons"""
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
                initiated = Initiate(
                        CheckoutRequestID=transaction.BillRefNumber,
                        ResultCode=0, 
                        ResultDescription=transaction.InvoiceNumber, 
                        user=user, 
                        service=payed_service,
                        mode='mpesa-paybill')
                initiated.save()
                message = " You Can Now Proceed with uploading your content!"  
                data={
                    'message':message,
                    'status':200
                } 
                
                """Sending emails to the user and the responsible personels to take actions on them"""
                send_mail(                                
                    'Mpesa Transaction Completed',
                    'Your Mpesa Transaction to Mike Creatives towards payment for Ksh {} of service {} has been successfully received.'.format(transaction.TransAmount, initiated.service),
                    'Transaction Complete <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                    [request.user.email],
                    fail_silently=True,
                )
                
                send_mail(                                
                    'Mpesa Transaction Completed',
                    'Mpesa Transaction to Mike Creatives for reference {} towards payment for USD {} of service {} has been successfully received.'.format(transaction.BillRefNumber, transaction.TransAmount, initiated.service),
                    'Transaction Complete <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                    ['mikecreatives254@gmail.com', 'w.mwangi95@gmail.com', 'edwinkyalo@hotmail.com'],
                    fail_silently=True,
                )             
                
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
    """A method that allows a user to select first a service before paying with mpesa"""
    template_name="select.html"
    error=None
    message=None
    user=request.user
    services= Service.objects.exclude(pricing=0).all()
     
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

@xframe_options_sameorigin
def paypal(request):
    """A method that is used to get the transaction after a successfull paypall transaction"""
    
    # print(json.load(request)['name'])
    if request.is_ajax() and request.method=='POST' and request.user:
        # getting the data from the ajax json
        data=json.load(request)['data']
        
        name=data['name']
        amount=data['amount']
        user=request.user
        id= data['id']
        status=data['status']
        currency=data['currency']
        service=data['service']
        
        if request.user.get_full_name():
            user_name=request.user.get_full_name()
        else:
            user_name=request.user.username
        
        service=Service.objects.get(pk=service)
        service_amount=round((float(service.pricing)/109), 2)
        print(service_amount)
        if service_amount == float(amount):
            transaction=Paypal(user=user, name=name, amount=amount, currency=currency, paypal_id=id, service=service)
            initiated = Initiate(
                        CheckoutRequestID=id,
                        ResultCode=0, 
                        ResultDescription=currency, 
                        user=user, 
                        service=service,
                        mode='paypal')
            initiated.save()
            # print(transaction)
            if status=='COMPLETED':  
                              
                transaction.save()
                user.is_payed=True
                user.save(update_fields=['is_payed'])
                send_mail(                                
                    'Paypal Transaction Completed',
                    'Your Paypal Transaction to Mike Creatives towards payment for USD {} of service {} has been successfully received.'.format(amount, service),
                    'Transaction Complete <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                    [request.user.email],
                    fail_silently=True,
                )
                
                send_mail(                                
                    'Paypal Transaction Completed',
                    'Paypal Transaction to Mike Creatives for user {} towards payment for USD {} of service {} has been successfully received.'.format(user_name, amount, service),
                    'Transaction Complete <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                    ['mikecreatives254@gmail.com', 'w.mwangi95@gmail.com', 'edwinkyalo@hotmail.com'],
                    fail_silently=True,
                )
                data={
                    'message':'Payment Successful!',
                    'status':200
                }
            else:
                data={
                    'message':'Payment Failed!',
                    'status':400
                }
        else:
            data={
                'message':'Payment Error! The Amount Was Not Correct',
                'status':403,
            }
        return JsonResponse(data)
        
