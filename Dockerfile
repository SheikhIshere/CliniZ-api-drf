FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    echo "Migrations completed"

# Copy the entire project
COPY . .

# Set the working directory to where manage.py is actually located
WORKDIR /app/App

# Run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]