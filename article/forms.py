from .models import Comment, Post
from django import forms

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
         'body': forms.Textarea(attrs={
                              'style': 'height: 8rem;width:100%; border-radius:5px; border:none; border-bottom:2px solid #dedede'}),
        
       }
        
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title', 'image', 'content', 'status') 
        widgets = {
            'title':forms.TextInput(
                attrs={'onkeyup':'resetForm()'}),
            'content': SummernoteWidget(
                attrs={'onkeyup':'resetForm()'}
            )}
        
class PostUpdateForm(forms.ModelForm):
     class Meta:
        model=Post
        fields=('image', 'content', 'status') 
        widgets = {  
        'content': SummernoteWidget(
            attrs={'onkeyup':'resetForm()'}
        )
        }