# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install netcat for the wait script and other essential dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # For postgres
    postgresql-client \
    libpq-dev \
    # For weasyprint and other dependencies
    build-essential \
    python3-dev \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-dev \
    libharfbuzz0b \
    libfribidi0 \
    libfontconfig1 \
    shared-mime-info \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# This will be handled by the docker-compose command now
# RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000
