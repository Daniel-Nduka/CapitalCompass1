from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Account, Budget, ZeroBasedCategory, Expense, FiftyThirtyTwentyCategory, Transaction

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
   # income_recurring = forms.BooleanField(required=False, label='Recurring')
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
  '''  
class ExpenseForm(forms.ModelForm):
    is_recurring = forms.BooleanField(required=False, label='Recurring')
    class Meta:
        model = Expense
        fields = ['description', 'assigned_amount', 'is_recurring']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'expense', 'date', 'description', 'payee', 'inflow', 'outflow'] 
    
    widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            #'inflow': forms.NumberInput(attrs={'class': 'form-control'}),
          #  'outflow': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    labels = {
            'account': 'Select Account',
            'expense': 'Select Expense (if applicable)',
            'date': 'Date of Transaction',
            'payee': 'Payee',
            'description': 'Description',
            'inflow': 'Inflow Amount',
            'outflow': 'Outflow Amount',
        }
    help_texts = {
            'date': 'Enter the date of the transaction',
            'description': 'Enter a description of the transaction',
            'inflow': 'Enter the inflow amount',
            'outflow': 'Enter the outflow amount',
        }
    def clean(self):
        cleaned_data = super().clean()
        inflow = cleaned_data.get("inflow")
        outflow = cleaned_data.get("outflow")

        # Check that at least one of inflow or outflow is provided
        if not inflow and not outflow:
            raise forms.ValidationError("Please provide either an inflow or an outflow.")

        # Check that only one of inflow or outflow is provided
        if inflow and outflow:
            raise forms.ValidationError("Please provide either an inflow or an outflow, not both.")

        return cleaned_data
