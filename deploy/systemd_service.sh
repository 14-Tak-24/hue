#!/bin/bash
# Systemd service installation for Tiapma'atzu API Server
# Run with sudo for production deployment

SERVICE_NAME="tiapmaatzu-api"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
PROJECT_DIR="/Users/AkshuN/Desktop/Hue"
USER=$(whoami)

echo "Installing Tiapma'atzu API Server as systemd service"
echo "===================================================="

# Create systemd service file
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Tiapma'atzu API Server
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn -c $PROJECT_DIR/deploy/gunicorn_config.py api_server:app
Restart=always
RestartSec=10
StandardOutput=append:$PROJECT_DIR/logs/systemd.log
StandardError=append:$PROJECT_DIR/logs/systemd_error.log

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable service
echo "Enabling service..."
sudo systemctl enable $SERVICE_NAME

echo "Service installed successfully!"
echo "To start: sudo systemctl start $SERVICE_NAME"
echo "To stop: sudo systemctl stop $SERVICE_NAME"
echo "To check status: sudo systemctl status $SERVICE_NAME"
echo "To view logs: sudo journalctl -u $SERVICE_NAME -f"