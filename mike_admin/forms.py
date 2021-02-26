from django import forms
from django_registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail

from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from account.models import Account
from .models import TermsOfService, Testimonial, StaffMember, Music, Service, CategoryItem


class AccountFormSub(RegistrationFormTermsOfService,RegistrationFormUniqueEmail):
    pass

class AccountForm(AccountFormSub):
    class Meta(AccountFormSub.Meta):
        model = Account
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('first_name', 'last_name', 'phone', 'avatar', 'information')
        
    # def save(self, user=None):
    #     user_profile = super(ProfileForm, self).save(commit=False)
    #     if user:            
    #         user_profile.save()
    #     return user_profile
    
class TermsForm(forms.ModelForm):
    class Meta:
        model=TermsOfService
        fields=('title', 'content')
        widgets={
            'title':forms.TextInput(
                attrs={'onkeyup':'resetForm()'}),
            'content': SummernoteWidget(
                attrs={'onkeyup':'resetForm()'}
            )
            } 
  
class ServiceForm(forms.ModelForm):
    class Meta:
        model=Service
        exclude=('date_added', 'date_modified', 'slug')
        widgets={
            'title':forms.TextInput(
                attrs={'onkeyup':'resetForm()'}),
            'content': SummernoteWidget(
                attrs={'onkeyup':'resetForm()'}
            )
            }  
        
        # widgets ={
        #     'content': SummernoteWidget,
        # } 
        
class CategoryItemsForm(forms.ModelForm):
    class Meta:
        model=CategoryItem
        exclude=('date_added', 'date_modified')
        widgets={
            'title':forms.TextInput(
                attrs={'onkeyup':'resetForm()'}),
            'content': SummernoteWidget(
                attrs={'onkeyup':'resetForm()'}
            )
        } 
  
class TestimonialForm(forms.ModelForm):
     class Meta:
         model= Testimonial
         fields = ('name', 'picture', 'is_published', 'content')
         widgets={
             'name':forms.TextInput(
                 attrs={'onkeyup':'resetForm()'}),
             }
         
class StaffMemberForm(forms.ModelForm):
    class Meta:
        model= StaffMember
        fields='__all__'
       
         
        
class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields=['title','music','picture', 'is_boompay', 'is_skiza', 'description']
        
        widgets = {'music': forms.FileInput(
            attrs={
                'accept': 'audio/*',
                'onselect':'resetForm()'}),
             'title':forms.TextInput(
                 attrs={'onkeyup':'resetForm()'}),
             }
         
