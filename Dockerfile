# ------------------------------------------------------------------------------
# Stage 1: Builder
# This stage builds the application and its dependencies.
# ------------------------------------------------------------------------------
FROM python:3.13.3-slim-bookworm AS builder
WORKDIR /app

# Install system build tools for packages with native extensions
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb

# Pre-build all dependencies into wheels for reproducibility and speed
COPY --chown=root:root --chmod=644 requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/app/wheelhouse -r requirements.txt

# ------------------------------------------------------------------------------
# Stage 2: Runtime
# This stage creates the final, minimal image to run the application.
# ------------------------------------------------------------------------------
FROM python:3.13.3-slim-bookworm AS runtime
WORKDIR /app

# Metadata labels
LABEL org.opencontainers.image.title="🧪 RESTful API with Python 3 and FastAPI"
LABEL org.opencontainers.image.description="Proof of Concept for a RESTful API made with Python 3 and FastAPI"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/nanotaboada/python-samples-fastapi-restful"

# Copy prebuilt wheels and install dependencies
COPY --chown=root:root --chmod=644 requirements.txt .
COPY --from=builder --chown=root:root --chmod=755 /app/wheelhouse /app/wheelhouse
RUN pip install --no-cache-dir --no-index --find-links /app/wheelhouse -r requirements.txt && \
    rm -rf /app/wheelhouse

# Copy application code (read-only)
COPY --chown=root:root --chmod=644      main.py     ./
COPY --chown=root:root --chmod=755      database    ./database
COPY --chown=root:root --chmod=755      models      ./models
COPY --chown=root:root --chmod=755      routes      ./routes
COPY --chown=root:root --chmod=755      schemas     ./schemas
COPY --chown=root:root --chmod=755      services    ./services

# Copy metadata for GHCR (read-only)
COPY --chown=root:root --chmod=644      README.md   ./
COPY --chown=root:root --chmod=755      assets      ./assets

# Copy entrypoint sctipt and SQLite database
COPY --chown=root:root --chmod=755      scripts/entrypoint.sh       ./entrypoint.sh
COPY --chown=root:root --chmod=755      sqlite3-db                  ./docker-compose

# Create non-root user and make volume mount point writable
RUN groupadd --system fastapi && \
    adduser --system --ingroup fastapi --disabled-password --gecos '' fastapi && \
    mkdir -p /sqlite3-db && \
    chown fastapi:fastapi /sqlite3-db

# Drop privileges
USER fastapi

# Logging output immediately
ENV PYTHONUNBUFFERED=1

EXPOSE 9000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
