from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import os

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .getOrCreate()

# Define schema for incoming JSON data
schema = StructType([
    StructField("device_id", StringType(), True),
    StructField("metric", IntegerType(), True),
    StructField("timestamp", IntegerType(), True)
])

# Read data from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .load()

# Parse the JSON data and select required columns
json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Write the processed data to the console for testing
query = json_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
