from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import UserProfile, Account, Budget
from .forms import UserForm, UserProfileForm, AccountForm, BudgetForm

from django.contrib.auth import logout


# Create your views here.
def logout_and_signup(request):
    logout(request)
    return redirect('registration_register')

def index(request):
    return render(request, 'financeapp/index.html')

def about(request):
    return render(request, 'financeapp/about.html')


@login_required
def account_list(request):
    accounts = request.user.accounts.all()
    total_balance = 0
    for account in accounts:
        if account.account_type != 'CREDIT':
            total_balance += account.balance
    
    total_debt = 0
    for account in accounts:
        if account.account_type == 'CREDIT':
            total_debt += account.balance
            
    net_balance = total_balance - total_debt
    
    context ={
        'accounts': accounts,
        'total_balance': total_balance,
        'total_debt': total_debt,
        'net_balance': net_balance,
    }
     
    return render(request, 'financeapp/accounts.html', context)
    

@login_required
def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('financeapp:accounts')
    else:
        form = AccountForm()
    return render(request, 'financeapp/add_account.html', {'form': form})


def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        account.delete()
        return redirect('financeapp:accounts')
    
    context ={
       'account': account
   }
    return render(request, 'financeapp/delete_account.html', context)

def edit_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('financeapp:accounts')
    else:
        form = AccountForm(instance=account)
    return render(request, 'financeapp/edit_account.html', {'form': form})


def transactions(request):
    return render(request, 'financeapp/transactions.html')

@login_required
def profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    }
    return render(request, 'financeapp/profile.html', context)

#Create budget
def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('financeapp:budget_list')
    else:
        form = BudgetForm()
    return render(request, 'financeapp/budget.html', {'form': form})

#Budget List
def budget_list(request):
   budgets = request.user.budgets.all()
   context = {
       'budgets': budgets
   }
   return render(request, 'financeapp/budget_list.html', context)

