#!/bin/sh
set -e

# Helper function for formatted logging
log() {
    echo "[ENTRYPOINT] $(date '+%Y/%m/%d - %H:%M:%S') | $1"
    return 0
}

STORAGE_PATH="${STORAGE_PATH:-/storage/players-sqlite3.db}"

log "✔ Starting container..."

mkdir -p "$(dirname "$STORAGE_PATH")"

if [ ! -f "$STORAGE_PATH" ]; then
    log "⚠️ No existing database file found in volume."
    log "🗄️ Applying Alembic migrations to initialize the database..."
    alembic upgrade head
    log "✔ Migrations applied."
else
    log "✔ Existing database file found at $STORAGE_PATH."
fi

log "✔ Ready!"
log "🚀 Launching app..."
log "🔌 API endpoints | http://localhost:9000"
log "📚 Swagger UI    | http://localhost:9000/docs"
exec "$@"
