from django.urls import path, include

from .import views
from . import auth_urls
from .api import urls

app_name='mike_admin'
urlpatterns = [    
    path('', views.home, name="home"),
    path('profile/', views.profile, name="profile"),
    path('profile/update/', views.update_profile, name="update_profile"),
    path('', include(auth_urls)),
    path('send/', views.sendemail),
    path('', include(urls)),

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
    path('music/<int:pk>/', views.music_detail, name='music_detail'),
    path('music/create/', views.create_music, name="create_music"),
    path('music/<int:pk>/change/', views.update_music, name="update_music"), 
    path('music/<int:pk>/delete/', views.delete_music, name="delete_music"),
    
    # Services urls
    path('service/create/', views.create_service, name="create_service"),
    path('services/', views.ServicesList.as_view(), name='services'),
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),    
    path('service/<slug:slug>/change/', views.update_service, name="update_service"), 
    path('service/<slug:slug>/delete/', views.delete_service, name="delete_service"),
    
    # Category items urls
    path('categories/item/create/', views.create_service, name="create_category_item"),
    path('categories/item/', views.CategoryItemList.as_view(), name='category_items'),
    path('categories/item/<id:id>/', views.service_category_item_detail, name='category_detail'),    
    path('categories/item/<id:id>/change/', views.update_service, name="update_category_item"), 
    path('categories/item/<id:id>/delete/', views.delete_service, name="delete_category_item"),
    
    
    #Users urls
    path('users/', views.UserList.as_view(), name='users'),
    path('user/<str:username>/', views.user_detail, name='user_detail'),
    
    #Users urls
    path('transactions/', views.LipaTransactionList.as_view(), name='lipa'),
    path('messages/',  views.requestMessages, name='post_messages'),
    path('payments/', views.paymentsPage, name="payments")
]
