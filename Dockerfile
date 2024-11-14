# Use a base image with Java, required for Spark
FROM openjdk:11-jre-slim
# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*
# Install PySpark and any other required Python packages
RUN pip3 install pyspark
# Set the working directory
WORKDIR /app
# Copy your application code (optional if you have specific code to run)
COPY . /app
# Default command to start a PySpark shell (you can change this if you have an app to run)
CMD ["pyspark", "--master", "local[*]"]