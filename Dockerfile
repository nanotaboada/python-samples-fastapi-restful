# ------------------------------------------------------------------------------
# Stage 1: Builder
# This stage resolves and pre-builds all dependency wheels for offline installation.
# No application source code is copied here — only pyproject.toml and uv.lock.
# ------------------------------------------------------------------------------
# Python version should match .python-version file (currently 3.13.3)
FROM python:3.13.3-slim-bookworm AS builder

WORKDIR /app

# Install system build tools required to compile native extensions (e.g. gevent, greenlet)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libffi-dev libssl-dev && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb

# Resolve and build all dependency wheels from pyproject.toml and uv.lock:
# uv export reads uv.lock to produce a pinned, reproducible dependency list;
# pip wheel compiles each resolved package into a .whl file for offline installation
COPY --chown=root:root --chmod=644 pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv==0.10.1 --quiet && \
    uv export --frozen --no-dev --no-hashes | pip wheel --no-cache-dir --wheel-dir=/app/wheelhouse -r /dev/stdin

# ------------------------------------------------------------------------------
# Stage 2: Runtime
# This stage creates the final, minimal image to run the application.
# ------------------------------------------------------------------------------
# Python version should match .python-version file (currently 3.13.3)
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

# Copy pre-built wheels from builder
COPY --from=builder     /app/wheelhouse/            /app/wheelhouse/

# Install all pre-built wheels from the builder stage; no network access required
RUN pip install --no-cache-dir --no-index --find-links /app/wheelhouse /app/wheelhouse/*.whl && \
    rm -rf /app/wheelhouse

# Copy application source code
COPY main.py            ./
COPY alembic.ini        ./
COPY alembic/           ./alembic/
COPY databases/         ./databases/
COPY models/            ./models/
COPY routes/            ./routes/
COPY schemas/           ./schemas/
COPY services/          ./services/
COPY tools/             ./tools/

# Copy entrypoint and healthcheck scripts
COPY --chmod=755        scripts/entrypoint.sh       ./entrypoint.sh
COPY --chmod=755        scripts/healthcheck.sh      ./healthcheck.sh

# Add non-root user and make volume mount point writable
# Avoids running the container as root (see: https://rules.sonarsource.com/docker/RSPEC-6504/)
RUN adduser --system --disabled-password --group fastapi && \
    mkdir -p /storage && \
    chown fastapi:fastapi /storage

ENV PYTHONUNBUFFERED=1

USER fastapi

EXPOSE 9000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["./healthcheck.sh"]

ENTRYPOINT ["./entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
