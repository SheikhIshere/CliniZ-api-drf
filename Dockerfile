# Base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY App/ ./App/

# Set workdir to App
WORKDIR /app/App

# Collect static files (optional)
RUN mkdir -p static staticfiles

# Copy wait script
COPY wait_for_db.sh /app/wait_for_db.sh
RUN chmod +x /app/wait_for_db.sh

# Default command
CMD ["/app/wait_for_db.sh"]
