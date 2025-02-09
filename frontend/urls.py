# accounts/urls.py
from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.landingView, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginView, name='login'),
    path('myaccount/', views.myAccount, name='myaccount'),
    path('logout/', views.logoutView, name='logout'),
]