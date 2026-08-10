#!/bin/sh
set -e

echo "Waiting for database..."
until python school/manage.py migrate --check >/dev/null 2>&1 || python -c "
import sys, time, os
import psycopg2
url = os.environ.get('DATABASE_URL', '')
" 2>/dev/null; do
  sleep 1
done

echo "Applying database migrations..."
python school/manage.py migrate --noinput

echo "Collecting static files..."
python school/manage.py collectstatic --noinput --clear || true

echo "Starting Django development server..."
exec python school/manage.py runserver 0.0.0.0:8000