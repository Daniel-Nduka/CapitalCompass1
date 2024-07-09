from django.urls import path 
from financeapp import views
app_name = 'financeapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]
