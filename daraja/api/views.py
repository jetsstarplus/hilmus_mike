from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from datetime import datetime
import pytz
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden
from django.core.mail import send_mail
from django.conf import settings

#for handling responses
from rest_framework.response import Response


from daraja.api.serializers import Lipa_na_mpesaSerializer, C2BPaymentSerializer
from daraja import models
from mike_admin.models import Service
# from account.models import UserPayment


class Lipa_List(CreateAPIView):
    """This method waits for the response from mpesa and stores the successful transaction information"""
    queryset = models.Lipa_na_mpesa.objects.all()
    serializer_class = Lipa_na_mpesaSerializer
    permission_classes = [AllowAny]
    
    
    def create(self, request, *args, **kwargs):
        print(request.data, "this is the request.data")

        merchant_request_id = request.data["Body"]['stkCallback']['MerchantRequestID']
        checkout_request_id = request.data["Body"]['stkCallback']['CheckoutRequestID']
        result_code = request.data["Body"]["stkCallback"]['ResultCode']
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
      
        try:
            amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
            mpesa_receipt_no = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
            balance = ""        
            transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
            phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
                        
            str_transation_date = str(transaction_date) #changing int datetime to string
            transation_date_time = datetime.strptime(str_transation_date, "%Y%m%d%H%M%S")#changing a string to datetime

            #making transaction datetime to be aware of the timezone
            aware_transaction_datetime = pytz.utc.localize(transation_date_time)
        
            #creating an instance of our model
            mpesa_model = models.Lipa_na_mpesa.objects.create(
                CheckoutRequestID = checkout_request_id,
                MerchantRequestID = merchant_request_id,
                ResultCode = result_code,
                ResultDesc = result_description,
                Amount = amount,
                MpesaReceiptNumber = mpesa_receipt_no,
                Balance = balance,
                TransationDate = aware_transaction_datetime,
                phonenumber = phone_number,
        
            )
            initiated=models.Initiate.objects.get(CheckoutRequestID=checkout_request_id)                     
            user=get_user_model().objects.get(pk=initiated.user.pk)
            if result_code==0: 
                # Checking if the transaction was successful with result code 0 and changing the user's information to payed
               user.is_payed= True
               user.save(update_fields=['is_payed'])   
               initiated.ResultDescription=result_description
               initiated.CheckoutRequestID=mpesa_receipt_no
               initiated.save(update_fields=['ResultDescription', 'MpesaReceiptNumber'])            
            else:
                initiated.ResultCode=1
                initiated.save(update_fields=['ResultCode'])
            
            mpesa_model.save()
            send_mail(                                
                    'Mpesa Transaction Completed',
                    'Your Mpesa Transaction to Mike Creatives towards payment for Ksh {} of service {} has been successfully received.'.format(amount, initiated.service),
                    'Transaction Complete <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                    [request.user.email],
                    fail_silently=True,
                )
                
            send_mail(                                
                'Mpesa Transaction Completed',
                'Mpesa Transaction to Mike Creatives for reference {} towards payment for USD {} of service {} has been successfully received.'.format(mpesa_receipt_no, amount, initiated.service),
                'Transaction Complete <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                ['mikecreatives254@gmail.com', 'w.mwangi95@gmail.com', 'edwinkyalo@hotmail.com'],
                fail_silently=True,
            )
            return Response({'ResultDescription': "Yey it worked"})

        ##to check whether the transaction is cancelled or not
        except:
             #creating an instance of our model
            #print(result_description)
            return Response({'ResultDescription': result_description})


def Customer_to_Business_Validate(request):
    print(request.data, " This is the request") 
    TransAmount=request.data["TransAmount"]
    BillRefNumber=request.data["BillRefNumber"]
    
    payed_service=base64.b64decode(BillRefNumber.encode('ascii')).decode('ascii')
    payed_service=payed_service.split('+')[1]
    
    service=Service.objects.filter(id=payed_service)
    if service.Price==float(TransAmount):
        return HttpResponse(content="Success", status=200, reason="Amount Matches", content_type='application/json', charset=utf-8)
    else:
        return HttpResponseForbidden(content_type="application/json")
      

class Customer_to_Business_Confirm(CreateAPIView):
    """This method stores the information from the customer to business transaction"""
    queryset = models.C2BPaymentModel.objects.all()
    serializer_class = C2BPaymentSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, " This is the request")
         
        TransactionType=request.data["TransactionType"]
        TransID=request.data["TransID"]
        TransTime=request.data["TransTime"]
        TransAmount=request.data["TransAmount"]
        BusinessShortCode=request.data["BusinessShortCode"]
        BillRefNumber=request.data["BillRefNumber"]
        InvoiceNumber=request.data["InvoiceNumber"]
        OrgAccountBalance=request.data["OrgAccountBalance"]
        ThirdPartyTransID=request.data["ThirdPartyTransID"]
        MSISDN=request.data["MSISDN"]
        FirstName=request.data["FirstName"]
        MiddleName=request.data["MiddleName"]
        LastName=request.data["LastName"]
        
        str_transation_date = str(TransTime) #changing int datetime to string
        transation_date_time = datetime.strptime(str_transation_date, "%Y%m%d%H%M%S")#changing a string to datetime

        #making transaction datetime to be aware of the timezone
        aware_transaction_datetime = pytz.utc.localize(transation_date_time)
        
        mpesa_model=models.C2BPaymentModel(
            TransactionType=TransactionType,
            TransID=TransID,
            TransTime=aware_transaction_datetime,
            TransAmount=TransAmount,
            BusinessShortCode=BusinessShortCode,
            BillRefNumber=BillRefNumber,
            InvoiceNumber=InvoiceNumber,
            OrgAccountBalance=OrgAccountBalance,
            ThirdPartyTransID=ThirdPartyTransID,
            MSISDN=MSISDN,
            FirstName=FirstName,
            MiddleName=MiddleName,
            LastName=LastName,
            Status=False
        )
        
        mpesa_model.save()
        return HttpResponse("success")


#this method is used to get the balance
class Lipa_na_Mpesa_Balance(CreateAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, " This is the balance request")
        return Response({'ResultDesc': 0})

  
#a general method for handling the qeuetime out of all the requests
class Lipa_na_Mpesa_QeueTimeOut(CreateAPIView):
    queryset = None
    serializer_class = None
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data + " This is the qeue time out request")
        return Response({'ResultDesc': 0})
    