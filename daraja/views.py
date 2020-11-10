from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from django.contrib.auth.models import User
from rest_framework import viewsets
from . import serializers
import requests
from mpesa.daraja import lipa_na_mpesa
import json
from mike_admin.models import Service

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
        
        selected_service = Service.objects.filter(id=service)
                                
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
                state=False
        else:
            if phone==13:
                phone_number== phone_number[4:phone]
                print(phone_number)
                state=True
            else:
                error=" Enter the correct phone number"
                state=False
        if state:  
            try:      
                phone_number=int('254'+phone_number) 
            except:
                error="Phone number was not correct"           
            try:
                test = lipa_na_mpesa(phone_number, selected_service.pricing, user, selected_service.title)
                               
                message = " You can now enter the pin in your phone to finish the payment"
                print(test)
                print(test.MerchantRequestID)
            except:
                error=" There was a connection error"
        
    context={
        'error':error,
        'message':message,
        'services':services
    }
    return render(request, template_name=template_name, context=context)
