from .models import Comment, Post
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title', 'content', 'status')   
        widgets ={
            'content': SummernoteWidget,
        }   