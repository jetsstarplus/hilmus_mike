from django.urls import path, include

from . import views

app_name='pages'
urlpatterns=[
    path('', views.index, name="index"),
    path('articles/', views.PostList.as_view(), name='articles'),
    path('articles/<slug:slug>/', views.post_detail, name="article_detail"),
    path('articles/search/', views.PostSearchList.as_view(), name="post_search"),
    path("mike-creatives/ajax/submit-contacts/", views.submit_contacts, name = "contacts-submit"),
    path("mike-creatives/hilmus/ajax/submit-subscription/", views.submit_subscription, name = "subscribe"),
    path("terms-of-service/", views.terms, name='terms'),
    path("contact/", views.contact, name="contact"),
]