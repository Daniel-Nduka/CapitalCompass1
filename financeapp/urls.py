from django.urls import path 
from financeapp import views
app_name = 'financeapp'

urlpatterns = [
    
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    #path('transactions/', views.transactions, name='transactions'),
    
    path('select_budget/<int:budget_id>/', views.select_budget, name='select_budget'),

  
     
    #path for account.intro
   
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('accounts/edit/<int:account_id>/', views.edit_account, name='edit_account'),
    path('accounts/delete/<int:account_id>/', views.delete_account, name='delete_account'),
   


    
    
    path('logout-and-signup/', views.logout_and_signup, name='logout_and_signup'),
    
    path('create-budget/', views.create_budget, name='create_budget'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/delete/<int:budget_id>/', views.delete_budget, name='delete_budget'),
    
    #path for zero_based budget
    path('budgets/zero_based/<int:budget_id>/', views.zero_based_page, name='zero_based_page'), 
    path('budgets/zero-based/<int:budget_id>/<int:year>/<int:month>/', views.zero_based_page, name='zero_based_page_with_date'),
    path('budgets/zero_based/<int:budget_id>/add_category/', views.add_zero_based_category, name='add_zero_category'),
    path('budgets/zero_based/<int:budget_id>/edit_category/', views.edit_zero_based_category, name='edit_zero_category'),
    path('budgets/zero_based/<int:budget_id>/add_expense/', views.add_zero_based_expense, name='add_zero_expense'),
    path('budgets/zero_based/<int:budget_id>/edit_expense/', views.edit_zero_based_expense, name='edit_zero_expense'),
    
    path('budgets/zero_based/<int:budget_id>/delete_category/', views.delete_category, name='delete_zero_category'),
    path('budgets/zero_based/<int:budget_id>/delete_expense/', views.delete_expense, name='delete_zero_expense'),

    #path for 50.30.20 budget
    path('budgets/fifty_thirty_twenty/<int:budget_id>/', views.fifty_thirty_twenty_page, name='fifty_thirty_twenty_page'),
    path('budgets/fifty_thirty_twenty/<int:budget_id>/<int:year>/<int:month>/', views.fifty_thirty_twenty_page, name='fifty_thirty_twenty_page_with_date'),
    path('budgets/fifty_thirty_twenty/<int:budget_id>/add_expense/', views.add_fifty_thirty_twenty_expense, name='add_fifty_thirty_twenty_expense'),
    path('budgets/fifty_thirty_twenty/<int:budget_id>/edit_expense/', views.edit_fifty_thirty_twenty_expense, name='edit_fifty_thirty_twenty_expense'),
    path('budgets/fifty_thirty_twenty/<int:budget_id>/delete_50_expense/', views.delete_50_expense, name='delete_expense'),
    path('budgets/fifty_thirty_twenty/<int:budget_id>/delete_30_expense/', views.edit_fifty_thirty_twenty_category, name='edit_category'),
    
    path('load-sidebar-content/<int:budget_id>/', views.load_sidebar_content_with_budget, name='load_sidebar_content_with_budget'),
    path('load-sidebar-content/', views.load_sidebar_content_without_budget, name='load_sidebar_content_without_budget'),
    
    path('transactions/', views.transaction_list, name='transactions'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
]
