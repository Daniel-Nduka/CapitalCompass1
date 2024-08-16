from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import UserProfile, Budget, ZeroBasedCategory, Expense, Account, FiftyThirtyTwentyCategory, Transaction, ContactMessage, AccountSupport
from .forms import UserForm, AccountForm, BudgetForm, ZeroBudgetForm, ExpenseForm, Fifty_Twenty_ThirtyForm, TransactionForm, ContactMessageForm, AccountSupportForm, AddMoneyForm
from django.db.models import Sum
import random
from django.contrib.auth import logout
import logging
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone

logger = logging.getLogger(__name__)
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.db import IntegrityError

def csrf_failure(request, reason=""):
    return render(request, 'financeapp/index.html')

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'


# Create your views here.

#overview
@login_required
def overview(request):
    return render(request, 'financeapp/overview.html')

#This ensures when a user clicks sign up, if there is an authenticated user, it logs them out and redirects them to the sign up page.
def logout_and_signup(request):
    logout(request)
    return redirect('registration_register')

#This is the index page
def index(request):
    return render(request, 'financeapp/index.html')

#This is the about page
def about(request):
    return render(request, 'financeapp/about.html')

@login_required
def help_page(request):
    return render(request, 'financeapp/help_page.html')

#This ensures when a user selects a budget, it is stored in the session
'''
@login_required
def select_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    request.session['selected_budget_id'] = budget.id
    
    if budget.budget_type == 'zero_based':
        return redirect('financeapp:zero_based_page', budget_id=budget.id)
    else: 
        return redirect('financeapp:fifty_thirty_twenty_page', budget_id=budget.id)
'''

#This is the account list page. When a user selects a budget, it displays the accounts associated with that budget.
#if there is no budget selected, it redirects the user to the budget list page.

@login_required
def account_list(request):
    budget = request.selected_budget
    if not budget:
        return redirect('financeapp:budget_list')   

    accounts = Account.objects.filter(budget=budget)
    total_balance = sum(account.balance for account in accounts)
 
    
    context = {
        'budget': budget,
        'accounts': accounts,
        'total_balance': total_balance,
    }
    return render(request, 'financeapp/accounts.html', context)

@login_required
def add_account(request):
    budget = request.selected_budget
    if not budget:
        return redirect('financeapp:budget_list')

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.budget = budget
            account.save()
            return redirect('financeapp:account_list')
    return redirect('financeapp:account_list')

@login_required
def delete_account(request, account_id):
    budget = request.selected_budget
    if not budget:
        return redirect('financeapp:budget_list')
    account = get_object_or_404(Account, id=account_id, budget=budget)  
    if request.method == 'POST':
        account.delete()
        return redirect('financeapp:account_list')
    
    context = {
        'account': account
    }
    return render(request, 'financeapp/delete_account.html', context)

@login_required
def edit_account(request):
    account_id = request.POST.get('account_id')
    budget = request.selected_budget
    if not budget:
        return redirect('financeapp:budget_list')

    account = get_object_or_404(Account, id=account_id, budget=budget)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('financeapp:account_list')
    return redirect('financeapp:account_list')

#add money to account
@login_required
def add_money_to_account(request):
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            account_id = request.POST.get('account_id')
            account = get_object_or_404(Account, id=account_id, budget__user=request.user)
            amount = form.cleaned_data['amount']

            # Add money to the account
            account.balance += amount
            account.save()

            # Create a transaction for adding money
            Transaction.objects.create(
                account=account,
                inflow=amount,
                outflow=0,
                description=f'Added £{amount} to {account.account_name}',
                date=timezone.now(),
                created_by_account=True,
            )

            messages.success(request, f'£{amount} has been added to {account.account_name}.')
        else:
            messages.error(request, 'There was an error adding money. Please try again.')

    return redirect('financeapp:account_list')
'''

def transactions(request):
    return render(request, 'financeapp/transactions.html')
'''
#This is the profile page. It allows users to update their profile information.
@login_required
def profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=user)  # Create a new UserProfile instance for the user

    if request.method == 'POST':
        if 'profile_form' in request.POST:
            user_form = UserForm(request.POST, instance=user)
        #    profile_form = UserProfileForm(request.POST, instance=user_profile)
            if user_form.is_valid():
                user_form.save()
              #  profile = profile_form.save(commit=False)
              #  profile.user = user  # Ensure the user field is set
             ##   profile.save()
                messages.success(request, 'Your profile has been updated successfully.')
                return redirect('financeapp:profile')
            else:
                messages.error(request, 'Please correct the errors below.')
        elif 'password_form' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('financeapp:profile')
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=user)
       # profile_form = UserProfileForm(instance=user_profile)
        password_form = PasswordChangeForm(user)

    context = {
        'user_form': user_form,
       # 'profile_form': profile_form,
        'password_form': password_form,
        'user_profile': user_profile,
    }
    return render(request, 'financeapp/profile.html', context)

