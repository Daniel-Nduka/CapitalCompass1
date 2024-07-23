
from django.db import models
from django.contrib.auth.models import User

import datetime

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    last_accessed_budget = models.ForeignKey('Budget', on_delete=models.SET_NULL, null=True, blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.user.username
    
class Budget(models.Model):
    BUDGET_TYPES = [
        ('zero_based', 'Zero-Based'),
        ('fifty_thirty_twenty', '50/30/20'),
    ]
    
    CURRENCY_TYPES = [
        ('POUNDS', 'Pounds'),
        ('DOLLARS', 'Dollars'),
        ('EUROS', 'euros'),   
        
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    budget_name = models.CharField(max_length=100)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPES, default="POUNDS")
    month = models.DateField(auto_now_add=True)  # Add month field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.budget_name} ({self.get_budget_type_display()}) - {self.user.username}"


class Account(models.Model):
    ACCOUNT_TYPES = [
       ('CHECKING', 'checking'),
       ('SAVINGS', 'savings'),
       ('CREDIT', 'credit'), 
       ('CASH', 'cash'),
    ]
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='accounts')
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
       return f"{self.account_name} ({self.get_account_type_display()}) - {self.budget.budget_name}"

   
    
class ZeroBasedCategory(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='zero_based_categories')
    name = models.CharField(max_length=100)
    assigned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(default=datetime.date.today)
    is_recurring = models.BooleanField(default=False)  # New field to indicate if the category is recurring
    def __str__(self):
        return self.name
    @property
    def activity (self):
        total_activity = 0
        for expense in self.expenses.all():
            total_activity += expense.spent
        return total_activity
    @property
    def available(self):
        return self.assigned_amount - self.activity
    
class Expense(models.Model):
    category = models.ForeignKey(ZeroBasedCategory, on_delete=models.CASCADE, related_name='expenses')  
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    is_recurring = models.BooleanField(default=False)  # New field to indicate if the expense is recurring
    
    assigned_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.assigned_amount} - {self.description}"
    @property   
    def available(self):
        return self.assigned_amount - self.spent

''' 
class Transactions(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.amount} - {self.description}"
        '''
            
   
#inherit from Budget
"""
class ZeroBasedBudget(Budget):
    total_income = models.DecimalField(max_digits=10, decimal_places=2)

class ZeroBasedCategory(models.Model):
    budget = models.ForeignKey(ZeroBasedBudget, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

#Inherits from Budget
class FiftyThirtyTwentyBudget(Budget):
    income = models.DecimalField(max_digits=10, decimal_places=2)

class FiftyThirtyTwentyCategory(models.Model):
    BUDGET_CATEGORIES = [
        ('needs', 'Needs'),
        ('wants', 'Wants'),
        ('savings', 'Savings'),
    ]
    budget = models.ForeignKey(FiftyThirtyTwentyBudget, on_delete=models.CASCADE, related_name='categories')
    category = models.CharField(max_length=20, choices=BUDGET_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    """
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
   
    
    
    
    
    