import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from alarm.operations import Operations
from getmac import get_mac_address as gma
from alarm.views import user_site_config
import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firealarm.settings")
#django.setup()
oprs= Operations()

connected_user = []

class FireAlarmConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        # self.role_id = self.scope['url_route']['kwargs']['role_id']
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        # self.user_type = self.scope['url_route']['kwargs']['user_type']

        # self.user_group = f'live_user_{self.user_id}_{self.role_id}_{self.user_type}'
        self.user_group = f'live_user_{self.user_id}'

        print(self.user_id, self.user_group)

        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )

        await self.accept()
        if self.user_group not in connected_user:
            connected_user.append({"user_id" : self.user_id, "user_group" : self.user_group,})
            logging.info(f"Connected Users Are : {str(connected_user)}")

        await self.channel_layer.group_send(self.user_group, {
            'type': 'live_link',
            'response': "live_link created.",
        })

        await self.channel_layer.group_send(self.user_group, {
            'type': 'site_config',
            'response': "socket connected.",
        })

    async def disconnect(self, close_code):
        logging.info(f'User Disconnecting... Closing Code {str(close_code)}')
        self.channel_layer.group_discard("wss", self.channel_name)
        for user in connected_user:
            if self.user_group in user['user_group']:
                connected_user.remove(user)
                logging.info(f"Disconnectin User : {self.user_group}")
                logging.info(f"Now Connected Users Are : {str(connected_user)}")

    
    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """

        response = json.loads(text_data)
        oprs.check_opr(response)


    async def send_message(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))

    async def dataSender(self, data):
        self.channel_layer.group_send("wss", {
            'type': 'send_message',
            'response': data,
        })

    async def record(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "status_code": 200,
            "payload": res,
        }))

    async def site_config(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        try:
            await self.send(text_data=json.dumps({
                "status_code": 200,
                "payload": res,
            }))
        except Exception as e:
            logging.error(f"site_config : {str(e)}")

    async def live_link(self, res):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "status_code": 200,
            "payload": res,
        }))

