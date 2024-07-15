from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.user.username

class Account(models.Model):
    ACCOUNT_TYPES = [
       ('CHECKING', 'checking'),
       ('SAVINGS', 'savings'),
       ('CREDIT', 'credit'), 
       ('CASH', 'cash'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
       return f"{self.account_name} ({self.get_account_type_display()}) - {self.user.username}"

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    