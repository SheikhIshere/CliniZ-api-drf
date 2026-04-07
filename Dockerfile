FROM python:3.12-slim

WORKDIR /app

# Install psycopg2 dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY App/ ./App/
WORKDIR /app/App

# Expose port
EXPOSE 8013

# Run Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8013"]
