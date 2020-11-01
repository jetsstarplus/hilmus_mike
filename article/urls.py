from . import views
from django.urls import path

app_name='article'
urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name="create_post"),
    path('post/<slug:slug>/change/', views.update_post, name="update_post"), 
    path('post/<slug:slug>/delete/', views.delete_post, name="delete_post")
]