#Create budget page. after creating a budget, it redirects the user to the budget list page.
@login_required
def create_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)  # Pass user here
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            try:
                budget.save()
                messages.success(request, 'Budget created successfully!')
                return redirect('financeapp:budget_list')
            except IntegrityError:
                form.add_error('budget_name', 'A budget with this name already exists.')
        else:
            # Capture and display form errors
            for error in form.errors.values():
                messages.error(request, error, extra_tags='budget_danger')
    else:
        form = BudgetForm(user=request.user)  # Pass user here
    return render(request, 'financeapp/budget.html', {'form': form})


#Budget list page. It displays the budgets associated with the user.
@login_required
def budget_list(request):
   budgets = request.user.budgets.all()
   context = {
       'budgets': budgets
   }
   return render(request, 'financeapp/budget_list.html', context)
@login_required

def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
   
    if request.method == 'POST':
        #ensure the selected budget is removed from the session
        if request.session.get('selected_budget_id') == budget_id:
            del request.session['selected_budget_id']
        budget.delete()
        messages.success(request, 'Budget deleted successfully.')
        return redirect('financeapp:budget_list')
    context = {
        'budget': budget
    }
    return render(request, 'financeapp/delete_budget.html', context)

@login_required
def copy_recurring_items(budget, selected_date):
    last_month = selected_date - datetime.timedelta(days=1)
    last_month_categories = ZeroBasedCategory.objects.filter(budget=budget, month__year=last_month.year, month__month=last_month.month, is_recurring=True)

    for category in last_month_categories:
        new_category, created = ZeroBasedCategory.objects.get_or_create(
            budget=budget,
            name=category.name,
            month=selected_date,
            defaults={'assigned_amount': category.assigned_amount, 'is_recurring': category.is_recurring}
        )

        for expense in category.expenses.filter(is_recurring=True):
            Expense.objects.get_or_create(
                category=new_category,
                description=expense.description,
                assigned_amount=expense.assigned_amount,
                spent=0,  # reset spent for new month
                is_recurring=expense.is_recurring
            )

#Helper ensures when a user selects a budget, it is stored in the session
'''
@login_required
def select_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    request.session['selected_budget_id'] = budget.id
    
    if budget.budget_type == 'zero_based':
        return redirect('financeapp:zero_based_page', budget_id=budget.id)
    else: 
        return redirect('financeapp:fifty_thirty_twenty_page', budget_id=budget.id)
'''
    
#Zero based budget page. It displays the categories and expenses associated with the budget.
#when a user selects a budget, it stores the budget in the session.
        
@login_required
def zero_based_page(request, budget_id, year=None, month=None):
    #Retrieve the selected budget from the session
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    request.session['selected_budget_id'] = budget.id

    # Get the selected date
    if not year or not month:
        today = datetime.date.today()
        year, month = today.year, today.month

    selected_date = datetime.date(year, month, 1)
    copy_recurring_items(budget, selected_date)

    previous_month_date = selected_date.replace(day=1) - datetime.timedelta(days=1)
    next_month_date = selected_date.replace(day=28) + datetime.timedelta(days=4)
    previous_month = previous_month_date.month
    previous_year = previous_month_date.year
    next_month = next_month_date.replace(day=1).month
    next_year = next_month_date.replace(day=1).year

    categories = ZeroBasedCategory.objects.filter(budget=budget, month__year=year, month__month=month)
    
    # Calculate the total balance for the budget
    total_balance = 0
    accounts = budget.accounts.all()
    for account in accounts:
        total_balance += account.balance

    budgeted_money = sum(category.assigned_amount for category in categories)
    
    # Calculate the total amount spent
    spent_money = sum(category.activity for category in categories)
    
    # Calculate the money available
    money_available = total_balance - spent_money


    category_form = ZeroBudgetForm()
    expense_form = ExpenseForm()

    context = {
        'budget': budget,
        'categories': categories,
        'category_form': category_form,
        'expense_form': expense_form,
        'total_balance': total_balance,
        'money_available': money_available,
        'budgeted_money': budgeted_money,
        'spent_money': spent_money,
        'selected_date': selected_date,
        'year': year,
        'month': month,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'financeapp/zero_based_budget_detail.html', context)


