FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /SmartHospital

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc libjpeg-dev zlib1g-dev libfreetype6-dev libwebp-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /vol/static /vol/media

EXPOSE 8001

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --no-input --clear && gunicorn SmartHospital.wsgi:application --bind 0.0.0.0:8001 --workers 3"]

