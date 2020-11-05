from django.db import models
from datetime import datetime
from django.utils import timezone
import pytz

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
        TransID = models.CharField(max_length=12)
        TransTime = models.CharField(max_length = 20)
        TransAmount = models.FloatField()
        BusinessShortCode = models.CharField(max_length = 12)
        BillRefNumber = models.CharField(max_length = 20)
        InvoiceNumber = models.CharField(max_length = 20)
        OrgAccountBalance = models.FloatField()
        ThirdPartyTransID = models.CharField(max_length = 20)
        MSISDN = models.CharField(max_length = 20)
        FirstName = models.CharField(max_length = 20)
        MiddleName = models.CharField(max_length = 20)
        LastName = models.CharField(max_length = 20)

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