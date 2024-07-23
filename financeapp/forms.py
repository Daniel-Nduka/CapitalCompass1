from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Account, Budget, ZeroBasedCategory, Expense

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
        
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['budget_name', 'budget_type', 'currency_type']
        
class ZeroBudgetForm(forms.ModelForm):
    is_recurring = forms.BooleanField(required=False, label='Recurring')
    class Meta:
        model = ZeroBasedCategory
        fields = ['name', 'assigned_amount', 'is_recurring']

class ExpenseForm(forms.ModelForm):
    is_recurring = forms.BooleanField(required=False, label='Recurring')
    class Meta:
        model = Expense
        fields = ['description', 'assigned_amount', 'spent', 'is_recurring']