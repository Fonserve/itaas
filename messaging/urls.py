# messaging/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MessageListCreateView.as_view(), name='message-list-create'),
]