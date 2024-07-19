from django.urls import path 
from financeapp import views
app_name = 'financeapp'

urlpatterns = [
    
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('transactions/', views.transactions, name='transactions'),
    
    path('select_budget/<int:budget_id>/', views.select_budget, name='select_budget'),

  
     
    
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('accounts/edit/<int:account_id>/', views.edit_account, name='edit_account'),
    path('accounts/delete/<int:account_id>/', views.delete_account, name='delete_account'),
   


    
    
    path('logout-and-signup/', views.logout_and_signup, name='logout_and_signup'),
    
    path('create-budget/', views.create_budget, name='create_budget'),
    path('budgets/', views.budget_list, name='budget_list'),
    
    
    path('budgets/zero_based/<int:budget_id>/', views.zero_based_page, name='zero_based_page'),
    path('budgets/zero_based/<int:budget_id>/add_category/', views.add_zero_based_category, name='add_category'),
    path('budgets/zero_based/<int:budget_id>/edit_category/', views.edit_zero_based_category, name='edit_category'),
    path('budgets/zero_based/<int:budget_id>/add_expense/', views.add_zero_based_expense, name='add_expense'),
    path('budgets/zero_based/<int:budget_id>/edit_expense/', views.edit_zero_based_expense, name='edit_expense'),

    
]
