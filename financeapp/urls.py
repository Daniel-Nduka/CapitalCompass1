from django.urls import path 
from financeapp import views
app_name = 'financeapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('budget/', views.budget, name='budget'),
    path('profile/', views.profile, name='profile'),
    path('transactions/', views.transactions, name='transactions'),
    path('accounts/', views.account_list, name='accounts'),
    path('accounts/add/', views.add_account, name='add_account'),
    path('accounts/delete/<int:account_id>/', views.delete_account, name='delete_account'),
    path('accounts/edit/<int:account_id>/', views.edit_account, name='edit_account'),
    path('logout-and-signup/', views.logout_and_signup, name='logout_and_signup'),
]
