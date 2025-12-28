FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY App/ ./App

# Run migrations
RUN python3 App/manage.py makemigrations && \
    python3 App/manage.py migrate

# Run server
CMD ["python3", "App/manage.py", "runserver", "0.0.0.0:8000"]
