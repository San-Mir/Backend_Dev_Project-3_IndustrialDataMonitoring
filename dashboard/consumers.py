import json
from channels.generic.websocket import WebsocketConsumer
from threading import Thread
from kafka import KafkaConsumer


class DataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # Start a thread to consume data from Kafka and send it to the WebSocket
        self.running = True
        self.thread = Thread(target=self.consume_kafka_data)
        self.thread.start()

    def consume_kafka_data(self):
        """Consume data from Kafka and send it to the WebSocket."""
        try:
            # Set up Kafka consumer
            consumer = KafkaConsumer(
                'iot_data',  # Replace with your Kafka topic name
                bootstrap_servers='localhost:9092',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            )

            while self.running:
                for message in consumer:
                    if not self.running:
                        break  # Exit loop if WebSocket is disconnected

                    data = message.value  # The data from Kafka
                    print(f"Received data from Kafka: {data}")  # Debugging

                    # Send the data to the WebSocket
                    self.send(text_data=json.dumps(data))

        except Exception as e:
            print(f"Error in Kafka consumer thread: {e}")
        finally:
            print("Kafka consumer thread shutting down.")

    def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        self.running = False
        self.thread.join()  # Stop the Kafka consumption thread
        print("WebSocket disconnected.")
