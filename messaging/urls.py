# messaging/urls.py
from django.urls import path
from . import views

# From main urls.py
#    path('api/messaging/', include('messaging.urls')),

urlpatterns = [
    path('', views.MessageListCreateView.as_view(), name='message-list-create'),
    path('conversations/', views.ConversationListView.as_view(), name='conversation-list'),
    path('conversations/<int:user_id>/', views.ConversationView.as_view(), name='conversation-detail'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('groups/', views.GroupChatListCreateView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', views.GroupChatDetailView.as_view(), name='group-detail'),
    path('groups/<int:group_id>/messages/', views.GroupMessageListCreateView.as_view(), name='group-messages'),
]