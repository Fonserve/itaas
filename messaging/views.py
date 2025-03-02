# messaging/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Message, GroupChat, GroupMessage
from .serializers import (
    MessageSerializer, ConversationSerializer, UserSerializer,
    GroupChatSerializer, GroupMessageSerializer
)

User = get_user_model()

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(recipient=user) | Message.objects.filter(sender=user)

class ConversationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, user_id):
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get all messages between current user and other user
        messages = Message.objects.filter(
            Q(sender=request.user, recipient=other_user) | 
            Q(sender=other_user, recipient=request.user)
        ).order_by('timestamp')
        
        # Mark messages as read
        unread_messages = messages.filter(recipient=request.user, read=False)
        unread_messages.update(read=True)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    def post(self, request, user_id):
        try:
            recipient = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = {
            "sender": request.user.id,
            "recipient": recipient.id,
            "content": request.data.get("content")
        }
        
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConversationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Find all users this user has conversations with
        conversation_users = User.objects.filter(
            Q(sent_messages__recipient=user) | Q(received_messages__sender=user)
        ).distinct().exclude(id=user.id)
        
        conversations = []
        for other_user in conversation_users:
            # Get the last message
            last_message = Message.objects.filter(
                Q(sender=user, recipient=other_user) | 
                Q(sender=other_user, recipient=user)
            ).order_by('-timestamp').first()
            
            # Count unread messages
            unread_count = Message.objects.filter(
                sender=other_user,
                recipient=user,
                read=False
            ).count()
            
            conversations.append({
                'user': {
                    'id': other_user.id,
                    'username': other_user.username,
                    'full_name': other_user.get_full_name()
                },
                'last_message': {
                    'content': last_message.content if last_message else "",
                    'timestamp': last_message.timestamp if last_message else None
                },
                'unread_count': unread_count
            })
        
        return Response(conversations)

class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Return a list of users available for messaging"""
        search_term = request.query_params.get('search', '')
        
        # Get all users except for the current user
        User = get_user_model()
        if search_term:
            users = User.objects.filter(
                Q(username__icontains=search_term) |
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(email__icontains=search_term)
            ).exclude(id=request.user.id)
        else:
            # Without search term, limit results to manageable number
            # In a real app, you might implement pagination
            users = User.objects.exclude(id=request.user.id)[:20]
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class GroupChatListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get all group chats that the current user is a member of"""
        return GroupChat.objects.filter(members=self.request.user)
    
    def perform_create(self, serializer):
        """Ensure the current user is added as a member"""
        group_chat = serializer.save()
        if self.request.user not in group_chat.members.all():
            group_chat.members.add(self.request.user)

class GroupChatDetailView(generics.RetrieveAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get all group chats that the current user is a member of"""
        return GroupChat.objects.filter(members=self.request.user)

class GroupMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Get all messages for a specific group chat"""
        group_id = self.kwargs.get('group_id')
        return GroupMessage.objects.filter(group_id=group_id)
    
    def perform_create(self, serializer):
        """Set the sender to the current user and group to the specified group"""
        group_id = self.kwargs.get('group_id')
        try:
            group = GroupChat.objects.get(id=group_id, members=self.request.user)
        except GroupChat.DoesNotExist:
            return Response(
                {"error": "Group not found or you are not a member"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer.save(sender=self.request.user, group=group)