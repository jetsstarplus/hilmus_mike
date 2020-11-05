from rest_framework import serializers
from daraja.models import Lipa_na_mpesa, C2BPaymentModel


class Lipa_na_mpesaSerializer(serializers.Serializer):
    class Meta:
        model = Lipa_na_mpesa
        fields = '__all__'


class C2BPaymentSerializer(serializers.Serializer):
    class Meta:
        model = C2BPaymentModel
        fields ='__all__'
        # { 'id',
        # "TransactionType",
        # "TransID",
        # "TransTime",
        # "TransAmount",
        # "BusinessShortCode",
        # "BillRefNumber",
        # "InvoiceNumber",
        # "OrgAccountBalance",
        # "ThirdPartyTransID",
        # "MSISDN",
        # "FirstName",
        # "MiddleName",
        # "LastName"
        # }

