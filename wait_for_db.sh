#!/bin/sh
# wait_for_db.sh

echo "Waiting for PostgreSQL..."
until nc -z $DB_HOST $DB_PORT; do
  sleep 2
done

echo "PostgreSQL is up — running migrations"
python manage.py makemigrations
python manage.py migrate

echo "Starting server"
exec python manage.py runserver 0.0.0.0:8000
