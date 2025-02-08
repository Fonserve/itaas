# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingView, name='home'),
    path('register/', views.register, name='register'),
]