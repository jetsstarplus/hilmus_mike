from django.urls import path, include
from daraja.api import views as apiviews

urlpatterns = [
    path("lmmapi/", apiviews.Lipa_List.as_view(), name ="LipaNaMpesaCallbackApi"),
    path("lmmapi/validate/", apiviews.Customer_to_Business_Validate.as_view(), name ="C2BValidationUrl"),
    path("lmmapi/confirm/", apiviews.Customer_to_Business_Confirm.as_view(), name ="C2BConfirmationUrl"),
    path("lmmapi/balance/", apiviews.Lipa_na_Mpesa_Balance.as_view(), name ="BusinessBalanceUrl"),
    path("lmmapi/qeuetimeout/", apiviews.Lipa_na_Mpesa_QeueTimeOut.as_view(), name ="BusinessQuetimeOut"),
    
]