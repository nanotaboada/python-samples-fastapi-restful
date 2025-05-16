#!/bin/bash
set -e

IMAGE_DATABASE_FILE_PATH="/app/docker-compose/players-sqlite3.db"
VOLUME_DATABASE_FILE_PATH="/sqlite3-db/players-sqlite3.db"

echo "✔ Starting container..."

if [ ! -f "$VOLUME_DATABASE_FILE_PATH" ]; then
    echo "⚠️ No existing database file found in volume."
    if [ -f "$IMAGE_DATABASE_FILE_PATH" ]; then
        echo "Copying database file to writable volume..."
        cp "$IMAGE_DATABASE_FILE_PATH" "$VOLUME_DATABASE_FILE_PATH"
        echo "✔ Database initialized at $VOLUME_DATBASE_FILE_PATH"
    else
        echo "⚠️ Database file missing at $IMAGE_DATABASE_FILE_PATH"
        exit 1
    fi
else
    echo "✔ Existing database file found. Skipping seed copy."
fi

echo "✔ Ready!"
echo "🚀 Launching app..."
exec "$@"
