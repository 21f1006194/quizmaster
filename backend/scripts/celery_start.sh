#!/bin/bash

# Set project directory
dirname=$(realpath "$(dirname "$0")/..")
cd "$dirname"

echo "Starting Celery Worker with Beat..."

# Start worker with beat in single process
celery -A celery_worker.celery_app worker --loglevel=info --concurrency=4 --beat | tee worker_with_beat.log &
WORKER_PID=$!
echo "Worker with Beat PID: $WORKER_PID"

# Stopping all processes
trap "echo 'Stopping...'; kill $WORKER_PID; celery -A app.celery_app:celery_app purge -f; exit" INT

wait $WORKER_PID