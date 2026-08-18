#!/bin/bash

# Tiapma'atzu Monitoring Script
# Real-time monitoring of system health, performance, and metrics

set -e

# Configuration
API_URL="http://localhost:8000"
FRONTEND_URL="http://localhost:3000"
LOG_FILE="./logs/monitoring.log"
ALERT_EMAIL="admin@tiapmaatzu.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create logs directory
mkdir -p logs

# Function to log messages
log() {
    local message="$1"
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_FILE"
}

# Function to check API health
check_api_health() {
    log "Checking API health..."
    
    local response=$(curl -s -w "\n%{http_code}" "$API_URL/health")
    local http_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | head -n-1)
    
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✓${NC} API is healthy"
        log "API health check passed: $body"
        
        # Parse health status
        local firebase_status=$(echo "$body" | grep -o '"firebase":[^,]*' | cut -d':' -f2)
        local auth_status=$(echo "$body" | grep -o '"auth":[^,]*' | cut -d':' -f2)
        
        if [ "$firebase_status" = "true" ]; then
            echo -e "${GREEN}✓${NC} Firebase connected"
        else
            echo -e "${RED}✗${NC} Firebase disconnected"
            log "WARNING: Firebase disconnected"
        fi
        
        if [ "$auth_status" = "true" ]; then
            echo -e "${GREEN}✓${NC} Auth service connected"
        else
            echo -e "${RED}✗${NC} Auth service disconnected"
            log "WARNING: Auth service disconnected"
        fi
        
        return 0
    else
        echo -e "${RED}✗${NC} API health check failed (HTTP $http_code)"
        log "ERROR: API health check failed (HTTP $http_code)"
        return 1
    fi
}

# Function to check frontend health
check_frontend_health() {
    log "Checking frontend health..."
    
    local response=$(curl -s -w "\n%{http_code}" "$FRONTEND_URL")
    local http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✓${NC} Frontend is healthy"
        log "Frontend health check passed"
        return 0
    else
        echo -e "${RED}✗${NC} Frontend health check failed (HTTP $http_code)"
        log "ERROR: Frontend health check failed (HTTP $http_code)"
        return 1
    fi
}

# Function to check database health
check_database_health() {
    log "Checking database health..."
    
    if docker ps | grep -q hue-db; then
        if docker exec hue-db pg_isready -U hue &> /dev/null; then
            echo -e "${GREEN}✓${NC} PostgreSQL is healthy"
            log "PostgreSQL health check passed"
            
            # Get database size
            local db_size=$(docker exec hue-db psql -U hue -d hue_db -t -c "SELECT pg_size_pretty(pg_database_size('hue_db'));" 2>/dev/null | xargs)
            echo "Database size: $db_size"
            log "Database size: $db_size"
            
            return 0
        else
            echo -e "${RED}✗${NC} PostgreSQL is not ready"
            log "ERROR: PostgreSQL is not ready"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠${NC} PostgreSQL container not running"
        log "WARNING: PostgreSQL container not running"
        return 1
    fi
}

# Function to check Redis health
check_redis_health() {
    log "Checking Redis health..."
    
    if docker ps | grep -q hue-redis; then
        if docker exec hue-redis redis-cli ping &> /dev/null; then
            echo -e "${GREEN}✓${NC} Redis is healthy"
            log "Redis health check passed"
            
            # Get Redis info
            local redis_info=$(docker exec hue-redis redis-cli info memory 2>/dev/null | grep used_memory_human | cut -d':' -f2 | tr -d '\r')
            echo "Redis memory usage: $redis_info"
            log "Redis memory usage: $redis_info"
            
            return 0
        else
            echo -e "${RED}✗${NC} Redis is not responding"
            log "ERROR: Redis is not responding"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠${NC} Redis container not running"
        log "WARNING: Redis container not running"
        return 1
    fi
}

# Function to check Docker containers
check_docker_containers() {
    log "Checking Docker containers..."
    
    local containers=("tiapmaatzu-api" "hue-db" "hue-redis")
    local all_healthy=true
    
    for container in "${containers[@]}"; do
        if docker ps | grep -q "$container"; then
            local status=$(docker inspect "$container" --format='{{.State.Health.Status}}' 2>/dev/null || echo "running")
            echo -e "${GREEN}✓${NC} $container is $status"
            log "$container is $status"
        else
            echo -e "${RED}✗${NC} $container is not running"
            log "ERROR: $container is not running"
            all_healthy=false
        fi
    done
    
    if [ "$all_healthy" = true ]; then
        return 0
    else
        return 1
    fi
}

