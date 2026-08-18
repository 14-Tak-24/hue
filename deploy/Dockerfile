FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY api_server.py .
COPY deploy/gunicorn_config.py ./deploy/

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV API_PORT=8000
ENV API_DEBUG=False

# Run with Gunicorn
CMD ["gunicorn", "-c", "deploy/gunicorn_config.py", "api_server:app"]