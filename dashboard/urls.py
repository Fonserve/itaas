# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView, name='home'),
    path('services/', views.ServicesView, name='services'),
    path('my_services/', views.MyServicesView, name='my_services'),
    path('subscriptions/', views.SubscriptionsView, name='subscriptions'),
    path('past_services/', views.PastServicesView, name='past_services'),
    path('ordering/', views.OrderingView, name='ordering'),
    path('analytics/', views.AnalyticsView, name='analytics'),
    path('messaging/', views.MessagingView, name='messaging'),  # Changed from .as_view() to direct function reference
    path('settings/', views.SettingsView, name='settings'),
]