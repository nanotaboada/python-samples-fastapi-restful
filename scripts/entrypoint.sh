#!/bin/bash
set -e

IMAGE_STORAGE_PATH="/app/hold/players-sqlite3.db"
VOLUME_STORAGE_PATH="/storage/players-sqlite3.db"

echo "✔ Starting container..."

if [[ ! -f "$VOLUME_STORAGE_PATH" ]]; then
    echo "⚠️ No existing database file found in volume."
    if [[ -f "$IMAGE_STORAGE_PATH" ]]; then
        echo "Copying database file to writable volume..."
        cp "$IMAGE_STORAGE_PATH" "$VOLUME_STORAGE_PATH"
        echo "✔ Database initialized at $VOLUME_STORAGE_PATH"
    else
        echo "⚠️ Database file missing at $IMAGE_STORAGE_PATH"
        exit 1
    fi
else
    echo "✔ Existing database file found. Skipping seed copy."
fi

echo "🔄 Running seed scripts to ensure schema is up to date..."
python /app/tools/seed_001_starting_eleven.py --db-path "$VOLUME_STORAGE_PATH"
python /app/tools/seed_002_substitutes.py --db-path "$VOLUME_STORAGE_PATH"

echo "✔ Ready!"
echo "🚀 Launching app..."
exec "$@"
