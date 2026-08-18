# Tiapma'atzu OS Deployment Guide

Complete deployment guide for the Tiapma'atzu autonomous business operating system.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Firebase Configuration](#firebase-configuration)
- [Monitoring and Maintenance](#monitoring-and-maintenance)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **OS**: macOS, Linux, or Windows with WSL2
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
- **Git**: For version control

### Required Accounts
- Firebase project with Firestore and Authentication enabled
- (Optional) PostgreSQL database hosting
- (Optional) Redis cache hosting
- (Optional) Container registry (Docker Hub, AWS ECR, etc.)

## Local Development Setup

### 1. Clone and Setup Repository

```bash
git clone <repository-url>
cd Hue
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment (if needed)
# Create .env file with VITE_API_URL=http://localhost:8000
```

### 4. Firebase Setup

```bash
# Download Firebase service account key from Firebase Console
# Place it in project root: tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json
# Update .env with: FIREBASE_SERVICE_ACCOUNT_KEY=tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json
```

### 5. Run Development Servers

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
python api_server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Access:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Health Check: http://localhost:8000/health

## Docker Deployment

### 1. Quick Start (Development)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 2. Production Deployment

```bash
# Build with production configuration
docker-compose -f docker-compose.yml up -d --build

# Scale services if needed
docker-compose up -d --scale api=3
```

### 3. Individual Service Deployment

**API Server Only:**
```bash
cd deploy
docker-compose up -d
```

**Frontend Only:**
```bash
# Uncomment frontend service in docker-compose.yml
docker-compose up -d frontend
```

### 4. Docker Management Commands

```bash
# View running containers
docker ps

# View logs for specific service
docker logs -f tiapmaatzu-api

# Restart service
docker-compose restart api

# Update and rebuild
docker-compose up -d --build

# Clean up everything
docker-compose down -v
```

## Production Deployment

### 1. Environment Configuration

Create production environment file:

```bash
# .env.production
API_PORT=8000
API_DEBUG=False
ENVIRONMENT=production

# Firebase
FIREBASE_SERVICE_ACCOUNT_KEY=/app/production-firebase-key.json

# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com
```

### 2. Firebase Production Setup

1. **Create Firebase Project:**
   - Go to Firebase Console
   - Create new project or use existing
   - Enable Firestore and Authentication

2. **Generate Service Account Key:**
   - Go to Project Settings > Service Accounts
   - Generate new private key
   - Save as `production-firebase-key.json`
   - **IMPORTANT**: Never commit this file to git

3. **Configure Firestore Rules:**
   - Set appropriate security rules in `firestore.rules`
   - Deploy rules: `firebase deploy --only firestore:rules`

### 3. Database Setup

**PostgreSQL Setup:**
```bash
# Using Docker
docker-compose up -d db

# Manual connection
docker exec -it hue-db psql -U hue -d hue_db

# Create tables (if needed)
# See database initialization scripts
```

**Redis Setup:**
```bash
# Using Docker
docker-compose up -d redis

# Test connection
docker exec -it hue-redis redis-cli ping
```

### 4. SSL/HTTPS Configuration

**Using Nginx:**
```bash
# Generate SSL certificates (Let's Encrypt)
certbot certonly --standalone -d your-domain.com

# Update nginx configuration with SSL paths
# Uncomment SSL section in deploy/nginx.conf
```

**Using Cloudflare:**
- Set up Cloudflare for your domain
- Enable SSL/TLS in Cloudflare dashboard
- Configure DNS records to point to your server

### 5. Platform-Specific Deployment

**Railway:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Render:**
```bash
# Use existing render.yaml configuration
# Connect repository to Render
# Configure environment variables in Render dashboard
```

**AWS:**
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t tiapmaatzu-api .
docker tag tiapmaatzu-api:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/tiapmaatzu-api:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/tiapmaatzu-api:latest
```

## Firebase Configuration

### Firestore Security Rules

Current rules in `firestore.rules`:
- Allows read/write for authenticated users
- Restricts access to souls collection
- Configure based on your security requirements

### Deployment

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Deploy Firebase configuration
firebase deploy

# Deploy specific services
firebase deploy --only firestore
firebase deploy --only hosting
firebase deploy --only functions
```

## Monitoring and Maintenance

### Health Checks

```bash
# API Health Check
curl http://localhost:8000/health

# Expected Response:
{
  "status": "healthy",
  "timestamp": "2026-08-17T19:03:33.504340",
  "firebase": true,
  "auth": true,
  "components": {
    "souls_manager": true,
    "cashinghouse": true,
    "financial_integration": true,
    "analytics": true
  }
}
```

### Log Management

```bash
# View API logs
docker logs -f tiapmaatzu-api

# View logs with timestamp
docker logs -t tiapmaatzu-api

# Export logs
docker logs tiapmaatzu-api > api-logs.txt
```

### Database Backups

```bash
# PostgreSQL Backup
docker exec hue-db pg_dump -U hue hue_db > backup.sql

# Restore Backup
docker exec -i hue-db psql -U hue hue_db < backup.sql

# Automated Backup Script
# See scripts/backup.sh
```

### Performance Monitoring

Key metrics to monitor:
- API response times
- Database query performance
- Firebase read/write operations
- Memory and CPU usage
- Error rates

## Troubleshooting

### Common Issues

**1. API Server Won't Start**
```bash
# Check port conflicts
lsof -i :8000

# Check logs
docker logs tiapmaatzu-api

# Verify environment variables
docker exec tiapmaatzu-api env
```

**2. Firebase Connection Issues**
```bash
# Verify service account key exists
ls -la tiapmaatzu-firebase-adminsdk-fbsvc-db8f709411.json

# Check Firebase initialization
curl http://localhost:8000/health

# Test Firebase connection manually
python -c "from firebase_admin import credentials, firestore; print('Firebase OK')"
```

**3. Frontend Build Errors**
```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check for TypeScript errors
npm run build
```

**4. Database Connection Issues**
```bash
# Test database connection
docker exec -it hue-db psql -U hue -d hue_db -c "SELECT 1;"

# Check database logs
docker logs hue-db

# Verify environment variables
echo $DATABASE_URL
```

**5. Docker Build Issues**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check disk space
docker system df
```

### Emergency Procedures

**Rollback Deployment:**
```bash
# Stop current deployment
docker-compose down

# Deploy previous version
git checkout <previous-commit-tag>
docker-compose up -d --build
```

**Database Recovery:**
```bash
# Stop application
docker-compose stop api

# Restore from backup
docker exec -i hue-db psql -U hue hue_db < backup.sql

# Restart application
docker-compose start api
```

**Firebase Rollback:**
```bash
# Rollback Firestore rules
firebase deploy --only firestore:rules --force

# Restore data from Firestore export
firebase firestore:import backup.firestore-export
```

## Security Best Practices

1. **Never commit sensitive files:**
   - Service account keys
   - Environment files
   - SSL certificates

2. **Use environment variables:**
   - All secrets via environment variables
   - Rotate keys regularly
   - Use different keys for dev/staging/prod

3. **Network security:**
   - Use HTTPS in production
   - Configure firewall rules
   - Limit database access

4. **Regular updates:**
   - Keep dependencies updated
   - Monitor security advisories
   - Apply security patches promptly

## Support and Resources

- **Documentation**: See project README and guides in `/docs`
- **Firebase Console**: https://console.firebase.google.com/
- **Issue Tracking**: Use project issue tracker
- **Emergency Contact**: [Add contact information]

## Appendix

### Quick Reference Commands

```bash
# Development
source venv/bin/activate && python api_server.py
cd frontend && npm run dev

# Docker
docker-compose up -d
docker-compose logs -f
docker-compose down

# Firebase
firebase deploy
firebase serve --only hosting

# Database
docker exec -it hue-db psql -U hue -d hue_db
docker exec hue-db pg_dump -U hue hue_db > backup.sql

# Monitoring
curl http://localhost:8000/health
docker stats
docker logs -f tiapmaatzu-api
```

### Configuration Files Reference

- `docker-compose.yml` - Main Docker orchestration
- `deploy/Dockerfile` - API server container
- `frontend/Dockerfile` - Frontend container
- `deploy/nginx.conf` - Nginx reverse proxy
- `deploy/gunicorn_config.py` - WSGI server configuration
- `.env.example` - Environment variable template
- `firebase.json` - Firebase project configuration

---

**Last Updated**: 2026-08-17
**Version**: 1.0.0
**Maintained By**: Tiapma'atzu Development Team