# Tiapma'atzu API Server Deployment Guide

## Overview
This guide provides multiple deployment options for the Tiapma'atzu Python API Server, which serves as a free alternative to Firebase Cloud Functions.

## Prerequisites
- Python 3.11+
- Firebase service account key (`tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json`)
- Virtual environment activated

## Deployment Options

### 1. Local Development (Quick Start)
**Best for:** Development and testing

```bash
# Make script executable
chmod +x deploy/start_local.sh

# Start server
./deploy/start_local.sh
```

The server will run on `http://localhost:5000`

### 2. Local Production with Gunicorn
**Best for:** Local production-like environment

```bash
# Install gunicorn
source venv/bin/activate
pip install gunicorn

# Make script executable
chmod +x deploy/start_production.sh

# Start server
./deploy/start_production.sh
```

### 3. Systemd Service (Linux/Production)
**Best for:** Persistent production server

```bash
# Make script executable
chmod +x deploy/systemd_service.sh

# Install service (requires sudo)
sudo ./deploy/systemd_service.sh

# Start service
sudo systemctl start tiapmaatzu-api

# Check status
sudo systemctl status tiapmaatzu-api

# View logs
sudo journalctl -u tiapmaatzu-api -f
```

### 4. Docker Container
**Best for:** Containerized deployment

```bash
# Build image
docker build -t tiapmaatzu-api .

# Run container
docker run -p 5000:5000 \
  -v $(pwd)/tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json:/app/tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json \
  -v $(pwd)/logs:/app/logs \
  tiapmaatzu-api

# Or use docker-compose
docker-compose up -d
```

### 5. Render (Free Cloud Platform)
**Best for:** Free cloud hosting

1. Create account at [render.com](https://render.com)
2. Connect GitHub repository
3. Create new Web Service
4. Use `deploy/render.yaml` configuration
5. Set environment variable `FIREBASE_SERVICE_ACCOUNT_KEY` in Render dashboard
6. Deploy

### 6. Railway (Free Cloud Platform)
**Best for:** Simple free cloud hosting

1. Create account at [railway.app](https://railway.app)
2. Connect GitHub repository
3. Use `deploy/railway.toml` configuration
4. Set environment variables in Railway dashboard
5. Deploy

### 7. Heroku (Free Tier Available)
**Best for:** Established cloud platform

```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create tiapmaatzu-api

# Set buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set API_DEBUG=false
heroku config:set API_PORT=5000

# Add Firebase key (add as config var)
heroku config:set FIREBASE_SERVICE_ACCOUNT_KEY="$(cat tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json)"

# Deploy
git push heroku main
```

## API Endpoints

### Health Check
- `GET /health` - Server health status

### Soul Management
- `GET /api/souls` - Get all souls
- `GET /api/souls/<soul_id>` - Get specific soul
- `GET /api/souls/archetype/<archetype>` - Get souls by archetype
- `GET /api/souls/rarity/<rarity>` - Get souls by rarity
- `GET /api/souls/platform/<platform>` - Get souls by platform
- `GET /api/souls/search?q=<query>` - Search souls
- `GET /api/souls/statistics` - Get souls statistics
- `GET /api/souls/network` - Get soul network map

### Financial Operations
- `GET /api/financial/summary` - Get financial summary
- `GET /api/financial/transactions` - Get all transactions
- `POST /api/financial/tributes` - Add tribute transaction
- `GET /api/financial/cash-flow?days=30` - Get cash flow analysis
- `GET /api/financial/forecast?days=90` - Get financial forecast
- `GET /api/financial/risk` - Get financial risk assessment
- `GET /api/financial/diversification` - Get revenue diversification
- `GET /api/financial/goals` - Get financial goals status

### Analytics
- `GET /api/analytics/dashboard` - Get analytics dashboard
- `GET /api/analytics/trends?days=30` - Get trend analysis
- `GET /api/analytics/comparison?days=30` - Get comparative analytics
- `GET /api/analytics/anomalies` - Get anomaly detection
- `GET /api/analytics/soul-performance` - Get soul performance
- `GET /api/analytics/archetype` - Get archetype performance
- `GET /api/analytics/network` - Get network analysis
- `GET /api/analytics/export?format=json` - Export analytics

### Firestore Sync
- `POST /api/firestore/sync` - Sync souls to Firestore
- `GET /api/firestore/souls` - Get souls from Firestore

## Testing the Deployment

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test souls endpoint
curl http://localhost:5000/api/souls

# Test financial summary
curl http://localhost:5000/api/financial/summary

# Test analytics dashboard
curl http://localhost:5000/api/analytics/dashboard
```

## Security Considerations

1. **HTTPS:** Use HTTPS in production (configure SSL certificates)
2. **Authentication:** Add API key authentication or OAuth
3. **Rate Limiting:** Implement rate limiting for production
4. **Firewall:** Configure firewall rules
5. **Environment Variables:** Never commit secrets to repository
6. **Firebase Key:** Keep service account key secure

## Monitoring

### Logs
- Application logs: `logs/access.log`, `logs/error.log`
- Systemd logs: `sudo journalctl -u tiapmaatzu-api -f`
- Docker logs: `docker logs tiapmaatzu-api`

### Health Monitoring
- Health check endpoint: `/health`
- Monitor component status
- Set up uptime monitoring (UptimeRobot, Pingdom)

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

### Firebase Connection Issues
- Verify service account key path
- Check Firebase project permissions
- Ensure network connectivity

### Import Errors
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple instances
- Use container orchestration (Kubernetes)

### Vertical Scaling
- Increase server resources
- Adjust Gunicorn worker count
- Optimize database queries

## Recommended Deployment Choice

**For immediate free deployment:** Use Render or Railway
**For local development:** Use Flask development server
**For production server:** Use Systemd service with Nginx reverse proxy
**For containerized deployment:** Use Docker

## Support

For issues, visit: https://devin.ai/support