#!/usr/bin/env bash
set -e

# wait for Postgres
until nc -z db 5432; do
  echo "Waiting for database..."
  sleep 1
done

# run migrations & collectstatic
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# hand off to CMD
exec "$@"

