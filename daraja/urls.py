from django.urls import path, include
from rest_framework import routers
from daraja import views

 #routers provide an easy way of automatically determining the url configurations

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

app_name = "home"

urlpatterns = [
    # path("users/", include(router.urls)),
     path('lipa/stkpush/', views.lipa_mpesa, name="lipa_na_mpesa_form"),
     path('lipa/paybill/<int:id>/confirm/', views.paybill, name="paybill"),
     path('lipa/select-service/', views.select_service, name="select-service"),
     path('payment/paypal/',views.paypal, name="paypal" ),
]