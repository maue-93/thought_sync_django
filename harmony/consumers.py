import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thought_sync.settings")
django.setup()

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Synch, SynchMembership, UserProfile

User = get_user_model()

from channels.consumer import AsyncConsumer

class HomeUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['room_name']

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
   
        # Broadcast message to group if needed
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': text_data_json
            }
        )

    async def group_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
    
# end of HomeUserConsumer


class SynchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['room_name']

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
   
        # Broadcast message to group if needed
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': text_data_json
            }
        )

    async def group_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
    
# end of SynchConsumer


class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['room_name']

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
   
        # Broadcast message to group if needed
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'group_message',
                'message': text_data_json
            }
        )

    async def group_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
    
# end of StreamConsumer