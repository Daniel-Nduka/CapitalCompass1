from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Account

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'location', 'birth_date')

#Account form
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_name', 'account_type', 'balance']
        
