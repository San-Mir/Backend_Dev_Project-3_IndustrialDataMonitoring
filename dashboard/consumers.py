# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

class DataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send_data()

    def send_data(self):
        # Simulated data that resembles the json_df structure
        sample_data = [
            {
                "device_id": "device_001",
                "metric": 42,
                "timestamp": "2024-11-14T12:34:56",
                "hello_world": "hello world"
            },
            {
                "device_id": "device_002",
                "metric": 78,
                "timestamp": "2024-11-14T12:35:56",
                "hello_world": "hello world"
            }
        ]
        
        # Convert to JSON
        json_data = json.dumps(sample_data)
        
        # Send data to WebSocket
        self.send(text_data=json_data)

    def disconnect(self, close_code):
        pass

