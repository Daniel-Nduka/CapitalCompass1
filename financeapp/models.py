
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

import datetime

# USer Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_accessed_budget = models.ForeignKey('Budget', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.user.username

#Budget Model
class Budget(models.Model):
    BUDGET_TYPES = [
        ('zero_based', 'Zero-Based'),
        ('fifty_thirty_twenty', '50/30/20'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    budget_name = models.CharField(max_length=100)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES)
    month = models.DateField(auto_now_add=True)  # Add month field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   # balance_initialized = models.BooleanField(default=False)

    # Meta class to ensure that the budget name is unique for each user
    class Meta:
        unique_together = ('user', 'budget_name')

    def __str__(self):
        return f"{self.budget_name} ({self.get_budget_type_display()}) - {self.user.username}"

    # Update the assigned amount for each category in the 50/30/20 budget
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
       # ('CREDIT', 'credit'),  # Commented out or use if necessary
       ('CASH', 'cash'),
       ('OTHER', 'other'),
    ]
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='accounts')
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, blank=True, default='OTHER')  # Ensure choices is added
    custom_account_type = models.CharField(max_length=100, blank=True, null=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Add a debug print to check the account type value
        print(f"Debug: account_type={self.account_type}")
        if self.account_type == 'OTHER' and self.custom_account_type:
            return f"{self.account_name} ({self.custom_account_type}) - {self.budget.budget_name}"
        return f"{self.account_name} ({self.get_account_type_display()}) - {self.budget.budget_name}"

    def save(self, *args, **kwargs):
        if self.custom_account_type and self.account_type not in dict(self.ACCOUNT_TYPES).keys():
            self.account_type = 'OTHER'
        super().save(*args, **kwargs)
        self.budget.update_fifty_thirty_twenty_categories()


class PlaidAccount(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='plaid_account')
    access_token = models.CharField(max_length=100)
    item_id = models.CharField(max_length=100)
    plaid_account_id = models.CharField(max_length=100)  # Plaid's account ID for this specific account
    institution_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.institution_name} - {self.account.account_name}"


@receiver(post_save, sender=Account)
def create_initial_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            account=instance,
            date=timezone.now(),
            description=f"Initial balance for {instance.account_name}",
            inflow=instance.balance,
            outflow=0,
            created_by_account=True,
        )

#Base Category
class BaseCategory(models.Model):
    assigned_amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(default=datetime.date.today().replace(day=1))


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   # month_only = models.DateField(default=datetime.date.today().replace(day=1))


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
   # month_only = models.DateField(default=datetime.date.today().replace(day=1))
    is_recurring = models.BooleanField(default=False)
    class Meta:
        unique_together = ('budget', 'name', 'month')

    def __str__(self):
        return self.name
    
# Signal to create a default category when a Zero-Based Budget is created
@receiver(post_save, sender=Budget)
def create_default_zero_based_category(sender, instance, created, **kwargs):
    if created and instance.budget_type == 'zero_based':
        # Check if a default category already exists to avoid duplication
        if not ZeroBasedCategory.objects.filter(budget=instance, name='General Expenses').exists():
            ZeroBasedCategory.objects.create(
                budget=instance,
                name='General Expenses',  # Use the chosen name here
                assigned_amount=Decimal(0.00),  # Default assigned amount, can be modified as needed
            )


class Expense(models.Model):
    fifty_30_twenty_category = models.ForeignKey(FiftyThirtyTwentyCategory, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    category = models.ForeignKey(ZeroBasedCategory, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    is_recurring = models.BooleanField(default=False)  # New field to indicate if the expense is recurring
    month_only = models.DateField(default=datetime.date.today().replace(day=1))

    assigned_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('fifty_30_twenty_category', 'description', 'month_only'), ('category', 'description', 'month_only')


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
            
    def delete(self, *args, **kwargs):
        # Update the account balance based on the transaction before deleting it
         # Reverse the effect of all transactions associated with this expense
        for transaction in self.transactions.all():
            # If it's an outflow transaction, add the amount back to the account
            if transaction.outflow > 0:
                transaction.account.balance += transaction.outflow
            # Save the updated account balance
            transaction.account.save()

        # Now delete the expense
        super().delete(*args, **kwargs)
    


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255, blank=True, null=True)
    payee = models.CharField(max_length=255, blank=True, null=True)
    inflow = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    outflow = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_by_account = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} - {self.description} ({self.inflow} / {self.outflow})"

    def save(self, *args, **kwargs):
        if self.pk is None and not self.created_by_account :  # This check is for a new transaction
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
        else:
            if self.pk is not None:
                old_transaction = Transaction.objects.get(pk=self.pk)
                if old_transaction.inflow > 0:
                    self.account.balance -= Decimal(old_transaction.inflow)
                elif old_transaction.outflow > 0:
                    self.account.balance += Decimal(old_transaction.outflow)
                
                    
                if self.inflow > 0:
                    self.account.balance += Decimal(self.inflow)
                    self.outflow = 0
                elif self.outflow > 0:
                    self.account.balance -= Decimal(self.outflow)
                    self.inflow = 0
                
                    if self.expense:
                        self.expense.spent = Decimal(self.outflow)
                        self.expense.save()
            self.account.save()
                
                

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Update the account balance based on the transaction before deleting it
        if self.inflow > 0:
            self.account.balance -= Decimal(self.inflow)
        if self.outflow > 0:
            self.account.balance += Decimal(self.outflow)

        self.account.save()

        # If this is an outflow, update the linked expense
        if self.outflow > 0 and self.expense:
            self.expense.spent -= Decimal(self.outflow)
            self.expense.save()

        super().delete(*args, **kwargs)

#contactus model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='contact_images/', null=True, blank=True, default=None)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"

class AccountSupport(models.Model):
    PROBLEM_CHOICES = [
        ('General', 'General'),
        ('Technical', 'Technical'),
        ('Financial', 'Financial'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem_type = models.CharField(max_length=20, choices=PROBLEM_CHOICES)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='contact_images/', null=True, blank=True, default=None)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.username}"

