import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user_inbox = None

    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.room = await Room.objects.aget(name=self.room_name)
        self.user_inbox = f"inbox_{self.user.username}"

        # connection has to be accepted
        await self.accept()

        # join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            # create a user inbox for private messages
            await self.channel_layer.group_add(
                self.user_inbox,
                self.channel_name,
            )
            # send the join event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_join",
                    "user": self.user.username,
                },
            )
            await self.room.online.aadd(self.user)

    async def disconnect(self, close_code):
        # leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            # delete the user inbox for private messages
            await self.channel_layer.group_discard(
                self.user_inbox,
                self.channel_name,
            )
            # send the leave event to the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_leave",
                    "user": self.user.username,
                },
            )
            await self.room.online.aremove(self.user)

    # persist message to database
    async def persist_message(self, message):
        await Message.objects.acreate(user=self.user, room=self.room, content=message)

    # receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        now = timezone.now()

        if not self.user.is_authenticated:
            return

        if message.startswith("/pm "):
            split = message.split(" ", 2)
            target = split[1]
            target_msg = split[2]

            # send private message to the target
            await self.channel_layer.group_send(
                f"inbox_{target}",
                {
                    "type": "private_message",
                    "user": self.user.username,
                    "message": target_msg,
                },
            )
            # send private message delivered to the user
            await self.send(
                json.dumps(
                    {
                        "type": "private_message_delivered",
                        "target": target,
                        "message": target_msg,
                    }
                )
            )
            return

        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.user.username,
                "datetime": now.isoformat(),
            },
        )

        # persist message
        await self.persist_message(message)

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))

    async def user_join(self, event):
        await self.send(text_data=json.dumps(event))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps(event))

    async def private_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def private_message_delivered(self, event):
        await self.send(text_data=json.dumps(event))
