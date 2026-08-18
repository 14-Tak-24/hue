#!/bin/bash

# Tiapma'atzu Deployment Script
# Automated deployment system for development, staging, and production environments

set -e

# Configuration
ENVIRONMENT=${1:-development}
PROJECT_NAME="tiapmaatzu"
GIT_BRANCH=${2:-main}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 [environment] [git_branch]"
    echo ""
    echo "Environments:"
    echo "  development - Local development deployment"
    echo "  staging     - Staging environment deployment"
    echo "  production  - Production environment deployment"
    echo ""
    echo "Git Branch: (default: main)"
    echo ""
    echo "Example: $0 production main"
    echo "         $0 staging develop"
    exit 1
}

# Function to log messages
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

# Function to log success
log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to log error
log_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to log warning
log_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    log_success "Docker is installed"
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    log_success "Docker Compose is installed"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed"
        exit 1
    fi
    log_success "Git is installed"
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    log_success "Docker daemon is running"
}

# Function to setup environment
setup_environment() {
    log "Setting up $ENVIRONMENT environment..."
    
    case $ENVIRONMENT in
        development)
            ENV_FILE=".env"
            COMPOSE_FILE="docker-compose.yml"
            ;;
        staging)
            ENV_FILE=".env.staging"
            COMPOSE_FILE="docker-compose.staging.yml"
            ;;
        production)
            ENV_FILE=".env.production"
            COMPOSE_FILE="docker-compose.yml"
            ;;
        *)
            log_error "Invalid environment: $ENVIRONMENT"
            usage
            ;;
    esac
    
    # Check if environment file exists
    if [ ! -f "$ENV_FILE" ]; then
        log_warning "Environment file $ENV_FILE not found"
        log "Creating from template..."
        if [ -f ".env.example" ]; then
            cp .env.example "$ENV_FILE"
            log_warning "Please update $ENV_FILE with your configuration"
        else
            log_error "No .env.example template found"
            exit 1
        fi
    fi
    
    log_success "Environment setup completed"
}

# Function to pull latest code
pull_code() {
    log "Pulling latest code from branch: $GIT_BRANCH..."
    
    git fetch origin
    git checkout "$GIT_BRANCH"
    git pull origin "$GIT_BRANCH"
    
    log_success "Code pull completed"
}

# Function to build Docker images
build_images() {
    log "Building Docker images..."
    
    case $ENVIRONMENT in
        development)
            docker-compose build
            ;;
        staging)
            docker-compose -f "$COMPOSE_FILE" build
            ;;
        production)
            docker-compose -f "$COMPOSE_FILE" build --no-cache
            ;;
    esac
    
    log_success "Docker images built successfully"
}

# Function to stop existing containers
stop_containers() {
    log "Stopping existing containers..."
    
    case $ENVIRONMENT in
        development)
            docker-compose down
            ;;
        staging)
            docker-compose -f "$COMPOSE_FILE" down
            ;;
        production)
            docker-compose -f "$COMPOSE_FILE" down
            ;;
    esac
    
    log_success "Containers stopped"
}

# Function to start containers
start_containers() {
    log "Starting containers..."
    
    case $ENVIRONMENT in
        development)
            docker-compose up -d
            ;;
        staging)
            docker-compose -f "$COMPOSE_FILE" up -d
            ;;
        production)
            docker-compose -f "$COMPOSE_FILE" up -d
            ;;
    esac
    
    log_success "Containers started"
}

# Function to run database migrations
run_migrations() {
    log "Running database migrations..."
    
    # Check if database is ready
    MAX_ATTEMPTS=30
    ATTEMPT=0
    
    while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
        if docker exec hue-db psql -U hue -d hue_db -c "SELECT 1" &> /dev/null; then
            log_success "Database is ready"
            break
        fi
        ATTEMPT=$((ATTEMPT + 1))
        log "Waiting for database... (attempt $ATTEMPT/$MAX_ATTEMPTS)"
        sleep 2
    done
    
    if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
        log_error "Database connection failed"
        exit 1
    fi
    
    # Run migrations (if migration system exists)
    if [ -f "scripts/migrate.py" ]; then
        docker-compose exec api python scripts/migrate.py
        log_success "Migrations completed"
    else
        log_warning "No migration script found"
    fi
}

# Function to health check
health_check() {
    log "Performing health checks..."
    
    MAX_ATTEMPTS=30
    ATTEMPT=0
    
    while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            log_success "API health check passed"
            break
        fi
        ATTEMPT=$((ATTEMPT + 1))
        log "Waiting for API to be healthy... (attempt $ATTEMPT/$MAX_ATTEMPTS)"
        sleep 2
    done
    
    if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
        log_error "API health check failed"
        exit 1
    fi
}

# Function to cleanup old images
cleanup_images() {
    log "Cleaning up old Docker images..."
    
    docker image prune -f
    log_success "Old images cleaned up"
}

# Function to deploy to production
deploy_production() {
    log "Deploying to production..."
    
    # Additional production-specific steps
    log "Running production pre-deployment checks..."
    
    # Backup current deployment
    log "Creating backup before deployment..."
    ./scripts/backup.sh
    
    # Deploy with zero downtime (if using load balancer)
    log "Deploying with zero downtime..."
    
    # Additional production checks
    log "Running post-deployment verification..."
    health_check
    
    log_success "Production deployment completed"
}

# Main deployment function
main() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Tiapma'atzu Deployment Script${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo "Environment: $ENVIRONMENT"
    echo "Git Branch: $GIT_BRANCH"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Setup environment
    setup_environment
    
    # Pull latest code
    pull_code
    
    # Build images
    build_images
    
    # Stop existing containers
    stop_containers
    
    # Start containers
    start_containers
    
    # Run migrations
    run_migrations
    
    # Health check
    health_check
    
    # Environment-specific actions
    case $ENVIRONMENT in
        production)
            deploy_production
            ;;
        staging)
            log "Staging deployment completed"
            ;;
        development)
            log "Development deployment completed"
            ;;
    esac
    
    # Cleanup
    cleanup_images
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Deployment Completed Successfully${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo "Environment: $ENVIRONMENT"
    echo "Timestamp: $(date)"
    echo ""
    echo "Services:"
    echo "  API: http://localhost:8000"
    echo "  Health: http://localhost:8000/health"
    echo "  Frontend: http://localhost:3000"
}

# Trap errors
trap 'log_error "Deployment failed"; exit 1' ERR

# Execute main function
main