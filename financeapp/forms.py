from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Account, Budget, ZeroBasedCategory, Expense, FiftyThirtyTwentyCategory, Transaction, ContactMessage

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
        fields = ['budget_name', 'budget_type' ]
        
    def clean_budget_name(self):
        budget_name = self.cleaned_data.get('budget_name')
        if Budget.objects.filter(budget_name=budget_name).exists():
            raise forms.ValidationError("Budget name must be unique. The specified name is already in use.")
        return budget_name
        
class ZeroBudgetForm(forms.ModelForm):
    class Meta:
        model = ZeroBasedCategory
        fields = ['name', 'assigned_amount', 'is_recurring']

    def __init__(self, *args, **kwargs):
        self.budget = kwargs.pop('budget', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if ZeroBasedCategory.objects.filter(budget=self.budget, name=name).exists():
            raise forms.ValidationError("Category with this name already exists.")
        return name
        

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
    
class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message', 'subject', 'image']
        
    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        'message': forms.Textarea(attrs={'class': 'form-control'}),
        'subject': forms.TextInput(attrs={'class': 'form-control'}),
        'image': forms.FileInput(attrs={'class': 'form-control'}),
    }
    labels = {
        'name': 'Your Name',
        'email': 'Your Email',
        'message': 'Your Message',
        'subject': 'Subject',
        'image': 'Upload an Image',
    }
    help_texts = {
        'name': 'Enter your name',
        'email': 'Enter your email address',
        'message': 'Enter your message',
        'subject': 'Enter the subject of your message',
        'image': 'Upload an image (optional)',
    }
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")
        message = cleaned_data.get("message")
        subject = cleaned_data.get("subject")
        image = cleaned_data.get("image")

        # Check that all fields are provided
        if not name or not email or not message:
            raise forms.ValidationError("Please provide all fields.")

        return cleaned_data