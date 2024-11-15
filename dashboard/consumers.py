# consumers.py
from queue import Empty
from threading import Thread
import json
from channels.generic.websocket import WebsocketConsumer
from dashboard.spark_consumer import shared_queue

class DataConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # Start a thread to send data from the shared queue to WebSocket
        self.running = True
        self.thread = Thread(target=self.send_data_from_queue)
        self.thread.start()

    def send_data_from_queue(self):
        while self.running:
            try:
                # Retrieve data from the queue with a timeout
                data = shared_queue.get(timeout=1)  # Wait for up to 1 second
                print(f"Sending data to WebSocket: {data}")  # Debugging
                self.send(text_data=data)  # Send the data as WebSocket message
            except Empty:
                # Queue is empty; continue waiting
                continue


    def disconnect(self, close_code):
        self.running = False
        self.thread.join()

