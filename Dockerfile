# Use official Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create directories in case not exist in image
RUN mkdir -p data logs

# Ensure output is sent to terminal
ENV PYTHONUNBUFFERED=1

# Run scheduler when container starts
CMD ["python", "scheduler.py"]
