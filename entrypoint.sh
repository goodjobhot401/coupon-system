#!/bin/sh

echo "🔥 Starting container: $HOSTNAME"

if [ "$BOOTSTRAP" = "true" ]; then
  echo "Running DB bootstrap..."
  python /app/src/database/bootstrap.py
fi

echo "Launching FastAPI with Gunicorn..."
exec gunicorn -k uvicorn.workers.UvicornWorker main:app -w 2 -b 0.0.0.0:8000

