from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from datetime import datetime
import pytz

#for handling responses
from rest_framework.response import Response


from daraja.api.serializers import Lipa_na_mpesaSerializer, C2BPaymentSerializer
from daraja import models
from mike_admin.models import Service
# from account.models import UserPayment


class Lipa_List(CreateAPIView):
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
            initiated=models.Initiate.objects.filter(checkoutRequestId=checkout_request_id)
            if  int(result_code)==0: 
               initiated.update(ResultCode=1)
               user=get_user_model().objects.filter(pk=initiated.pk)
               user.update(is_payed=True)
               
            else:
                initiated.update(ResultCode=0)
            
            mpesa_model.save()
            return Response({'ResultDescription': "Yey it worked"})

        ##to check whether the transaction is cancelled or not
        except:
             #creating an instance of our model
            #print(result_description)
            return Response({'ResultDescription': result_description})

# class Customer_to_Business_Validate(CreateAPIView):
#     queryset = models.C2BPaymentModel.objects.all()
#     serializer_class = C2BPaymentSerializer
#     permission_classes = [AllowAny]

    # def create(self, request):
    #     print(request.data + " This is the request")
    #     return Response({'ResultDesc': 0})

      

class Customer_to_Business_Confirm(CreateAPIView):
    queryset = models.C2BPaymentModel.objects.all()
    serializer_class = C2BPaymentSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data + " This is the request")
        return Response({'ResultDesc': 0})


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

 
        