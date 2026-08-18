#!/bin/bash

# Tiapma'atzu Restore Script
# Automated restore system for databases, Firebase data, and application files

set -e

# Configuration
BACKUP_DIR="./backups"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 [backup_timestamp] [component]"
    echo ""
    echo "Components:"
    echo "  postgres    - Restore PostgreSQL database"
    echo "  redis       - Restore Redis data"
    echo "  firestore   - Restore Firebase Firestore data"
    echo "  app_files   - Restore application files"
    echo "  config      - Restore configuration files"
    echo "  all         - Restore all components"
    echo ""
    echo "Example: $0 20260817_120000 postgres"
    echo "         $0 20260817_120000 all"
    exit 1
}

# Check arguments
if [ $# -lt 2 ]; then
    usage
fi

BACKUP_TIMESTAMP=$1
COMPONENT=$2

echo -e "${GREEN}Starting Tiapma'atzu Restore Process${NC}"
echo "Backup Timestamp: $BACKUP_TIMESTAMP"
echo "Component: $COMPONENT"
echo ""

# Function to restore PostgreSQL database
restore_postgres() {
    echo -e "${YELLOW}Restoring PostgreSQL database...${NC}"
    
    BACKUP_FILE="$BACKUP_DIR/postgres_backup_$BACKUP_TIMESTAMP.sql.gz"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED}✗ Backup file not found: $BACKUP_FILE${NC}"
        return 1
    fi
    
    if docker ps | grep -q hue-db; then
        gunzip -c "$BACKUP_FILE" | docker exec -i hue-db psql -U hue -d hue_db
        echo -e "${GREEN}✓ PostgreSQL restore completed${NC}"
    else
        echo -e "${RED}✗ PostgreSQL container not running${NC}"
        return 1
    fi
}

# Function to restore Redis
restore_redis() {
    echo -e "${YELLOW}Restoring Redis data...${NC}"
    
    BACKUP_FILE="$BACKUP_DIR/redis_backup_$BACKUP_TIMESTAMP.rdb.gz"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED}✗ Backup file not found: $BACKUP_FILE${NC}"
        return 1
    fi
    
    if docker ps | grep -q hue-redis; then
        gunzip -c "$BACKUP_FILE" > /tmp/redis_restore.rdb
        docker cp /tmp/redis_restore.rdb hue-redis:/data/dump.rdb
        docker exec hue-redis redis-cli SHUTDOWN NOSAVE
        docker start hue-redis
        rm /tmp/redis_restore.rdb
        echo -e "${GREEN}✓ Redis restore completed${NC}"
    else
        echo -e "${RED}✗ Redis container not running${NC}"
        return 1
    fi
}

# Function to restore Firebase Firestore data
restore_firestore() {
    echo -e "${YELLOW}Restoring Firebase Firestore data...${NC}"
    
    BACKUP_FILE="$BACKUP_DIR/firestore_backup_$BACKUP_TIMESTAMP.tar.gz"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED}✗ Backup file not found: $BACKUP_FILE${NC}"
        return 1
    fi
    
    if command -v firebase &> /dev/null; then
        tar -xzf "$BACKUP_FILE" -C "$BACKUP_DIR"
        firebase firestore:import "$BACKUP_DIR/firestore_backup_$BACKUP_TIMESTAMP"
        rm -rf "$BACKUP_DIR/firestore_backup_$BACKUP_TIMESTAMP"
        echo -e "${GREEN}✓ Firestore restore completed${NC}"
    else
        echo -e "${RED}✗ Firebase CLI not installed${NC}"
        return 1
    fi
}

# Function to restore application files
restore_app_files() {
    echo -e "${YELLOW}Restoring application files...${NC}"
    
    BACKUP_FILE="$BACKUP_DIR/app_files_$BACKUP_TIMESTAMP.tar.gz"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED}✗ Backup file not found: $BACKUP_FILE${NC}"
        return 1
    fi
    
    # Create backup of current files
    echo "Creating backup of current files..."
    tar -czf "$BACKUP_DIR/pre_restore_$(date +%Y%m%d_%H%M%S).tar.gz" src/ scripts/ api_server.py
    
    # Restore files
    tar -xzf "$BACKUP_FILE"
    echo -e "${GREEN}✓ Application files restore completed${NC}"
}

# Function to restore configuration files
restore_config() {
    echo -e "${YELLOW}Restoring configuration files...${NC}"
    
    BACKUP_FILE="$BACKUP_DIR/config_$BACKUP_TIMESTAMP.tar.gz"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED}✗ Backup file not found: $BACKUP_FILE${NC}"
        return 1
    fi
    
    # Create backup of current config
    echo "Creating backup of current configuration..."
    tar -czf "$BACKUP_DIR/pre_restore_config_$(date +%Y%m%d_%H%M%S).tar.gz" .env* docker-compose.yml firebase.json firestore.rules firestore.indexes.json
    
    # Restore configuration
    tar -xzf "$BACKUP_FILE"
    echo -e "${GREEN}✓ Configuration restore completed${NC}"
}

# Function to restore all components
restore_all() {
    echo -e "${YELLOW}Restoring all components...${NC}"
    
    restore_postgres
    restore_redis
    restore_firestore
    restore_app_files
    restore_config
    
    echo -e "${GREEN}✓ All components restored${NC}"
}

# Main restore execution
case $COMPONENT in
    postgres)
        restore_postgres
        ;;
    redis)
        restore_redis
        ;;
    firestore)
        restore_firestore
        ;;
    app_files)
        restore_app_files
        ;;
    config)
        restore_config
        ;;
    all)
        restore_all
        ;;
    *)
        echo -e "${RED}Invalid component: $COMPONENT${NC}"
        usage
        ;;
esac

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Restore Process Completed${NC}"
echo -e "${GREEN}========================================${NC}"
echo "Please restart services to apply changes:"
echo "  docker-compose restart"