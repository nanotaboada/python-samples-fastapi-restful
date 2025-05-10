# - Stage 1: Build dependencies into wheels ------------------------------------

    FROM python:3.13.3-slim-bookworm AS build

    WORKDIR /app

    # Install system build tools needed to compile Python packages with native
    # extensions, and clean up afterward to reduce image size.
    RUN apt-get update && \
        apt-get install -y --no-install-recommends build-essential gcc libffi-dev libssl-dev && \
        rm -rf /var/lib/apt/lists/* && \
        rm -rf /var/cache/apt/archives/*.deb

    # Pre-build all third-party dependencies into wheel files. This enables faster,
    # more reliable installation later without relying on network access.
    COPY requirements.txt .
    RUN pip wheel --no-cache-dir --wheel-dir=/app/wheelhouse -r requirements.txt

# - Stage 2: Runtime image ----------------------------------------------------

    FROM python:3.13.3-slim-bookworm AS runtime

    WORKDIR /app

    # Install runtime dependencies from prebuilt wheels (no network access).
    # This improves build speed and avoids dependency drift.
    COPY requirements.txt .
    COPY --from=build /app/wheelhouse /app/wheelhouse
    RUN pip install --no-cache-dir --no-index --find-links /app/wheelhouse -r requirements.txt && \
        rm -rf /app/wheelhouse

    # Copy only runtime-relevant application code (excluding tests and tooling)
    COPY models ./models
    COPY routes ./routes
    COPY schemas ./schemas
    COPY services ./services
    COPY data ./data
    COPY main.py .

    # Copy README and assets needed for GHCR package page metadata
    COPY README.md ./
    COPY assets ./assets

    # Add a non-root user for better container security
    RUN adduser --disabled-password --gecos '' fastapi && \
        chown -R fastapi:fastapi /app
    USER fastapi

    # Ensure logs and errors appear in Docker logs immediately
    ENV PYTHONUNBUFFERED=1

    # Expose FastAPI default port
    EXPOSE 9000

    # Start the FastAPI application using Uvicorn ASGI server
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
