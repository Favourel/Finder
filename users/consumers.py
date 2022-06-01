from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from .models import Notification
import json
from users.models import User
from django.contrib.auth.models import AnonymousUser
from django.forms.models import model_to_dict


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except:
        return AnonymousUser()


@database_sync_to_async
def create_notification(receiver, request, typeof="task_created", status="unread"):
    # notification_to_create = Notification.objects.filter(user_revoker=receiver, type_of_notification=typeof)
    notification_to_create = Notification.objects.filter(user=request.user, is_seen=False)
    print('I am here to help')
    return notification_to_create.user.username, notification_to_create.is_seen, create_notification


class NotificationConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.request = None

    async def websocket_connect(self, event):
        # print(self.scope)
        await self.accept()

        # notification = Notification.objects.get(user=self.request, is_seen=False)
        # dict = model_to_dict(notification.notification_type)

        await self.send(json.dumps({
            "type": "websocket.send",
            "text": "hello world",
            "msg": "sup it is me",
            # "notification": notification.notification_type,
        }))
        self.room_name = 'test_consumer'
        self.room_group_name = 'test_consumer_group'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # self.send({
        #     "type": "websocket.send",
        #     "text": "room made"
        # })

    async def websocket_receive(self, event):
        print(event)
        data_to_get = json.loads(event['text'])
        user_to_get = await get_user(int(data_to_get))
        print(user_to_get)
        get_of = await create_notification(user_to_get)
        self.room_group_name = 'test_consumer_group'
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "value": json.dumps(get_of)
            }
        )
        print('receive', event)

    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def send_notification(self, event):
        await self.send(json.dumps({
            "type": "websocket.send",
            "data": event,
            "msg": "get"
        }))
        print('I am here')
        print(event)