#Add zero based category. It allows users to add a category to the zero based budget.
@login_required
def add_zero_based_category(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    if request.method == 'POST':
        form = ZeroBudgetForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.budget = budget
            try:
                category.save()
                messages.success(request, 'Category added successfully.')
                return redirect('financeapp:zero_based_page', budget_id=budget.id)  
            except IntegrityError:
                messages.error(request, 'A category with this name already exists.', extra_tags='add_zero_category_danger')
        else:
            # Capture and display form errors
            for error in form.errors.values():
                messages.error(request, error, extra_tags='add_zero_category_danger')      
    else:
        form = ZeroBudgetForm(budget=budget)
    return redirect('financeapp:zero_based_page', budget_id=budget.id)

def handle_integrity_error(request, budget, form, category_id=None, template_name='financeapp/zero_based_budget_detail.html'):
    # Determine the budget type and get the appropriate category model and context name
    if budget.budget_type == 'zero_based':
        CategoryModel = ZeroBasedCategory
        category_context_name = 'category_id'
        template_name = 'financeapp/zero_based_budget_detail.html'
    elif budget.budget_type == 'fifty_thirty_twenty':
        CategoryModel = FiftyThirtyTwentyCategory
        category_context_name = 'fifty_30_twenty_category_id'
        template_name = 'financeapp/fifty_thirty_twenty_budget_detail.html'
    else:
        raise ValueError("Unsupported budget type")
    
    # Log the category ID and budget details for debugging
    print(f"Handling IntegrityError for budget: {budget.budget_type}, Category ID: {category_id}")

    # Retrieve the category based on the category_id
    category = get_object_or_404(CategoryModel, id=category_id, budget=budget)
    
    # Query for the categories in the selected month
    categories = CategoryModel.objects.filter(budget=budget, month__year=category.month.year, month__month=category.month.month)
    
    # Calculate totals
    total_balance = budget.accounts.aggregate(Sum('balance'))['balance__sum'] or 0
    budgeted_money = sum(cat.assigned_amount for cat in categories)
    spent_money = sum(cat.activity for cat in categories)
    money_available = total_balance - spent_money

    # Determine previous and next month
    previous_month_date = category.month.replace(day=1) - datetime.timedelta(days=1)
    next_month_date = category.month.replace(day=28) + datetime.timedelta(days=4)
    previous_month = previous_month_date.month
    previous_year = previous_month_date.year
    next_month = next_month_date.replace(day=1).month
    next_year = next_month_date.replace(day=1).year

    # Create context dictionary
    context = {
        'budget': budget,
        'category_form': form,  # Pass the bound form to retain values
        'form': form,
        category_context_name: category_id,  # Use the appropriate context name for the category ID
        'categories': categories,
        'total_balance': total_balance,
        'budgeted_money': budgeted_money,
        'spent_money': spent_money,
        'money_available': money_available,
        'selected_date': category.month,
        'year': category.month.year,
        'month': category.month.month,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
    }

    return render(request, template_name, context)

#Edit zero based category
@login_required
def edit_zero_based_category(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    category_id = request.POST.get('category_id')
    category = get_object_or_404(ZeroBasedCategory, id=category_id, budget=budget)

    if request.method == 'POST':
        category_form = ZeroBudgetForm(request.POST, instance=category)
        if category_form.is_valid():
            updated_category = category_form.save(commit=False)
            is_recurring = updated_category.is_recurring

            try:
                # Save the current category
                updated_category.save()

                # If the category is recurring, update future instances
                if is_recurring:
                    future_categories = ZeroBasedCategory.objects.filter(
                        budget=budget,
                        name=updated_category.name,
                        month__gt=updated_category.month,
                        is_recurring=True
                    )
                    for future_category in future_categories:
                        future_category.assigned_amount = updated_category.assigned_amount
                        future_category.save()

                return redirect('financeapp:zero_based_page', budget_id=budget.id)
            except IntegrityError:
                messages.error(request, 'A category with this name already exists.', extra_tags='edit_zero_category_danger')
                return handle_integrity_error(request, budget, category_form, category_id)
    return redirect('financeapp:zero_based_page', budget_id=budget.id)


#Delete zero-based Category
@login_required
def delete_zero_based_category(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    category_id = request.POST.get('category_id')
    category = get_object_or_404(ZeroBasedCategory, id=category_id, budget=budget)
    
    if request.method == 'POST':
        category.delete()
        return redirect('financeapp:zero_based_page', budget_id=budget.id)
    return redirect('financeapp:zero_based_page', budget_id=budget.id)

#Add zero based expense
@login_required
def add_zero_based_expense(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        category_id = request.POST.get('category_id')
        
        # Ensure category_id is provided and valid
        if not category_id or not category_id.isdigit():
            messages.error(request, 'Please select a valid category.', extra_tags='add_zero_expense_danger')
            return redirect('financeapp:zero_based_page', budget_id=budget.id)
        
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            category = get_object_or_404(ZeroBasedCategory, id=category_id)
            expense.category = category
            
            try: 
                expense.save()
                messages.success(request, 'Expense added successfully.')
                return redirect('financeapp:zero_based_page', budget_id=budget.id)
            except IntegrityError:
                messages.error(request, 'An expense with this description already exists.', extra_tags='add_zero_expense_danger')
                return handle_integrity_error(request, budget, expense_form, category_id)
        else:
            print(f"Form is invalid: {expense_form.errors}")  # Debugging line
            messages.error(request, 'Form is invalid. Please correct the errors and try again.', extra_tags='add_zero_expense_danger')
    
    return redirect('financeapp:zero_based_page', budget_id=budget.id)


#Edit zero based expense
@login_required
def edit_zero_based_expense(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    category_id = request.POST.get('category_id')
    category = get_object_or_404(ZeroBasedCategory, id=category_id, budget=budget)
    expense_id = request.POST.get('expense_id')
    expense = get_object_or_404(Expense, id=expense_id, category=category)
    

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated_expense = form.save(commit=False)
            is_recurring = 'is_recurring' in request.POST

            # Save the current expense
            updated_expense.is_recurring = is_recurring
            
            try: 
                updated_expense.save()
          
                if is_recurring:
                    future_expenses = Expense.objects.filter(
                        category__budget=budget,
                        category__name=category.name,
                        description=updated_expense.description,
                        category__month__gt=category.month,
                        is_recurring=True
                    )
                    for future_expense in future_expenses:
                        future_expense.assigned_amount = updated_expense.assigned_amount
                        future_expense.save()

                return redirect('financeapp:zero_based_page', budget_id=budget.id)
            except IntegrityError:
                messages.error(request, 'An expense with this description already exists.', extra_tags='edit_zero_expense_danger')
                return handle_integrity_error(request, budget, form, category_id)

        else:
            print("Form is invalid", form.errors)  # Debugging line
    else:
        print("Request method is not POST")  # Debugging line

    return redirect('financeapp:zero_based_page', budget_id=budget.id)

#Delete zero based expense
@login_required
def delete_zero_based_expense(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    category_id = request.POST.get('category_id')
    expense_id = request.POST.get('expense_id')

    if category_id and expense_id:
        category = get_object_or_404(ZeroBasedCategory, id=category_id, budget=budget)
        expense = get_object_or_404(Expense, id=expense_id, category=category)
    
        if request.method == 'POST':
            expense.delete()
            return redirect('financeapp:zero_based_page', budget_id=budget.id)
    
    return redirect('financeapp:zero_based_page', budget_id=budget.id)
#implementation of the 50/30/20 budget
@login_required
def copy_recurring_items_fifty_thirty_twenty(budget, selected_date):
    last_month = selected_date - datetime.timedelta(days=1)

    # Get last month's categories
    last_month_categories = FiftyThirtyTwentyCategory.objects.filter(
        budget=budget,
        month__year=last_month.year,
        month__month=last_month.month,
        is_recurring=True
    )

    for category in last_month_categories:
        # Create or update category for the current month
        new_category, created = FiftyThirtyTwentyCategory.objects.get_or_create(
            budget=budget,
            name=category.name,
            month=selected_date,
            defaults={'assigned_amount': category.assigned_amount, 'is_recurring': category.is_recurring}
        )

        for expense in category.expenses.filter(is_recurring=True):
            Expense.objects.get_or_create(
                fifty_30_twenty_category=new_category,
                description=expense.description,
                assigned_amount=expense.assigned_amount,
                spent=0,  # Reset spent for the new month
                is_recurring=expense.is_recurring
                )

                         
@login_required
def fifty_thirty_twenty_page(request, budget_id, year=None, month=None):
    base_budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='fifty_thirty_twenty')
    request.session['selected_budget_id'] = base_budget.id

    if not year or not month:
        today = datetime.date.today()
        year, month = today.year, today.month

    selected_date = datetime.date(year, month, 1)
    copy_recurring_items_fifty_thirty_twenty(base_budget, selected_date)
   
    previous_month_date = selected_date.replace(day=1) - datetime.timedelta(days=1)
    next_month_date = selected_date.replace(day=28) + datetime.timedelta(days=4)
    previous_month = previous_month_date.month
    previous_year = previous_month_date.year
    next_month = next_month_date.replace(day=1).month
    next_year = next_month_date.replace(day=1).year

    categories = FiftyThirtyTwentyCategory.objects.filter(budget=base_budget, month__year=year, month__month=month)
    
    # Calculate the total balance for the budget
    total_balance = 0
    accounts = base_budget.accounts.all()
    for account in accounts:
        total_balance += account.balance
        
    budgeted_money = sum(category.assigned_amount for category in categories)
    
    # Calculate the total amount spent
    spent_money = sum(category.activity for category in categories)
       
    money_available = total_balance - spent_money

    category_form = Fifty_Twenty_ThirtyForm()
    expense_form = ExpenseForm()

    context = {
        'budget': base_budget,
        'categories': categories,
        'category_form': category_form,
        'expense_form': expense_form,
        'money_available': money_available,
        'total_balance': total_balance,
        'budgeted_money': budgeted_money,
        'spent_money': spent_money,
        'selected_date': selected_date,
        'year': year,
        'month': month,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'financeapp/fifty_thirty_twenty_budget_detail.html', context)

@login_required
def edit_fifty_thirty_twenty_category(request, budget_id):
    base_budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='fifty_thirty_twenty')
    category_id = request.POST.get('fifty_30_twenty_category_id')
    category = get_object_or_404(FiftyThirtyTwentyCategory, id=category_id, budget=base_budget)
    if request.method == 'POST':
        category_form = Fifty_Twenty_ThirtyForm(request.POST, instance=category)
        if category_form.is_valid():
            updated_category = category_form.save(commit=False)
           # is_recurring = updated_category.is_recurring
            # Save the current category
            updated_category.save()
      
            future_categories = FiftyThirtyTwentyCategory.objects.filter(
                budget=base_budget,
                name=updated_category.name,
                month__gt=updated_category.month,
                is_recurring=True
                )

            for future_category in future_categories:
                future_category.assigned_amount = updated_category.assigned_amount
                future_category.save()
            return redirect('financeapp:fifty_thirty_twenty_page', budget_id=base_budget.id)
    return redirect('financeapp:fifty_thirty_twenty_page', budget_id=base_budget.id)

@login_required
def add_fifty_thirty_twenty_expense(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='fifty_thirty_twenty')
    
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            category_id = request.POST.get('fifty_30_twenty_category_id')

            if not category_id or not category_id.isdigit():
                messages.error(request, 'Please select a valid category.', extra_tags='add_fifty_expense_danger')
                return redirect('financeapp:fifty_thirty_twenty_page', budget_id=budget.id)
            
            try:
                expense.fifty_30_twenty_category = get_object_or_404(FiftyThirtyTwentyCategory, id=category_id)
                expense.save()
                messages.success(request, 'Expense added successfully.')
                return redirect('financeapp:fifty_thirty_twenty_page', budget_id=budget.id)
            except IntegrityError:
                messages.error(request, 'An expense with this description already exists.', extra_tags='add_fifty_expense_danger')
                return handle_integrity_error(request, budget, expense_form, category_id)
        else:
            messages.error(request, 'Form is invalid. Please correct the errors and try again.', extra_tags='add_fifty_expense_danger')

    return redirect('financeapp:fifty_thirty_twenty_page', budget_id=budget.id)

#Edit fifty thirty twenty expense
@login_required
def edit_fifty_thirty_twenty_expense(request, budget_id):
    base_budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='fifty_thirty_twenty')

    category_id = request.POST.get('fifty_30_twenty_category_id')
    category = get_object_or_404(FiftyThirtyTwentyCategory, id=category_id, budget=base_budget)
    expense_id = request.POST.get('expense_id')
    expense = get_object_or_404(Expense, id=expense_id, fifty_30_twenty_category=category)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            updated_expense = form.save(commit=False)
            is_recurring = 'is_recurring' in request.POST

            # Save the current expense
            updated_expense.is_recurring = is_recurring       
            try: 
                updated_expense.save()

                # If the expense is recurring, update future instances
                if is_recurring:
                    future_expenses = Expense.objects.filter(
                        fifty_30_twenty_category__budget=base_budget,
                        fifty_30_twenty_category__name=category.name,
                        description=updated_expense.description,
                        fifty_30_twenty_category__month__gt=category.month,
                        is_recurring=True
                    )
                    for future_expense in future_expenses:
                        future_expense.assigned_amount = updated_expense.assigned_amount
                        future_expense.save()
                    
                return redirect('financeapp:fifty_thirty_twenty_page', budget_id=base_budget.id)
            except IntegrityError:
                messages.error(request, 'An expense with this description already exists.', extra_tags='edit_fifty_expense_danger')
                return handle_integrity_error(request, base_budget, form, category_id)
        else:
            print("Form is invalid", form.errors)  # Debugging line
    else:
        print("Request method is not POST")  # Debugging line

    return redirect('financeapp:fifty_thirty_twenty_page', budget_id=base_budget.id)


@login_required
def delete_50_expense(request, budget_id):
    base_budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='fifty_thirty_twenty')

    # Ensure the current month's budget is retrieved or created
    today = datetime.date.today()
    selected_date = datetime.date(today.year, today.month, 1)
    #fifty_thirty_twenty_budget, _ = FiftyThirtyTwentyBudget.objects.get_or_create(budget=base_budget, month=selected_date)

    category_id = request.POST.get('fifty_30_twenty_category_id')
    expense_id = request.POST.get('expense_id')

    if category_id and expense_id:
        category = get_object_or_404(FiftyThirtyTwentyCategory, id=category_id, budget=base_budget)
        expense = get_object_or_404(Expense, id=expense_id, fifty_30_twenty_category=category)
        if request.method == 'POST':
            expense.delete()
            return redirect('financeapp:fifty_thirty_twenty_page', budget_id=base_budget.id)

    return redirect('financeapp:fifty_thirty_twenty_page', budget_id=base_budget.id)

@login_required
def load_sidebar_content_with_budget(request, budget_id):
    if request.is_ajax():
        budget = get_object_or_404(Budget, id=budget_id, user=request.user)
        request.session['selected_budget_id'] = budget_id  # Set selected budget in session
        sidebar_content = render_to_string('financeapp/sidebar_dynamic_content.html', {'budget': budget}, request=request)
        return JsonResponse({'sidebar_content': sidebar_content})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def load_sidebar_content_without_budget(request):
    if request.is_ajax():
        sidebar_content = render_to_string('financeapp/sidebar_dynamic_content.html', {'budget': None}, request=request)
        return JsonResponse({'sidebar_content': sidebar_content})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def transaction_list(request):
    budget = request.session.get('selected_budget_id')
    if not budget:
        return redirect('financeapp:budget_list')

    budget = get_object_or_404(Budget, id=budget)
    # Determine the default selected date, today for example
    selected_date = request.POST.get('date', datetime.date.today())
    
    # Extract year and month from the selected date
    if isinstance(selected_date, str):
        selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
    year = selected_date.year
    month = selected_date.month

    # Filter expenses for the selected month
    
    if (budget.budget_type == 'zero_based'):
        categories = ZeroBasedCategory.objects.filter(budget_id=budget,
                                                  month__year=year, 
                                                  month__month=month
                                                  ).prefetch_related('expenses')
    else:
        categories = FiftyThirtyTwentyCategory.objects.filter(budget_id=budget,
                                                  month__year=year, 
                                                  month__month=month
                                                  ).prefetch_related('expenses')
    transactions = Transaction.objects.filter(account__budget_id=budget)
    accounts = Account.objects.filter(budget_id=budget)
    context = {
        'transactions': transactions,
        'accounts': accounts,
        'categories': categories,
        'today': datetime.date.today(),
        'form': TransactionForm()  # Always provide an empty form here
    }
    return render(request, 'financeapp/transactions.html', context)

@login_required
def add_transaction(request):
    budget = request.session.get('selected_budget_id')
    if not budget:
        return redirect('financeapp:budget_list')

    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.account = transaction_form.cleaned_data['account']
            transaction.save()
            messages.success(request, 'Transaction added successfully.')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    # Always redirect to transaction_list after adding a transaction
    return redirect('financeapp:transactions')

@login_required
def edit_transaction(request):
    budget_id = request.session.get('selected_budget_id')
    if not budget_id:
        return redirect('financeapp:budget_list')
    
    transaction_id = request.POST.get('transaction_id')
    if not transaction_id:
        messages.error(request, 'Transaction ID is required.')
        return redirect('financeapp:transactions')

    transaction = get_object_or_404(Transaction, id=transaction_id, account__budget_id=budget_id)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully.')
        else:
            # Log form errors
            for field, errors in form.errors.items():
                print(f"Error in {field}: {errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        # In case the request method is not POST, do nothing or render an error page.
        messages.error(request, 'Invalid request method.')

    return redirect('financeapp:transactions')

@login_required
def delete_transaction(request):
    budget_id = request.session.get('selected_budget_id')
    if not budget_id:
        return redirect('financeapp:budget_list')
    
    transaction_id = request.POST.get('transaction_id')
    if not transaction_id:
        messages.error(request, 'Transaction ID is required.')
        return redirect('financeapp:transactions')

    transaction = get_object_or_404(Transaction, id=transaction_id, account__budget_id=budget_id)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully.')
        return redirect('financeapp:transactions')  # Add redirection here

    
    return redirect('financeapp:transactions')
'''
@login_required
def get_categories_for_date(request):
    budget = request.session.get('selected_budget_id')
    if not budget:
        return JsonResponse({'error': 'No budget selected'}, status=400)

    budget = get_object_or_404(Budget, id=budget)

    date_str = request.GET.get('date')
    try:
        selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        year, month = selected_date.year, selected_date.month
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    if budget.budget_type == 'zero_based':
        categories = ZeroBasedCategory.objects.filter(budget_id=budget,
                                                      month__year=year,
                                                      month__month=month)
    else:
        categories = FiftyThirtyTwentyCategory.objects.filter(budget_id=budget,
                                                              month__year=year,
                                                              month__month=month)

    category_data = [{'id': category.id, 'name': category.name} for category in categories]

    return JsonResponse({'categories': category_data})
'''

@login_required   
def financial_analysis(request, year=None, month=None):
    # Fetch categories and their assigned amounts
    budget_id = request.session.get('selected_budget_id')
    budget = get_object_or_404(Budget, id=budget_id)
    analysis_type = request.GET.get('analysis_type', 'categories')
    selected_category_id = request.GET.get('category_id')
    
    if not year or not month:
        today = datetime.date.today()
        year, month = today.year, today.month

    selected_date = datetime.date(year, month, 1)
    
    previous_month_date = selected_date.replace(day=1) - datetime.timedelta(days=1)
    next_month_date = (selected_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    previous_month = previous_month_date.month
    previous_year = previous_month_date.year
    next_month = next_month_date.month
    next_year = next_month_date.year
    

    # Default to show all categories
    if (budget.budget_type == 'zero_based'):
        categories = ZeroBasedCategory.objects.filter(budget__id=budget_id, month__year=year, month__month=month)
        previous_categories = ZeroBasedCategory.objects.filter(budget__id=budget_id, month__year=previous_year, month__month=previous_month)
    else:
        categories = FiftyThirtyTwentyCategory.objects.filter(budget__id=budget_id, month__year=year, month__month=month)
        previous_categories = FiftyThirtyTwentyCategory.objects.filter(budget__id=budget_id, month__year=previous_year, month__month=previous_month)
    category_labels = [category.name for category in categories]
    assigned_amounts = [category.assigned_amount for category in categories]
    total_assigned_amount = categories.aggregate(Sum('assigned_amount'))['assigned_amount__sum'] or 1
    category_data = [float(category.assigned_amount / total_assigned_amount) * 100 for category in categories]
    category_colors = ['#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in categories]
    
    
    # Create a dictionary for easy lookup of previous category amounts
    previous_category_dict = {category.name: category.assigned_amount for category in previous_categories}
    
    # Compare the previous month's categories with the current month's categories
    comparison_results_categories = {}
    for category in categories:
        prev_amount = previous_category_dict.get(category.name, 0)  # Get previous amount, default to 0 if not found
        comparison_results_categories[category.name] = category.assigned_amount - prev_amount
        
    
    # Identify the categories with the most and least budgeted amounts
    
   # previous_assigned_amounts = [category.assigned_amount for category in previous_categories]
    max_budget_category = categories.order_by('-assigned_amount').first()
    min_budget_category = categories.order_by('assigned_amount').first()

    # Fetch all expenses for the "all_expenses" analysis
    if (budget.budget_type == 'zero_based'):
        expenses = Expense.objects.filter(category__budget__id=budget_id, category__month__year=year, category__month__month=month)
    else:
        expenses = Expense.objects.filter(fifty_30_twenty_category__budget__id=budget_id, fifty_30_twenty_category__month__year=year, fifty_30_twenty_category__month__month=month)
    total_expense_amount = expenses.aggregate(Sum('assigned_amount'))['assigned_amount__sum'] or 1
    expense_labels = [expense.description for expense in expenses]
    expense_data = [float(expense.assigned_amount / total_expense_amount) * 100 for expense in expenses]
    expense_colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in expenses]
    max_expense = expenses.order_by('-assigned_amount').first()
    min_expense = expenses.order_by('assigned_amount').first()
    
    # Create a dictionary for easy lookup of previous category expenses
    previous_expense_dict = {expense.description: expense.spent for category in previous_categories for expense in category.expenses.all()}
    #compare the previous month's expenses with the current month's expenses spent
    comparison_results_expenses = {}
    for expense in expenses:
        prev_amount = previous_expense_dict.get(expense.description, 0)
        comparison_results_expenses[expense.description] = expense.spent - prev_amount
    
    # Check if there's any data for the selected month
    has_category_data = categories.exists()
    
    has_expense_data = expenses.exists()
    

    context = {
        'has_category_data': has_category_data,
        'has_expense_data': has_expense_data,
        'comparison_results_categories': comparison_results_categories,
        'comparison_results_expenses': comparison_results_expenses,
       # 'previous_assigned_amounts': previous_assigned_amounts,
        'assigned_amounts': assigned_amounts,
        'analysis_type': analysis_type,
        'categories': categories,
        'category_labels': category_labels,
        'category_data': category_data,
        'category_colors': category_colors,
        'assigned_amounts': assigned_amounts,
        'max_budget_category': max_budget_category,
        'min_budget_category': min_budget_category,
        'selected_date': selected_date,
        'selected_month': month,
        'selected_year': year,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
    }

    if analysis_type == 'expenses_within_category':
        selected_category = None
        
        if (budget.budget_type == 'zero_based'):
            if selected_category_id:
                selected_category = ZeroBasedCategory.objects.filter(id=selected_category_id, budget__id=budget_id).first()
            if not selected_category:
                selected_category = categories.first()  # Default to the first category if no valid selection
        else:
            if selected_category_id:
                selected_category = FiftyThirtyTwentyCategory.objects.filter(id=selected_category_id, budget__id=budget_id).first()
            if not selected_category:
                selected_category = categories.first()
        
        if selected_category:
            selected_category_id = selected_category.id  # Ensure selected_category_id is set
            expenses_within_category = selected_category.expenses.all()
            total_expense_within_category_amount = expenses_within_category.aggregate(Sum('assigned_amount'))['assigned_amount__sum'] or 1

            expense_labels = [expense.description for expense in expenses_within_category]
            expense_data = [float(expense.assigned_amount / total_expense_within_category_amount) * 100 for expense in expenses_within_category]
            expense_colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in expenses_within_category]

            max_expense = expenses_within_category.order_by('-assigned_amount').first()
            min_expense = expenses_within_category.order_by('assigned_amount').first()

            context.update({
                'selected_category_id': selected_category_id,
                'category_name': selected_category.name,
                'expense_labels': expense_labels,
                'expense_data': expense_data,
                'expense_colors': expense_colors,
                'max_expense': max_expense,
                'min_expense': min_expense,
        })

    
    if analysis_type == 'all_expenses':
        context.update({
            'expense_labels': expense_labels,
            'expense_data': expense_data,
            'expense_colors': expense_colors,
            'max_expense': max_expense,
            'min_expense': min_expense,
        })

    return render(request, 'financeapp/financial_analysis.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST, request.FILES)
        if form.is_valid():
            # Save form data to the database
            contact_message = form.save()

            # Prepare email content
            subject = f"New Contact Message from {contact_message.name}"
            message = (
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n"
                f"Subject: {contact_message.subject}\n"
                f"Message:\n{contact_message.message}\n"
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.CONTACT_EMAIL]

            # Send the email
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            # Prepare the confirmation email content to the sender
            sender_subject = "Thank you for contacting us!"
            sender_message = (
                f"Dear {contact_message.name},\n\n"
                "Thank you for reaching out to us. We have received your message and will get back to you soon.\n\n"
                "Best regards,\n"
                "The CapitalCompass Team"
            )
            recipient_list = [contact_message.email]

            # Send the confirmation email to the sender
            send_mail(sender_subject, sender_message, from_email, recipient_list, fail_silently=False)

            # Display success message and redirect
            messages.success(request, 'Your message has been sent successfully.', extra_tags='contact')
            return redirect('financeapp:contact')
        else:
            messages.error(request, 'Please correct the errors below.', extra_tags='contact')    
    else:
        form = ContactMessageForm()

    return render(request, 'financeapp/contact.html', {'form': form})


'''
def contactLoggedIn(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST, request.FILES)
        if form.is_valid():
            # Save form data to the database
            contact_message = form.save()

            # Prepare email content
            subject = f"New Contact Message from {contact_message.name}"
            message = (
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n"
                f"Subject: {contact_message.subject}\n"
                f"Message:\n{contact_message.message}\n"
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.CONTACT_EMAIL]

            # Send the email
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            # Prepare the confirmation email content to the sender
            sender_subject = "Thank you for contacting us!"
            sender_message = (
                f"Dear {contact_message.name},\n\n"
                "Thank you for reaching out to us. We have received your message and will get back to you soon.\n\n"
                "Best regards,\n"
                "The CapitalCompass Team"
            )
            recipient_list = [contact_message.email]

            # Send the confirmation email to the sender
            send_mail(sender_subject, sender_message, from_email, recipient_list, fail_silently=False)

            # Display success message and redirect
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('financeapp:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactMessageForm()

    return render(request, 'financeapp/contactLoggedin.html', {'form': form})
'''

@login_required  
def account_support(request):
    if request.method == 'POST':
        form = AccountSupportForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # Save form data to the database
            account_support = form.save(commit=False)
            account_support.user = request.user
            account_support.save()

            # Prepare email content
            subject = f"New Account Support Request from {request.user.username}"
            message = (
                f"Name: {request.user.username}\n"
                f"Email: {request.user.email}\n"
                f"Problem Type: {account_support.problem_type}\n"
                f"Subject: {account_support.subject}\n"
                f"Message:\n{account_support.message}\n"
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.CONTACT_EMAIL]

            # Send the email to the support team
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            # Prepare the confirmation email content to the sender
            sender_subject = "Thank you for contacting us!"
            sender_message = (
                f"Dear {request.user.get_full_name()},\n\n"
                "Thank you for reaching out to us. We have received your message and will get back to you soon.\n\n"
                "Best regards,\n"
                "The CapitalCompass Team"
            )
            recipient_list = [request.user.email]

            # Send the confirmation email to the sender
            send_mail(sender_subject, sender_message, from_email, recipient_list, fail_silently=False)

            # Display success message and redirect
            messages.success(request, 'Your message has been sent successfully.', extra_tags='account_support')
            return redirect('financeapp:account_support')
        else:
            messages.error(request, 'Please correct the errors below.', extra_tags='account_support')
    else:
        form = AccountSupportForm(user=request.user)

    return render(request, 'financeapp/account_support.html', {'form': form})