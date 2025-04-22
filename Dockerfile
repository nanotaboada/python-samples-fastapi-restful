# Stage 1: Build
FROM python:3.12-slim-bookworm AS build

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Runtime
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY models ./models
COPY routes ./routes
COPY schemas ./schemas
COPY services ./services
COPY data ./data
COPY main.py .

# Add non-root 'fastapi' user (optional for hardening)
RUN adduser --disabled-password --gecos '' fastapi \
    && chown -R fastapi:fastapi /app
USER fastapi

EXPOSE 9000
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
