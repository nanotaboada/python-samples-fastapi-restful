#!/bin/bash
set -e

echo "Starting container..."
echo "Applying database migrations..."
alembic upgrade head
echo "Database migrations applied."
echo "Launching app..."
exec "$@"
