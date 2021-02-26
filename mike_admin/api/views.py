from rest_framework import viewsets
from rest_framework import permissions

from .serializer import ServiceSerializer, CategorySerializer
from ..models import Service, CategoryItem

class ServiceViewSet(viewsets.ModelViewSet):
    queryset=Service.objects.all().order_by('-date_added')
    serializer_class=ServiceSerializer
    permission_classes=[permissions.AllowAny]
    
class CategoryItemsViewSet(viewsets.ModelViewSet):
    queryset=CategoryItem.objects.all().order_by('-date_added')
    serializer_class=CategorySerializer
    permission_classes=[permissions.AllowAny]
