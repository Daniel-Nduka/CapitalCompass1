from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import datetime

from .models import UserProfile, Budget, ZeroBasedCategory, Expense, Account
from .forms import UserForm, UserProfileForm, AccountForm, BudgetForm, ZeroBudgetForm, ExpenseForm

from django.contrib.auth import logout


# Create your views here.
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

#This ensures when a user selects a budget, it is stored in the session
@login_required
def select_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    request.session['selected_budget_id'] = budget.id
    return redirect('financeapp:zero_based_page', budget_id=budget.id)

#This is the account list page. When a user selects a budget, it displays the accounts associated with that budget.
#if there is no budget selected, it redirects the user to the budget list page.
@login_required
def account_list(request):
    budget = request.selected_budget
    if not budget:
        return redirect('financeapp:budget_list')

    accounts = Account.objects.filter(budget=budget)
    total_balance = sum(account.balance for account in accounts if account.account_type != 'CREDIT')
    total_debt = sum(account.balance for account in accounts if account.account_type == 'CREDIT')
    net_balance = total_balance - total_debt
    
    context = {
        'budget': budget,
        'accounts': accounts,
        'total_balance': total_balance,
        'total_debt': total_debt,
        'net_balance': net_balance,
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
    else:
        form = AccountForm()
    return render(request, 'financeapp/add_account.html', {'form': form})

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
def edit_account(request, account_id):
    budget = request.selected_budget
    if not budget:
        return redirect('financeapp:budget_list')

    account = get_object_or_404(Account, id=account_id, budget=budget)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('financeapp:account_list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'financeapp/edit_account.html', {'form': form})




def transactions(request):
    return render(request, 'financeapp/transactions.html')

#This is the profile page. It allows users to update their profile information.
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

#Create budget page. after creating a budget, it redirects the user to the budget list page.
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
# Helper Function to copy recurring categories and expenses from the previous budget
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

        if created:
            for expense in category.expenses.filter(is_recurring=True):
                Expense.objects.create(
                    category=new_category,
                    description=expense.description,
                    assigned_amount=expense.assigned_amount,
                    spent=0,  # reset spent for new month
                    is_recurring=expense.is_recurring
                )
#Zero based budget page. It displays the categories and expenses associated with the budget.
#when a user selects a budget, it stores the budget in the session.

@login_required
def zero_based_page(request, budget_id, year=None, month=None):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    request.session['selected_budget_id'] = budget.id

    if not year or not month:
        today = datetime.date.today()
        year, month = today.year, today.month

    selected_date = datetime.date(year, month, 1)

    # Copy recurring items if necessary
    copy_recurring_items(budget, selected_date)

    previous_month_date = selected_date.replace(day=1) - datetime.timedelta(days=1)
    next_month_date = selected_date.replace(day=28) + datetime.timedelta(days=4)
    previous_month = previous_month_date.month
    previous_year = previous_month_date.year
    next_month = next_month_date.replace(day=1).month
    next_year = next_month_date.replace(day=1).year

    categories = ZeroBasedCategory.objects.filter(budget=budget, month__year=year, month__month=month)

    total_balance = 0
    budgeted_money = sum(category.assigned_amount for category in categories)
    accounts = budget.accounts.all()

    for account in accounts:
        if account.account_type != 'CREDIT':
            total_balance += account.balance
        else:
            total_balance -= account.balance

    money_available = total_balance - budgeted_money

    category_form = ZeroBudgetForm()
    expense_form = ExpenseForm()

    context = {
        'budget': budget,
        'categories': categories,
        'category_form': category_form,
        'expense_form': expense_form,
        'money_available': money_available,
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
            category.save()
            return redirect('financeapp:zero_based_page', budget_id=budget.id)
    return redirect('financeapp:zero_based_page', budget_id=budget.id)

@login_required
def edit_zero_based_category(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    category_id = request.POST.get('category_id')
    category = get_object_or_404(ZeroBasedCategory, id=category_id, budget=budget)
    if request.method == 'POST':
        category_form = ZeroBudgetForm(request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
            return redirect('financeapp:zero_based_page', budget_id=budget.id)
    return redirect ('financeapp:zero_based_page', budget_id=budget.id)

@login_required
def delete_category(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    category_id = request.POST.get('category_id')
    category = get_object_or_404(ZeroBasedCategory, id=category_id, budget=budget)
    
    if request.method == 'POST':
        category.delete()
        return redirect('financeapp:zero_based_page', budget_id=budget.id)
    return redirect('financeapp:zero_based_page', budget_id=budget.id)

@login_required
def add_zero_based_expense(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    if request.method == 'POST':
        expense_form = ExpenseForm(request.POST)
        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            expense.category = get_object_or_404(ZeroBasedCategory, id=request.POST.get('category_id'))
            expense.save()
            return redirect('financeapp:zero_based_page', budget_id=budget.id)
    return redirect('financeapp:zero_based_page', budget_id=budget.id)


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
            expense = form.save(commit=False)
            # Ensure is_recurring is explicitly updated
            is_recurring_value = 'is_recurring' in request.POST
            expense.is_recurring = is_recurring_value
            expense.save()
            print(f"Updated is_recurring: {is_recurring_value}")  # Debugging line
            return redirect('financeapp:zero_based_page', budget_id=budget.id)
        else:
            print("Form is invalid", form.errors)  # Debugging line
    else:
        print("Request method is not POST")  # Debugging line
    
    return redirect('financeapp:zero_based_page', budget_id=budget.id)


@login_required
def delete_expense(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user, budget_type='zero_based')
    category_id = request.POST.get('category_id')
    expense_id = request.POST.get('expense_id')
    print(f"Budget ID: {budget_id}")
    print(f"Category ID: {category_id}")
    print(f"Expense ID: {expense_id}")

    if category_id and expense_id:
        category = get_object_or_404(ZeroBasedCategory, id=category_id, budget=budget)
        expense = get_object_or_404(Expense, id=expense_id, category=category)
    
        if request.method == 'POST':
            expense.delete()
            return redirect('financeapp:zero_based_page', budget_id=budget.id)
    
    return redirect('financeapp:zero_based_page', budget_id=budget.id)
