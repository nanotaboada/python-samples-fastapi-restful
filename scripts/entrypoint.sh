#!/bin/bash
set -e

echo "Starting container..."
echo "Database migrations will be applied by the application on startup."
echo "Launching app..."
exec "$@"
