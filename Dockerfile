# - Stage 1 --------------------------------------------------------------------

    FROM python:3.12-slim-bookworm AS build

    WORKDIR /app

    # Install build tools needed to compile some Python packages
    RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential gcc && \
        rm -rf /var/lib/apt/lists/*

    # Copy and build all required packages (with dependencies) into wheels
    COPY requirements.txt .
    RUN pip wheel --no-cache -r requirements.txt -w /app/wheelhouse

    # Copy full app source (not strictly needed in build stage unless building static assets)
    COPY . .

# - Stage 2 --------------------------------------------------------------------

    FROM python:3.12-slim-bookworm AS runtime

    WORKDIR /app

    # Only bring in requirements and prebuilt wheels from build stage
    COPY requirements.txt .
    COPY --from=build /app/wheelhouse /app/wheelhouse

    # Install app dependencies from local wheelhouse
    RUN pip install --no-cache-dir --no-index --find-links /app/wheelhouse -r requirements.txt

    # Copy only the necessary runtime source files
    COPY models ./models
    COPY routes ./routes
    COPY schemas ./schemas
    COPY services ./services
    COPY data ./data
    COPY main.py .

    # Add non-root user for security hardening
    RUN adduser --disabled-password --gecos '' fastapi && \
        chown -R fastapi:fastapi /app
    USER fastapi

    # Prevent Python from buffering stdout/stderr
    ENV PYTHONUNBUFFERED=1

    # Expose FastAPI port
    EXPOSE 9000

    # Start the FastAPI app with Uvicorn
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
