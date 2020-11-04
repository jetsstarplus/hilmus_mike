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
    path('testimonial/<int:id>/delete/', views.delete_testimonial, name="delete_testimonial"),
    
    
    # Testimonials urls
    path('staffs/', views.StaffList.as_view(), name='staffs'),
    path('staff/<int:id>/', views.staff_detail, name='staff_detail'),
    path('staff/create/', views.create_staff, name="create_staff"),
    path('staff/<int:id>/change/', views.update_staff, name="update_staff"), 
    path('staff/<int:id>/delete/', views.delete_staff, name="delete_staff"),
    
    # Tos urls
    path('terms/', views.TermsList.as_view(), name='terms'),
    path('terms/<int:id>/', views.terms_detail, name='terms_detail'),
    path('terms/create/', views.create_terms, name="create_terms"),
    path('terms/<int:id>/change/', views.update_terms, name="update_terms"), 
    path('terms/<int:id>/delete/', views.delete_terms, name="delete_terms"),
    
    # Music urls
    path('music/', views.MusicList.as_view(), name='music'),
    path('music/<pk>/', views.music_detail, name='music_detail'),
    path('music/create/', views.create_music, name="create_music"),
    path('music/<pk>/change/', views.update_music, name="update_music"), 
    path('music/<pk>/delete/', views.delete_music, name="delete_music"),
]