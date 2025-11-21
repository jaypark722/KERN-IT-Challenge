#!/bin/bash
set -e

echo "Waiting for database..."
while ! pg_isready -h db -U timekeeper; do
    sleep 1
done
echo "Database is ready!"

echo "Running database migrations..."
flask db upgrade

echo "Starting Flask application..."
exec python run.py
