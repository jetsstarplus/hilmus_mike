from django.urls import path, include

from .import views
from . import auth_urls

app_name='mike_admin'
urlpatterns = [    
    path('', views.home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('profile/update/', views.update_profile, name="update_profile"),
    path('', include(auth_urls)),

    # Testimonials urls
    path('testimonials/', views.TestimonialList.as_view(), name='testimonials'),
    path('testimonial/<int:id>/', views.testimonial_detail, name='testimonial_detail'),
    path('testimonial/create/', views.create_testimonial, name="create_testimonial"),
    path('testimonial/<int:id>/change/', views.update_testimonial, name="update_testimonial"), 
    path('testimonial/<int:id>/delete/', views.delete_testimonial, name="delete_testimonial")
]