# simulator.py

import json
import time
import random
from kafka import KafkaProducer
from config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, DEVICE_IDS, DATA_FREQUENCY

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_data():
    """Generates random data for each device and sends it to Kafka."""
    while True:
        for device_id in DEVICE_IDS:
            # Create mock data for the device
            data = {
                "device_id": device_id,
                "metric": random.randint(0, 100),
                "timestamp": int(time.time())
            }
            # Send data to Kafka
            producer.send(KAFKA_TOPIC, value=data)
            print(f"Sent data: {data}")

        # Wait for the specified interval before sending new data
        time.sleep(DATA_FREQUENCY)

if __name__ == "__main__":
    try:
        print("Starting IoT data simulator...")
        generate_data()
    except KeyboardInterrupt:
        print("Stopping simulator.")
