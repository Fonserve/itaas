# subscriptions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.SubscriptionListView.as_view(), name='subscription-list'),
    path('create/', views.SubscriptionCreateView.as_view(), name='subscription-create'),
]