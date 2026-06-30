import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_room_name = 'chat_lobby'

        await self.channel_layer.group_add(
            self.chat_room_name,
            self.channel_name
        )
        # Simply accept the connection
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_room_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message','')

        await self.channel_layer.group_send(
            self.chat_room_name,
            {
                'type': 'chat_msg',
                'message':message
            }
        )
    async def chat_msg(self,event):
        message = event['message']

        await self.send(
            text_data = json.dumps({
            'message':message
            })
        )
