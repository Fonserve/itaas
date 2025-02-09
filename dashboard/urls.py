# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView, name='home'),
    path('services/', views.ServicesView, name='services'),
]