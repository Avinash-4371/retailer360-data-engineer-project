# Use Python 3.12 slim image to match your local environment
FROM python:3.12-slim

# Install build tools (needed for some Python packages like pandas/pyarrow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (better for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code
COPY src/ ./src/

# Set working directory to src
WORKDIR /app/src

# Ensure Python can import from src
ENV PYTHONPATH=/app/src

# Run your pipeline
CMD ["python", "main.py"]
