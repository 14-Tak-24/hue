#!/bin/bash

# Tiapma'atzu Backup Script
# Automated backup system for databases, Firebase data, and application files

set -e

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS=30

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create backup directory
mkdir -p "$BACKUP_DIR"

echo -e "${GREEN}Starting Tiapma'atzu Backup Process${NC}"
echo "Timestamp: $TIMESTAMP"
echo "Backup Directory: $BACKUP_DIR"
echo ""

# Function to backup PostgreSQL database
backup_postgres() {
    echo -e "${YELLOW}Backing up PostgreSQL database...${NC}"
    
    if docker ps | grep -q hue-db; then
        docker exec hue-db pg_dump -U hue hue_db > "$BACKUP_DIR/postgres_backup_$TIMESTAMP.sql"
        gzip "$BACKUP_DIR/postgres_backup_$TIMESTAMP.sql"
        echo -e "${GREEN}✓ PostgreSQL backup completed${NC}"
    else
        echo -e "${RED}✗ PostgreSQL container not running${NC}"
    fi
}

# Function to backup Redis
backup_redis() {
    echo -e "${YELLOW}Backing up Redis data...${NC}"
    
    if docker ps | grep -q hue-redis; then
        docker exec hue-redis redis-cli BGSAVE
        docker cp hue-redis:/data/dump.rdb "$BACKUP_DIR/redis_backup_$TIMESTAMP.rdb"
        gzip "$BACKUP_DIR/redis_backup_$TIMESTAMP.rdb"
        echo -e "${GREEN}✓ Redis backup completed${NC}"
    else
        echo -e "${RED}✗ Redis container not running${NC}"
    fi
}

# Function to backup Firebase Firestore data
backup_firestore() {
    echo -e "${YELLOW}Backing up Firebase Firestore data...${NC}"
    
    if command -v firebase &> /dev/null; then
        firebase firestore:export "$BACKUP_DIR/firestore_backup_$TIMESTAMP"
        tar -czf "$BACKUP_DIR/firestore_backup_$TIMESTAMP.tar.gz" -C "$BACKUP_DIR" "firestore_backup_$TIMESTAMP"
        rm -rf "$BACKUP_DIR/firestore_backup_$TIMESTAMP"
        echo -e "${GREEN}✓ Firestore backup completed${NC}"
    else
        echo -e "${RED}✗ Firebase CLI not installed${NC}"
    fi
}

# Function to backup application files
backup_app_files() {
    echo -e "${YELLOW}Backing up application files...${NC}"
    
    tar -czf "$BACKUP_DIR/app_files_$TIMESTAMP.tar.gz" \
        --exclude='node_modules' \
        --exclude='venv' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='backups' \
        --exclude='logs' \
        src/ scripts/ api_server.py requirements.txt deploy/
    
    echo -e "${GREEN}✓ Application files backup completed${NC}"
}

# Function to backup configuration files
backup_config() {
    echo -e "${YELLOW}Backing up configuration files...${NC}"
    
    tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
        .env* \
        docker-compose.yml \
        firebase.json \
        firestore.rules \
        firestore.indexes.json
    
    echo -e "${GREEN}✓ Configuration backup completed${NC}"
}

# Function to cleanup old backups
cleanup_old_backups() {
    echo -e "${YELLOW}Cleaning up backups older than $RETENTION_DAYS days...${NC}"
    
    find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -delete
    echo -e "${GREEN}✓ Old backups cleaned up${NC}"
}

# Function to generate backup report
generate_report() {
    echo -e "${YELLOW}Generating backup report...${NC}"
    
    REPORT_FILE="$BACKUP_DIR/backup_report_$TIMESTAMP.txt"
    
    echo "Tiapma'atzu Backup Report" > "$REPORT_FILE"
    echo "Timestamp: $TIMESTAMP" >> "$REPORT_FILE"
    echo "========================" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
    
    echo "Backup Contents:" >> "$REPORT_FILE"
    ls -lh "$BACKUP_DIR" | grep "$TIMESTAMP" >> "$REPORT_FILE"
    
    echo "" >> "$REPORT_FILE"
    echo "Disk Usage:" >> "$REPORT_FILE"
    du -sh "$BACKUP_DIR" >> "$REPORT_FILE"
    
    echo -e "${GREEN}✓ Backup report generated${NC}"
}

# Main backup execution
main() {
    # Run all backup functions
    backup_postgres
    backup_redis
    backup_firestore
    backup_app_files
    backup_config
    
    # Cleanup and report
    cleanup_old_backups
    generate_report
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Backup Process Completed Successfully${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo "Backup Location: $BACKUP_DIR"
    echo "Timestamp: $TIMESTAMP"
}

# Execute main function
main