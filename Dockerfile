# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Create a non-root user
RUN useradd -m myuser

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
# Make sure to add a .dockerignore file to exclude sensitive files
COPY . /app/

# Change to the non-root user
USER myuser

# Expose the FastAPI app's port
EXPOSE 9000

# Run the FastAPI app using uvicorn when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
