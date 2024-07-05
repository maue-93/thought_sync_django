import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Synch, SynchMembership, UserProfile

User = get_user_model()

class HomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(
                f"user_{self.user.id}",
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        if not self.user.is_anonymous:
            await self.channel_layer.group_discard(
                f"user_{self.user.id}",
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'invite_user':
            await self.invite_user(data)
        elif action == 'create_synch':
            await self.create_synch(data)

    async def invite_user(self, data):
        synch_id = data['synch_id']
        invitee_username = data['invitee_username']

        try:
            synch = await Synch.objects.aget(id=synch_id)
            invitee_user = await User.objects.aget(username=invitee_username)
            invitee_profile = await UserProfile.objects.aget(user=invitee_user)

            # Create SynchMembership
            await SynchMembership.objects.acreate(synch=synch, member=invitee_profile)

            # Send message to the invited user only
            await self.channel_layer.group_add(
                f"user_{invitee_user.id}",
                self.channel_name
            )

            # Send synch data to the invited user
            synch_data = {
                'id': str(synch.id),
                'name': synch.name,
                'creator': str(synch.creator.id) if synch.creator else None,
                'picture': synch.picture.url if synch.picture else None,
                'created_at': synch.created_at.isoformat() if synch.created_at else None,
                'updated_at': synch.updated_at.isoformat() if synch.updated_at else None,
            }
            await self.channel_layer.group_send(
                f"user_{invitee_user.id}",
                {
                    'type': 'synch_invite',
                    'synch_data': synch_data,
                }
            )

        except Exception as e:
            # Handle the exception (log it, send error message, etc.)
            print(e)

    async def create_synch(self, data):
        name = data.get('name')
        creator_profile = await UserProfile.objects.aget(user=self.user)

        try:
            synch = await Synch.objects.acreate(name=name, creator=creator_profile)

            # Send message to the user who created the synch
            synch_data = {
                'id': str(synch.id),
                'name': synch.name,
                'creator': str(synch.creator.id) if synch.creator else None,
                'picture': synch.picture.url if synch.picture else None,
                'created_at': synch.created_at.isoformat() if synch.created_at else None,
                'updated_at': synch.updated_at.isoformat() if synch.updated_at else None,
            }

            await self.send(text_data=json.dumps({
                'type': 'synch_created',
                'synch_data': synch_data
            }))

        except Exception as e:
            # Handle the exception (log it, send error message, etc.)
            print(e)

    async def synch_invite(self, event):
        synch_data = event['synch_data']

        await self.send(text_data=json.dumps({
            'type': 'synch_invite',
            'synch_data': synch_data
        }))
