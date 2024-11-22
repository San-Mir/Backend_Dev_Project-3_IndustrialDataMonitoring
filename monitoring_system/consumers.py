import json
from channels.generic.websocket import AsyncWebsocketConsumer
from kafka import KafkaConsumer
from threading import Thread

class MonitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept WebSocket connection
        await self.accept()

        # Start Kafka consumer thread to fetch data
        self.running = True
        self.thread = Thread(target=self.consume_kafka_data)
        self.thread.start()

    def consume_kafka_data(self):
        """Consume data from Kafka and send it to the WebSocket."""
        # Kafka consumer configuration
        consumer = KafkaConsumer(
            'monitoring_topic',  # Replace with your topic name
            bootstrap_servers='localhost:9092',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        while self.running:
            for message in consumer:
                if not self.running:
                    break  # Exit loop if WebSocket is disconnected

                # Extract Kafka message data
                data = message.value
                print(f"Kafka message received: {data}")

                # Send data to WebSocket client
                self.send(text_data=json.dumps(data))

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()

    async def receive(self, text_data):
        """Handle incoming WebSocket messages (if needed)."""
        # Echo back the received message or process it further
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            'status': 'received',
            'device_id': data.get('device_id'),
            'metric': data.get('metric'),
            'timestamp': data.get('timestamp'),
        }))
