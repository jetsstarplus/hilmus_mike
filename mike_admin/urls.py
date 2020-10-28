from django.urls import path, include

from .import views
from . import auth_urls

app_name='mike_admin'
urlpatterns = [    
    path('', views.home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('', include(auth_urls)),

]