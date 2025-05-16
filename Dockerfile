# ------------------------------------------------------------------------------ 
# Stage 1: Builder 
# ------------------------------------------------------------------------------ 
    FROM python:3.13.3-slim-bookworm AS builder 
    WORKDIR /app 
    
    # Install build dependencies 
    RUN apt-get update && \
        apt-get install -y --no-install-recommends \
            build-essential \
            gcc \
            libffi-dev \
            libssl-dev && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/* 
    
    # Copy and pre-build Python dependencies 
    COPY requirements.txt . 
    RUN pip install --upgrade pip && \
        pip wheel --no-cache-dir --wheel-dir=/app/wheelhouse -r requirements.txt 
    
    # ------------------------------------------------------------------------------ 
    # Stage 2: Runtime 
    # ------------------------------------------------------------------------------ 
    FROM python:3.13.3-slim-bookworm AS runtime 
    WORKDIR /app 
    
    # Metadata 
    LABEL org.opencontainers.image.title="🧪 RESTful API with Python 3 and FastAPI" 
    LABEL org.opencontainers.image.description="Proof of Concept for a RESTful API made with Python 3 and FastAPI" 
    LABEL org.opencontainers.image.licenses="MIT" 
    LABEL org.opencontainers.image.source="https://github.com/nanotaboada/python-samples-fastapi-restful" 
    
    # Install runtime dependencies 
    COPY requirements.txt . 
    COPY --from=builder /app/wheelhouse /app/wheelhouse 
    RUN pip install --no-cache-dir --no-index --find-links=/app/wheelhouse -r requirements.txt && \
        rm -rf /app/wheelhouse 
    
    # Copy app code 
    COPY main.py . 
    COPY database/ ./database/ 
    COPY models/ ./models/ 
    COPY routes/ ./routes/ 
    COPY schemas/ ./schemas/ 
    COPY services/ ./services/ 
    COPY README.md . 
    COPY assets/ ./assets/ 
    
    # Copy startup script and SQLite DB seed 
    COPY scripts/entrypoint.sh ./entrypoint.sh 
    RUN chmod +x ./entrypoint.sh
    COPY sqlite3-db ./docker-compose 
    
    # Create non-root user and make volume writable 
    RUN groupadd --system fastapi && \
        useradd --system --gid fastapi --create-home fastapi && \
        mkdir -p /sqlite3-db && \
        chown -R fastapi:fastapi /app /sqlite3-db 
    
    # Configure environment 
    ENV PYTHONUNBUFFERED=1 
    EXPOSE 9000 
    
    ENTRYPOINT ["./entrypoint.sh"] 
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
    
    # 👇Run with not root user
    USER fastapi
    
