#!/bin/bash
# Production startup script for Tiapma'atzu API Server using Gunicorn

echo "Starting Tiapma'atzu API Server (Production)"
echo "=============================================="

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Start server with Gunicorn
echo "Starting Gunicorn production server on port 5000..."
gunicorn -c deploy/gunicorn_config.py api_server:app