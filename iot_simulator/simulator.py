import json
import time
import random
import sqlite3
from kafka import KafkaProducer
from config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, DEVICE_IDS, DATA_FREQUENCY

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Database connection setup
DB_FILE = 'iot_data.db'  # SQLite database file

def setup_database():
    """Create the database and the table if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS iot_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            metric INTEGER NOT NULL,
            timestamp INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def store_in_database(data):
    """Insert the data into the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO iot_data (device_id, metric, timestamp)
        VALUES (?, ?, ?)
    ''', (data['device_id'], data['metric'], data['timestamp']))
    conn.commit()
    conn.close()

def generate_data():
    """Generates random data for each device, stores it in SQLite, and sends it to Kafka."""
    while True:
        for device_id in DEVICE_IDS:
            # Create mock data for the device
            data = {
                "device_id": device_id,
                "metric": random.randint(0, 100),
                "timestamp": int(time.time())
            }
            # Store data in SQLite
            store_in_database(data)

            # Send data to Kafka
            producer.send(KAFKA_TOPIC, value=data)
            print(f"Sent and stored data: {data}")

        # Wait for the specified interval before sending new data
        time.sleep(DATA_FREQUENCY)

if __name__ == "__main__":
    try:
        print("Setting up the database...")
        setup_database()
        print("Starting IoT data simulator...")
        generate_data()
    except KeyboardInterrupt:
        print("Stopping simulator.")
