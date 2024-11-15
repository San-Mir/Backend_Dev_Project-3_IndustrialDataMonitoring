# Shared queue
from queue import Queue
shared_queue = Queue()

import findspark
findspark.init() 

import os 
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, lit
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType


# Set up Spark environment
os.environ["JAVA_HOME"] = "C:\\Program Files\\Java\\jdk8u432-b06"  # Replace with the actual path found
os.environ["PATH"] += os.pathsep + os.path.join(os.environ["JAVA_HOME"], "bin")
os.environ["SPARK_HOME"] = "C:\\spark"
os.environ["HADOOP_HOME"] = "C:\\hadoop"  # Ensure winutils.exe is in C:\hadoop\bin
os.environ["SPARK_USER"] = "Hassan"  # Replace with actual username
os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
    .config("spark.hadoop.security.authentication", "simple") \
    .getOrCreate()

# Define schema for incoming JSON data
schema = StructType([
    StructField("device_id", StringType(), True),
    StructField("metric", IntegerType(), True),
    StructField("timestamp", TimestampType(), True)  # Use TimestampType if needed for date-time parsing
])

# Read data from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .load()

# Parse the JSON data and select required columns
json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*").withColumn("hello_world", lit("hello world"))

# Write to the queue
def write_to_queue(batch_df, batch_id):
    # Collect data from the DataFrame and put it in the shared queue
    data = batch_df.toJSON().collect()
    for record in data:
        shared_queue.put(record)


# Write the processed data to the console for testing
query = json_df.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_queue)\
    .format('console')\
    .start()

query.awaitTermination()

# while not shared_queue.empty():
#     print(f'data: ', {shared_queue.get()})