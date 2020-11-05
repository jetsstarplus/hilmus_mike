from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from rest_framework import viewsets
from . import serializers
import requests
from mpesa.daraja import lipa_na_mpesa
import json

#viewsets define the behavior of the view
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializers

 
#This is the form submission view
def lipa_na_mpesa(request):
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
        
