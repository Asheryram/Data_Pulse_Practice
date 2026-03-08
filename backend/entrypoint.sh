#!/bin/bash

echo "==> Running migrations..."
python manage.py makemigrations authentication datasets rules checks reports scheduling
python manage.py migrate

echo "==> Seeding default users..."
python manage.py seed_users || true

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn..."
exec gunicorn datapulse.wsgi:application -c gunicorn.conf.py
