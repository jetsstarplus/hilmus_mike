from django.db import models
from datetime import datetime
from django.utils import timezone
import pytz

from django.conf import settings

from mike_admin.models import Service

# Create your models here.
class Lipa_na_mpesa(models.Model):
    CheckoutRequestID = models.CharField(max_length=50, null = True)
    MerchantRequestID = models.CharField(max_length = 30, null = True)
    ResultCode = models.IntegerField(null = True)
    ResultDesc = models.TextField(max_length = 200,null = True )
    Amount = models.FloatField(null = True)
    MpesaReceiptNumber = models.CharField(max_length = 50, null = True)
    Balance = models.CharField(max_length=10, blank = True, null = True)
    TransationDate = models.DateTimeField(default=timezone.now)
    phonenumber = models.CharField(max_length = 15, null = True)

    class Meta:
        ordering = ["-TransationDate"]
        verbose_name_plural = "Lipa Na Mpesa Payments"
        verbose_name = "Lipa Na Mpesa Payment"

    def __str__(self):
        return self.MpesaReceiptNumber


class C2BPaymentModel(models.Model):
    #Confirmation Respose
        TransactionType = models.CharField(max_length = 13)
        TransID = models.CharField(max_length=50)
        TransTime = models.CharField(max_length = 50)
        TransAmount = models.FloatField()
        BusinessShortCode = models.CharField(max_length = 50)
        BillRefNumber = models.CharField(max_length = 50)
        InvoiceNumber = models.CharField(max_length = 50)
        OrgAccountBalance = models.FloatField()
        ThirdPartyTransID = models.CharField(max_length = 50)
        MSISDN = models.CharField(max_length = 50)
        FirstName = models.CharField(max_length = 50)
        MiddleName = models.CharField(max_length = 50)
        LastName = models.CharField(max_length = 50)
        Status = models.BooleanField(default=False)
        user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
        Service=models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True)
        class Meta:
            ordering = ['TransTime']
            verbose_name_plural = "Customer To Business Payment"
            verbose_name = "Customer To Business Payments"

        def time(self):
            str_transation_date = str(self.TransTime) #changing int datetime to string
            transation_date_time = datetime.strptime(str_transation_date, "%Y%m%d%H%M%S")#changing a string to datetime

            #making transaction datetime to be aware of the timezone
            aware_transaction_datetime = pytz.utc.localize(transation_date_time)
            return aware_transaction_datetime
        
        
        def transaction_name(self):
            return self.FirstName + ' ' + self.LastName
            
        transaction_name.description = "Full Name"  
        
class Initiate(models.Model):       
    CheckoutRequestID = models.CharField(max_length=50, null = True, unique=True)
    MerchantRequestID = models.CharField(max_length = 30, null = True, unique=True)
    ResultCode = models.IntegerField(null = True)
    mode=models.CharField(max_length=40, null = True, blank=True)
    ResultDescription = models.TextField(max_length = 200,null = True)
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="initiated")
    service= models.ForeignKey(Service, on_delete=models.PROTECT)
    date_added= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.CheckoutRequestID
    class Meta:
        verbose_name_plural="Initiated Transactions"
        verbose_name="Initiated Transaction"
        
class Paypal(models.Model):
    """A model that is used to store paypal transactions"""
    name=models.CharField(max_length=50)
    amount=models.FloatField(null=True, blank=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    paypal_id=models.CharField(max_length=100, null=True, blank=True)
    service=models.ForeignKey(Service, on_delete=models.PROTECT, null=True, blank=True)
    currency=models.CharField(max_length=50, null=True, blank=True)
    date_added= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    