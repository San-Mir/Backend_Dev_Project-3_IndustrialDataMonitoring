FROM python:3.9-slim 

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application code into the container
COPY . /app

# Install Python dependencies (replace with your requirements file if available)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Expose any required ports (e.g., 8000 for Django or Kafka)
EXPOSE 8000

# Default command to run your application
# Adjust the command for your specific use case
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
