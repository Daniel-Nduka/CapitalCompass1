from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    last_accessed_budget = models.ForeignKey('Budget', on_delete=models.SET_NULL, null=True, blank=True)

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
        ('EUROS', 'Euros'),   
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    budget_name = models.CharField(max_length=100)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES)
    currency_type = models.CharField(max_length=20, choices=CURRENCY_TYPES, default="POUNDS")
    month = models.DateField(auto_now_add=True)
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
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_name} ({self.get_account_type_display()}) - {self.budget.budget_name}"

# Base Category
class BaseCategory(models.Model):
    assigned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(default=datetime.date.today)
    is_recurring = models.BooleanField(default=False)

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
    def assigned_amount_total(self):
        return sum(expense.assigned_amount for expense in self.expenses.all())

    def save(self, *args, **kwargs):
        if self.assigned_amount_total > self.assigned_amount:
            self.assigned_amount = self.assigned_amount_total
        super().save(*args, **kwargs)

# 50/30/20 Models
'''
class FiftyThirtyTwentyBudget(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='fifty_thirty_twenty_budgets')
    month = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"50/30/20 Budget for {self.budget.budget_name} - {self.month.strftime('%B %Y')}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.categories.exists():
            categories = ['Needs', 'Wants', 'Savings']
            for category in categories:
                FiftyThirtyTwentyCategory.objects.create(
                    budget=self,
                    category=category,
                    assigned_amount=0.0
                )

class FiftyThirtyTwentyCategory(BaseCategory):
    CATEGORY_CHOICES = [
        ('Needs', 'Needs'),
        ('Wants', 'Wants'),
        ('Savings', 'Savings'),
    ]

    budget = models.ForeignKey(FiftyThirtyTwentyBudget, on_delete=models.CASCADE, related_name='categories')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.category} - {self.budget.budget.budget_name}"
'''

# Zero-Based Models
class ZeroBasedCategory(BaseCategory):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='zero_based_categories')
    name = models.CharField(max_length=100)

class Expense(models.Model):
   # fifty_30_twenty_category = models.ForeignKey(FiftyThirtyTwentyCategory, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    category = models.ForeignKey(ZeroBasedCategory, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    is_recurring = models.BooleanField(default=False)
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
        self.category.save()
'''
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.category:
            self.category.save()
        if self.fifty_30_twenty_category:
            self.fifty_30_twenty_category.save()
'''