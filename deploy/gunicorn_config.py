"""
Gunicorn configuration for Tiapma'atzu API Server
Production WSGI server configuration
"""

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Process naming
proc_name = "tiapmaatzu_api"

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process management
daemon = False
pidfile = "logs/gunicorn.pid"
umask = 0o007
user = None
group = None
tmp_upload_dir = None

# Server mechanics
sendfile = True
reuse_port = True
chdir = "/app"
raw_env = [
    'FIREBASE_SERVICE_ACCOUNT_KEY=/app/tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json',
    'API_PORT=8000',
    'API_DEBUG=False'
]

# SSL (if using HTTPS)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'