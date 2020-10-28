from . import views
from django.urls import path

app_name='article'
urlpatterns = [
    path('posts/', views.PostList.as_view(), name='post'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name="create_post"),
    path('posts/<slug:slug>/change/', views.PostUpdate.as_view(), name="update_post"), 
    path('posts/<slug:slug>/delete/', views.PostDelete.as_view(), name="delete_post")
]