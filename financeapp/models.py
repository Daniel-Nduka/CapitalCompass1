
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

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
    balance_initialized = models.BooleanField(default=False)  # Add this line

    def __str__(self):
        return f"{self.budget_name} ({self.get_budget_type_display()}) - {self.user.username}"
    
    def update_fifty_thirty_twenty_categories(self):
        if self.budget_type == 'fifty_thirty_twenty':
            total_balance = sum(account.balance for account in self.accounts.all())
            total_balance_float = float(total_balance)  # Convert Decimal to float
            for category in self.fifty_thirty_twenty_categories.all():
                if category.name == 'Needs':
                    category.assigned_amount = Decimal(0.5 * total_balance_float)
                elif category.name == 'Wants':
                    category.assigned_amount = Decimal(0.3 * total_balance_float)
                else:
                    category.assigned_amount = Decimal(0.2 * total_balance_float)
                category.save()
            


class Account(models.Model):
    ACCOUNT_TYPES = [
       ('CHECKING', 'checking'),
       ('SAVINGS', 'savings'),
      # ('CREDIT', 'credit'), 
       ('CASH', 'cash'),
    ]
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='accounts')
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    previous_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
   # current_balance = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #recurring_income = models.BooleanField(default=False)
    
    
    def __str__(self):
       return f"{self.account_name} ({self.get_account_type_display()}) - {self.budget.budget_name}"
   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the budget's categories if necessary
        self.budget.update_fifty_thirty_twenty_categories()
#Base Category
class BaseCategory(models.Model):
    assigned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(default=datetime.date.today)
   # is_recurring = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
    def __str__(self):
        return self.name

    @property
    def activity(self):
        return sum(expense.spent for expense in self.expenses.all())

    @property
    def available(self):
        return self.assigned_amount - self.activity

    @property
    def expenses_assigned_amount_total(self):
        return sum(expense.assigned_amount for expense in self.expenses.all())
    '''
    def save(self, *args, **kwargs):
        if self.assigned_amount_total > self.assigned_amount:
            self.assigned_amount = self.assigned_amount_total
        super().save(*args, **kwargs)
    '''

 #50.30.20 Models implementation
# 50/30/20 Category Model
class FiftyThirtyTwentyCategory(BaseCategory):
    CATEGORY_CHOICES = [
        ('Needs', 'Needs'),
        ('Wants', 'Wants'),
        ('Savings', 'Savings'),
    ]

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='fifty_thirty_twenty_categories')
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_recurring = models.BooleanField(default=True)  # New field to indicate if category is occuring
  #  is_user_modified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.budget.budget_name} ({self.month.strftime('%B %Y')})"

    class Meta:
        unique_together = ('budget', 'name', 'month')
  
@receiver(post_save, sender=Budget)
def create_fifty_thirty_twenty_categories(sender, instance, created, **kwargs):
    if created and instance.budget_type == 'fifty_thirty_twenty':
        categories = ['Needs', 'Wants', 'Savings']
        for name in categories:
            FiftyThirtyTwentyCategory.objects.create(
                budget=instance,
                name=name,
                assigned_amount=0.0,
                month=instance.month
            )
 
 
#Zero Based Models implementation      
class ZeroBasedCategory(BaseCategory):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='zero_based_categories')
    name = models.CharField(max_length=100) 
    is_recurring = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Expense(models.Model):
    fifty_30_twenty_category = models.ForeignKey(FiftyThirtyTwentyCategory, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    category = models.ForeignKey(ZeroBasedCategory, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
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
  
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the category's assigned amount if necessary
        if self.category:
            self.category.save()
        if self.fifty_30_twenty_category:
            self.fifty_30_twenty_category.save()

   
           
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True, null=True)
    payee = models.CharField(max_length=255, blank=True, null=True)
    inflow = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outflow = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.date} - {self.description} ({self.inflow} / {self.outflow})"

    def save(self, *args, **kwargs):
        # Update the account balance based on the transaction
        if self.inflow > 0:
            self.account.balance += Decimal(self.inflow)
            self.outflow = 0
        if self.outflow > 0:
            self.account.balance -= Decimal(self.outflow)
            self.inflow = 0
        
        self.account.save()

        # If this is an outflow, update the linked expense
        if self.outflow > 0 and self.expense:
            self.expense.spent += Decimal(self.outflow)
            self.expense.save()

        super().save(*args, **kwargs)
    
        