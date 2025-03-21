# Stage 1: Build stage using Alpine for dependency installation
FROM python:3.9-alpine AS builder
WORKDIR /app
# Copy only the dependency file first to leverage caching
COPY requirements.txt .
# Install build dependencies required to compile any native extensions
RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image using a clean Alpine image
FROM python:3.9-alpine
WORKDIR /app
# Copy installed Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
# Copy the rest of the application code
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
