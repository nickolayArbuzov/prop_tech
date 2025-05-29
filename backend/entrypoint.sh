#!/bin/bash
set -e

echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  echo "Still waiting..."
  sleep 1
done

echo "PostgreSQL is up — applying Alembic migrations"
alembic upgrade head

echo "Running seed.py"
python seed.py

echo "Starting FastAPI app"
exec uvicorn main:app --reload --host 0.0.0.0 --port 5000