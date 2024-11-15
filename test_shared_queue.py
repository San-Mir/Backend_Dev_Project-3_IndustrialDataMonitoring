import time
from dashboard.spark_consumer import shared_queue

# Function to test shared_queue
def test_shared_queue():
    print("Waiting for data in shared_queue...")
    while True:
        if not shared_queue.empty():
            # Retrieve data from the queue
            data = shared_queue.get()
            print(f"Data retrieved from queue: {data}")
        else:
            print("No data in queue, waiting...")
        time.sleep(1)  # Avoid busy-waiting

if __name__ == "__main__":
    test_shared_q