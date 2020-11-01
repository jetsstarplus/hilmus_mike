from django import forms
from django_registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail

from account.models import Account


class AccountFormSub(RegistrationFormTermsOfService,RegistrationFormUniqueEmail):
    pass

class AccountForm(AccountFormSub):
    class Meta(AccountFormSub.Meta):
        model = Account
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('first_name', 'last_name', 'avatar', 'information')
    def save(self, user=None):
        user_profile = super(ProfileForm, self).save(commit=False)
        if user:            
            user_profile.save()
        return user_profile