# Function to check disk space
check_disk_space() {
    log "Checking disk space..."
    
    local disk_usage=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
    echo "Disk usage: $disk_usage%"
    log "Disk usage: $disk_usage%"
    
    if [ "$disk_usage" -gt 80 ]; then
        echo -e "${RED}✗${NC} Disk usage is critical"
        log "ERROR: Disk usage is critical ($disk_usage%)"
        return 1
    elif [ "$disk_usage" -gt 60 ]; then
        echo -e "${YELLOW}⚠${NC} Disk usage is high"
        log "WARNING: Disk usage is high ($disk_usage%)"
        return 0
    else
        echo -e "${GREEN}✓${NC} Disk usage is normal"
        log "Disk usage is normal ($disk_usage%)"
        return 0
    fi
}

# Function to check memory usage
check_memory_usage() {
    log "Checking memory usage..."
    
    local mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    echo "Memory usage: $mem_usage%"
    log "Memory usage: $mem_usage%"
    
    if [ "$mem_usage" -gt 90 ]; then
        echo -e "${RED}✗${NC} Memory usage is critical"
        log "ERROR: Memory usage is critical ($mem_usage%)"
        return 1
    elif [ "$mem_usage" -gt 75 ]; then
        echo -e "${YELLOW}⚠${NC} Memory usage is high"
        log "WARNING: Memory usage is high ($mem_usage%)"
        return 0
    else
        echo -e "${GREEN}✓${NC} Memory usage is normal"
        log "Memory usage is normal ($mem_usage%)"
        return 0
    fi
}

# Function to check API response time
check_api_response_time() {
    log "Checking API response time..."
    
    local start_time=$(date +%s%N)
    curl -s "$API_URL/health" > /dev/null
    local end_time=$(date +%s%N)
    local response_time=$((($end_time - $start_time) / 1000000))
    
    echo "API response time: ${response_time}ms"
    log "API response time: ${response_time}ms"
    
    if [ "$response_time" -gt 1000 ]; then
        echo -e "${RED}✗${NC} API response time is slow"
        log "ERROR: API response time is slow (${response_time}ms)"
        return 1
    elif [ "$response_time" -gt 500 ]; then
        echo -e "${YELLOW}⚠${NC} API response time is elevated"
        log "WARNING: API response time is elevated (${response_time}ms)"
        return 0
    else
        echo -e "${GREEN}✓${NC} API response time is good"
        log "API response time is good (${response_time}ms)"
        return 0
    fi
}

# Function to check recent logs for errors
check_error_logs() {
    log "Checking recent logs for errors..."
    
    local error_count=0
    
    if [ -f "logs/error.log" ]; then
        error_count=$(tail -100 logs/error.log | grep -i "error" | wc -l)
        echo "Recent errors (last 100 lines): $error_count"
        log "Recent errors (last 100 lines): $error_count"
        
        if [ "$error_count" -gt 10 ]; then
            echo -e "${RED}✗${NC} High error rate detected"
            log "ERROR: High error rate detected ($error_count errors)"
            return 1
        elif [ "$error_count" -gt 5 ]; then
            echo -e "${YELLOW}⚠${NC} Elevated error rate detected"
            log "WARNING: Elevated error rate detected ($error_count errors)"
            return 0
        else
            echo -e "${GREEN}✓${NC} Error rate is normal"
            log "Error rate is normal ($error_count errors)"
            return 0
        fi
    else
        echo -e "${YELLOW}⚠${NC} No error log file found"
        log "WARNING: No error log file found"
        return 0
    fi
}

# Function to generate monitoring report
generate_report() {
    log "Generating monitoring report..."
    
    local report_file="./logs/monitoring_report_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "Tiapma'atzu Monitoring Report"
        echo "Generated: $(date)"
        echo "================================"
        echo ""
        echo "System Status:"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        echo "Resource Usage:"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
        echo ""
        echo "Disk Usage:"
        df -h
        echo ""
        echo "Memory Usage:"
        free -h
        echo ""
        echo "Recent Logs (last 20 lines):"
        tail -20 "$LOG_FILE"
    } > "$report_file"
    
    echo "Report generated: $report_file"
    log "Report generated: $report_file"
}

# Main monitoring function
main() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Tiapma'atzu System Monitoring${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo "Started: $(date)"
    echo ""
    
    local overall_status=0
    
    # Run all health checks
    check_api_health || overall_status=1
    check_frontend_health || overall_status=1
    check_database_health || overall_status=1
    check_redis_health || overall_status=1
    check_docker_containers || overall_status=1
    check_disk_space || overall_status=1
    check_memory_usage || overall_status=1
    check_api_response_time || overall_status=1
    check_error_logs || overall_status=1
    
    # Generate report
    generate_report
    
    echo ""
    echo -e "${BLUE}========================================${NC}"
    if [ $overall_status -eq 0 ]; then
        echo -e "${GREEN}All Systems Operational${NC}"
    else
        echo -e "${RED}System Issues Detected${NC}"
    fi
    echo -e "${BLUE}========================================${NC}"
    echo "Completed: $(date)"
    
    return $overall_status
}

# Execute main function
main