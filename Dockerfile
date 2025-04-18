# Stage 1: Base image to install dependencies
FROM python:3.9-slim AS build

WORKDIR /app

# Install build dependencies if any are needed (optional)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy only app files after installing dependencies
COPY . .

# Stage 2: Create a minimal runtime image
FROM python:3.9-slim AS runtime

# Create non-root user
RUN useradd -m myuser

WORKDIR /app

# Copy installed packages from build stage
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=build /app /app

# Set permissions (optional)
RUN chown -R myuser:myuser /app

# Switch to non-root user
USER myuser

EXPOSE 9000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
