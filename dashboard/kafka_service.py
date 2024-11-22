from kafka import KafkaConsumer
import json

def fetch_kafka_messages(limit=10):
    """
    Fetch a limited number of messages from the Kafka topic.
    """
    consumer = KafkaConsumer(
        'sensor_data',
        bootstrap_servers=['localhost:9092'],
        group_id='django-group',
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    messages = []

    for message in consumer:
        messages.append(message.value)  # Collect message values
        if len(messages) >= limit:     # Stop after reaching the limit
            break

    consumer.close()
    return messages

if __name__ == "__main__":
    messages = fetch_kafka_messages(limit=4)
    print("Fetched Messages:")
    for msg in messages:
        print(msg)