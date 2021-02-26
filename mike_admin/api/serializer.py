from rest_framework import serializers
from ..models import Service, CategoryItem


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItem
        fields ='__all__'
       

