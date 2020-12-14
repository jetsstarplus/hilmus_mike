
from django.urls import path, include

from . import views

app_name="upload_handler"
urlpatterns = [
    path('account/upload/', views.upload_progress, name="upload_handler"),
]
