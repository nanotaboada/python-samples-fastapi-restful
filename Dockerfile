# - Stage 1: Builder -----------------------------------------------------------

FROM python:3.13.3-slim-bookworm AS builder
WORKDIR /app

# Install system build tools for packages with native extensions
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb

# Pre-build all dependencies into wheels for reproducibility and speed
COPY --chown=root:root --chmod=644 requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir=/app/wheelhouse -r requirements.txt

# - Stage 2: Runtime -----------------------------------------------------------

FROM python:3.13.3-slim-bookworm AS runtime
WORKDIR /app

# Metadata labels
LABEL org.opencontainers.image.title="🧪 RESTful API with Python 3 and FastAPI"
LABEL org.opencontainers.image.description="Proof of Concept for a RESTful API made with Python 3 and FastAPI"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.source="https://github.com/nanotaboada/python-samples-fastapi-restful"

# Copy prebuilt wheels and install dependencies
COPY --from=builder --chown=root:root --chmod=755 /app/wheelhouse /app/wheelhouse
COPY --chown=root:root --chmod=644 requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links /app/wheelhouse -r requirements.txt && \
    rm -rf /app/wheelhouse

# Copy application code (read-only)
COPY --chown=root:root --chmod=644 main.py          ./
COPY --chown=root:root --chmod=755 models           ./models
COPY --chown=root:root --chmod=755 routes           ./routes
COPY --chown=root:root --chmod=755 schemas          ./schemas
COPY --chown=root:root --chmod=755 services         ./services
COPY --chown=root:root --chmod=755 data             ./data

# Copy metadata for GHCR (read-only)
COPY --chown=root:root --chmod=644 README.md        ./
COPY --chown=root:root --chmod=755 assets           ./assets

# Create a non-root user for running the app
RUN adduser --system --disabled-password --gecos '' fastapi

# Drop privileges
USER fastapi

# Logging output immediately
ENV PYTHONUNBUFFERED=1

EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
