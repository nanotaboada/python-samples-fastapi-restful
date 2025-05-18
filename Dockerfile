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

# Build all dependencies into wheels for reproducibility and speed
COPY --chown=root:root --chmod=644 requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/app/wheelhouse -r requirements.txt

# ------------------------------------------------------------------------------
# Stage 2: Runtime
# This stage creates the final, minimal image to run the application.
# ------------------------------------------------------------------------------
FROM python:3.13.3-slim-bookworm AS runtime

WORKDIR /app

# Install curl for health check
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Add metadata labels
LABEL org.opencontainers.image.title="🧪 RESTful API with Python 3 and FastAPI"
LABEL org.opencontainers.image.description="Proof of Concept for a RESTful API made with Python 3 and FastAPI"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/nanotaboada/python-samples-fastapi-restful"

# Copy metadata docs for container registries (e.g.: GitHub Container Registry)
COPY README.md          ./
COPY assets             ./assets

# Copy pre-built wheels from builder
COPY --from=builder     /app/wheelhouse    /app/wheelhouse

# Install dependencies
COPY requirements.txt   .
RUN pip install --no-cache-dir --no-index --find-links /app/wheelhouse -r requirements.txt && \
    rm -rf /app/wheelhouse

# Copy application source code
COPY main.py            ./
COPY database           ./database
COPY models             ./models
COPY routes             ./routes
COPY schemas            ./schemas
COPY services           ./services

# Copy entrypoint script and image-bundled, pre-seeded SQLite database
COPY --chmod=755        scripts/entrypoint.sh       ./entrypoint.sh
COPY --chmod=755        scripts/healthcheck.sh      ./healthcheck.sh
COPY --chmod=755        storage                     ./docker-compose

# Add non-root user and make volume mount point writable
RUN groupadd --system fastapi && \
    adduser --system --ingroup fastapi --disabled-password --gecos '' fastapi && \
    mkdir -p /storage && \
    chown fastapi:fastapi /storage

ENV PYTHONUNBUFFERED=1

# Drop privileges
USER fastapi

EXPOSE 9000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["./healthcheck.sh"]

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
