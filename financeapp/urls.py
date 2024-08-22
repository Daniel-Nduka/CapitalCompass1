from django.urls import path 
from financeapp import views
app_name = 'financeapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    
    path('overview/', views.overview, name='overview'),
    path('help/', views.help_page, name='help'),
    
    #path('select_budget/<int:budget_id>/', views.select_budget, name='select_budget'),

  
     
    #path for account.intro
   
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('accounts/edit/', views.edit_account, name='edit_account'),
    path('accounts/delete/<int:account_id>/', views.delete_account, name='delete_account'),
    path('accounts/add_money/', views.add_money_to_account, name='add_money_to_account'),
   


    
    
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
    
    path('budgets/zero_based/<int:budget_id>/delete_category/', views.delete_zero_based_category, name='delete_zero_category'),
    path('budgets/zero_based/<int:budget_id>/delete_expense/', views.delete_zero_based_expense, name='delete_zero_expense'),

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
    path('transactions/edit/', views.edit_transaction, name='edit_transaction'),
    path ('transactions/delete/', views.delete_transaction, name='delete_transaction'), 
    
    path('analysis/', views.financial_analysis, name='financial_analysis'),
    path('analysis/<int:year>/<int:month>/', views.financial_analysis, name='financial_analysis_with_date'),
    
    path('contact/', views.contact, name='contact'),
    #path('contactLog/', views.contactLoggedIn, name='contactLog'),
    path('account_support/', views.account_support, name='account_support'),
    #path('get-categories-for-date/', views.get_categories_for_date, name='get_categories_for_date'),
    
    # Other URL patterns...
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('create-link-token/', views.create_link_token, name='create_link_token'),
   # path('exchange-public-token/', views.exchange_public_token, name='exchange_public_token'),
   # path('get-balance/<int:account_id>/', views.get_balance, name='get_balance'),
   path('create-and-link-account/', views.create_and_link_account, name='create_and_link_account'),
    
]
