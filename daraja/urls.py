from django.urls import path, include
from rest_framework import routers
from daraja import views

 #routers provide an easy way of automatically determining the url configurations

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

app_name = "home"

urlpatterns = [
    # path("users/", include(router.urls)),
     path("hilmus/ajax/submit/user/transaction/initiate/", views.lipa_na_mpesa_view, name = "lipa_na_mpesa"),
]