from .models import Comment, Post
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
         'body': forms.Textarea(attrs={
                              'style': 'height: 120px;width:100%'}),
       }
        
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title', 'image', 'content', 'status')   
        widgets ={
            'content': SummernoteWidget,
        }  
        
class PostUpdateForm(forms.ModelForm):
     class Meta:
        model=Post
        fields=('image', 'content', 'status')   
        widgets ={
            'content': SummernoteWidget,
        } 