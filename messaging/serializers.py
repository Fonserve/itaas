# messaging/serializers.py
from rest_framework import serializers
from .models import Message, GroupChat, GroupMessage
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'sender_name', 'recipient_name', 'content', 'timestamp', 'read']
    
    def get_sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.username
    
    def get_recipient_name(self, obj):
        return obj.recipient.get_full_name() or obj.recipient.username

class ConversationSerializer(serializers.Serializer):
    user = UserSerializer()
    last_message = serializers.DictField()
    unread_count = serializers.IntegerField()

class GroupChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        source='members',
        queryset=User.objects.all(),
        many=True,
        write_only=True
    )
    
    class Meta:
        model = GroupChat
        fields = ['id', 'name', 'members', 'member_ids', 'created_at']
        read_only_fields = ['created_at']
    
    def create(self, validated_data):
        members = validated_data.pop('members')
        group_chat = GroupChat.objects.create(**validated_data)
        group_chat.members.set(members)
        return group_chat

class GroupMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    
    class Meta:
        model = GroupMessage
        fields = ['id', 'group', 'sender', 'sender_name', 'content', 'timestamp']
    
    def get_sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.username