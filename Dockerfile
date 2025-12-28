# Use slim Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Set working directory to where manage.py is located
WORKDIR /app/App

# Ensure static directories exist
RUN mkdir -p static staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start the server at container runtime
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
