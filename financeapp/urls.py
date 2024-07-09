from django.urls import path 
from financeapp import views
app_name = 'financeapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('budget/', views.budget, name='budget'),
    path('accounts/', views.accounts, name='accounts'),
    path('profile/', views.profile, name='profile'),
    path('transactions/', views.transactions, name='transactions'),
]
