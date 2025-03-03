from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('mark-read/<int:notification_id>/', views.mark_as_read, name='mark_read'),
    path('mark-all-read/', views.mark_all_as_read, name='mark_all_read'),
    path('count/', views.get_unread_count, name='unread_count'),
    path('delete/<int:notification_id>/', views.delete_notification, name='delete'),
]
