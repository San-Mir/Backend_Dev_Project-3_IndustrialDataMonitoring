import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Process the incoming data if needed
        await self.send(text_data=json.dumps({
            'device_id': data.get('device_id'),
            'metric': data.get('metric'),
            'timestamp': data.get('timestamp'),
        }))
