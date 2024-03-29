# Use an official Python runtime as a parent image
FROM python:3.11-alpine AS builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk update && \
    apk add --no-cache build-base mysql-dev

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Collect static files and run Django migrations
RUN python manage.py collectstatic --noinput && \
    python manage.py migrate

# Use a lightweight base image for the runtime environment
FROM python:3.11-alpine

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk update && \
    apk add --no-cache libpq

# Set the working directory in the container
WORKDIR /app

# Copy the built static files and migrations from the builder stage
COPY --from=builder /app .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
