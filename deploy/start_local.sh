#!/bin/bash
# Local development startup script for Tiapma'atzu API Server

echo "Starting Tiapma'atzu API Server (Local Development)"
echo "================================================"

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create logs directory
mkdir -p logs

# Start server with Flask development server
echo "Starting Flask development server on port 5000..."
python api_server.py