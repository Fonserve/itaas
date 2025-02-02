# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ServiceOrderListCreateView.as_view(), name='serviceorder-list-create'),
    path('<int:pk>/', views.ServiceOrderDetailView.as_view(), name='serviceorder-detail'),
]