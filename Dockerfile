# Stage 1: Build stage (install Python dependencies, including TensorFlow)
FROM python:3.9-slim as builder

# Ensure we have system dependencies needed for compiling (if necessary)
# For just installing TensorFlow wheels, you typically only need the basics:
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image (lightweight)
FROM python:3.9-slim

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy application code
WORKDIR /app
COPY . .

# Expose the port for Cloud Run
EXPOSE 8080

# Start the Flask app
CMD ["python", "app.py"]
