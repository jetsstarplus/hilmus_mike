from django.urls import path, include
from rest_framework import routers
from . import views

#routers provide an easy way of automatically determining the url configurations

router = routers.DefaultRouter()
router.register(r'categories', views.ServiceViewSet)
router.register(r'items', views.CategoryItemsViewSet)

urlpatterns = [
    path('api/hans-project/android/', include(router.urls))
]


 