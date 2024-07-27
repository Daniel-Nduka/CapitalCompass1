from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Account, Budget, ZeroBasedCategory, Expense, FiftyThirtyTwentyCategory

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
'''
class Fifty_Twenty_ThirtyForm(forms.ModelForm):
    class Meta:
        model = FiftyThirtyTwentyCategory
        fields = ['name', 'assigned_amount']
'''

class Fifty_Twenty_ThirtyForm(forms.ModelForm):
    class Meta:
        model = FiftyThirtyTwentyCategory
        fields = ['assigned_amount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_amount'].label = 'Custom Assigned Amount'

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_user_modified = True  # Set the flag to indicate the user has modified the amount
        if commit:
            instance.save()
        return instance
    
class ExpenseForm(forms.ModelForm):
    is_recurring = forms.BooleanField(required=False, label='Recurring')
    class Meta:
        model = Expense
        fields = ['description', 'assigned_amount', 'spent', 'is_recurring']