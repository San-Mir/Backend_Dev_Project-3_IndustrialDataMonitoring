from kafka import KafkaProducer
import json
import time
import random
import six

def produce_data():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    while True:
        data = {
            "metric": random.randint(1, 100),
            "timestamp": int(time.time())
        }
        producer.send('sensor_data', value=data)
        print(f"Sent: {data}")
        time.sleep(2)

if __name__ == "__main__":
    produce_data()
