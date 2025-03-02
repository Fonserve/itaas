# messaging/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message, GroupChat, GroupMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if self.user.is_anonymous:
            await self.close()
            return
            
        await self.channel_layer.group_add(
            f'user_{self.user.id}',
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        if hasattr(self, 'user') and not self.user.is_anonymous:
            await self.channel_layer.group_discard(
                f'user_{self.user.id}',
                self.channel_name
            )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'direct_message':
            recipient_id = data.get('recipient_id')
            content = data.get('content')
            
            # Save message to database
            message = await self.save_direct_message(recipient_id, content)
            
            # Send to recipient's group
            await self.channel_layer.group_send(
                f'user_{recipient_id}',
                {
                    'type': 'chat_message',
                    'message': {
                        'id': message.id,
                        'sender_id': self.user.id,
                        'sender_name': self.user.username,
                        'content': content,
                        'timestamp': str(message.timestamp),
                        'is_direct': True
                    }
                }
            )
            
            # Send back to sender for confirmation
            await self.send(text_data=json.dumps({
                'type': 'message_sent',
                'message': {
                    'id': message.id,
                    'recipient_id': recipient_id,
                    'content': content,
                    'timestamp': str(message.timestamp)
                }
            }))
            
        elif message_type == 'group_message':
            group_id = data.get('group_id')
            content = data.get('content')
            
            # Save group message
            message = await self.save_group_message(group_id, content)
            group_members = await self.get_group_members(group_id)
            
            # Send to all group members
            for member in group_members:
                if member.id != self.user.id:  # Don't send to sender
                    await self.channel_layer.group_send(
                        f'user_{member.id}',
                        {
                            'type': 'chat_message',
                            'message': {
                                'id': message.id,
                                'sender_id': self.user.id,
                                'sender_name': self.user.username,
                                'content': content,
                                'timestamp': str(message.timestamp),
                                'group_id': group_id,
                                'is_direct': False
                            }
                        }
                    )
            
            # Send back to sender for confirmation
            await self.send(text_data=json.dumps({
                'type': 'message_sent',
                'message': {
                    'id': message.id,
                    'group_id': group_id,
                    'content': content,
                    'timestamp': str(message.timestamp)
                }
            }))
    
    async def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': message
        }))
    
    @database_sync_to_async
    def save_direct_message(self, recipient_id, content):
        recipient = User.objects.get(id=recipient_id)
        message = Message.objects.create(
            sender=self.user,
            recipient=recipient,
            content=content
        )
        return message
    
    @database_sync_to_async
    def save_group_message(self, group_id, content):
        group = GroupChat.objects.get(id=group_id)
        message = GroupMessage.objects.create(
            sender=self.user,
            group=group,
            content=content
        )
        return message
    
    @database_sync_to_async
    def get_group_members(self, group_id):
        group = GroupChat.objects.get(id=group_id)
        return list(group.members.all())