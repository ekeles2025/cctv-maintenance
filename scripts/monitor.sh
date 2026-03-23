#!/bin/bash

# Camera System Monitoring Script
# This script provides monitoring and maintenance functions

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PROJECT_NAME="camera-system"
LOG_FILE="./logs/monitor.log"

# Logging
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}ℹ $1${NC}"
    log "INFO: $1"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
    log "SUCCESS: $1"
}

warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    log "WARNING: $1"
}

error() {
    echo -e "${RED}✗ $1${NC}"
    log "ERROR: $1"
}

# Check service health
check_health() {
    info "Checking service health..."

    # Check Docker services
    if ! docker-compose ps | grep -q "Up"; then
        error "No services are running"
        return 1
    fi

    # Check nginx
    if curl -f -s http://localhost:8080/health >/dev/null 2>&1; then
        success "Nginx is healthy"
    else
        error "Nginx is not responding"
    fi

    # Check database
    if docker-compose exec -T db pg_isready -U camera_user -d camera_system >/dev/null 2>&1; then
        success "Database is healthy"
    else
        error "Database is not responding"
    fi

    # Check Redis
    if docker-compose exec -T redis redis-cli ping >/dev/null 2>&1; then
        success "Redis is healthy"
    else
        error "Redis is not responding"
    fi

    # Check application instances
    for app in app1 app2 app3 app4; do
        if docker-compose exec -T $app curl -f -s http://localhost:8000/health >/dev/null 2>&1; then
            success "Application $app is healthy"
        else
            error "Application $app is not responding"
        fi
    done
}

# Show resource usage
show_resources() {
    info "Resource usage:"

    echo ""
    echo "Docker containers:"
    docker-compose ps

    echo ""
    echo "Container resource usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"

    echo ""
    echo "Disk usage:"
    df -h | grep -E "(Filesystem|/)$"

    echo ""
    echo "Database size:"
    docker-compose exec -T db psql -U camera_user -d camera_system -c "SELECT pg_size_pretty(pg_database_size(current_database()));" 2>/dev/null || echo "Could not get database size"
}

# Show logs
show_logs() {
    local service="${1:-all}"
    local lines="${2:-50}"

    if [ "$service" = "all" ]; then
        info "Showing last $lines lines from all services:"
        docker-compose logs --tail="$lines" -f
    else
        info "Showing last $lines lines from $service:"
        docker-compose logs --tail="$lines" -f "$service"
    fi
}

# Database maintenance
db_maintenance() {
    info "Running database maintenance..."

    # Vacuum analyze
    docker-compose exec -T db psql -U camera_user -d camera_system -c "VACUUM ANALYZE;"

    # Reindex
    docker-compose exec -T db psql -U camera_user -d camera_system -c "REINDEX DATABASE camera_system;"

    # Show table sizes
    echo ""
    echo "Table sizes:"
    docker-compose exec -T db psql -U camera_user -d camera_system -c "
        SELECT
            schemaname,
            tablename,
            pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
    "

    success "Database maintenance completed"
}

# Backup database
backup_db() {
    info "Creating database backup..."

    local backup_dir="./backups"
    mkdir -p "$backup_dir"

    local timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_file="$backup_dir/camera_system_$timestamp.sql"

    docker-compose exec -T db pg_dump -U camera_user camera_system > "$backup_file"

    # Compress backup
    gzip "$backup_file"

    success "Database backup created: ${backup_file}.gz"

    # Cleanup old backups (keep last 10)
    cd "$backup_dir" || exit 1
    ls -t *.sql.gz 2>/dev/null | tail -n +11 | xargs -r rm
    cd - >/dev/null 2>&1 || exit 1

    if [ $? -eq 0 ]; then
        info "Old backups cleaned up (keeping last 10)"
    fi
}

# Clean up Docker
cleanup() {
    info "Cleaning up Docker resources..."

    # Remove stopped containers
    docker container prune -f

    # Remove unused images
    docker image prune -f

    # Remove unused volumes
    docker volume prune -f

    # Remove unused networks
    docker network prune -f

    success "Docker cleanup completed"
}

# Show system statistics
show_stats() {
    info "System statistics:"

    echo ""
    echo "=== Application Statistics ==="
    # Get stats from database
    docker-compose exec -T db psql -U camera_user -d camera_system -c "
        SELECT json_build_object(
            'total_cameras', (SELECT COUNT(*) FROM cameras),
            'total_regions', (SELECT COUNT(*) FROM regions),
            'total_branches', (SELECT COUNT(*) FROM branches),
            'total_technicians', (SELECT COUNT(*) FROM \"user\" WHERE role = 'technician'),
            'open_faults', (SELECT COUNT(*) FROM faults WHERE resolved_at IS NULL),
            'closed_faults', (SELECT COUNT(*) FROM faults WHERE resolved_at IS NOT NULL),
            'faults_today', (SELECT COUNT(*) FROM faults WHERE date_reported::date = CURRENT_DATE)
        )::text as stats;
    " 2>/dev/null | grep -v "json_build_object\|-\|(\|)" | jq . 2>/dev/null || echo "Could not retrieve application statistics"

    echo ""
    echo "=== Performance Metrics ==="
    # Show response times (if available)
    echo "Average response time: Check nginx access logs"

    echo ""
    echo "=== Error Rates ==="
    # Count errors in logs
    local error_count=$(docker-compose logs --no-color 2>&1 | grep -i error | wc -l)
    echo "Errors in logs: $error_count"
}

# Restart services
restart_services() {
    info "Restarting all services..."
    docker-compose restart
    sleep 10
    check_health
}

# Scale application
scale_app() {
    local instances="${1:-4}"
    info "Scaling application to $instances instances..."

    docker-compose up -d --scale app1="$instances" --scale app2="$instances" --scale app3="$instances" --scale app4="$instances"

    success "Application scaled to $instances instances"
}

# Main function
main() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "📊 Camera System Monitoring & Maintenance"
    echo "=================================================="
    echo -e "${NC}"

    mkdir -p logs

    case "${1:-status}" in
        "health")
            check_health
            ;;
        "resources")
            show_resources
            ;;
        "logs")
            show_logs "${2:-all}" "${3:-50}"
            ;;
        "stats")
            show_stats
            ;;
        "backup")
            backup_db
            ;;
        "maintenance")
            db_maintenance
            ;;
        "cleanup")
            cleanup
            ;;
        "restart")
            restart_services
            ;;
        "scale")
            scale_app "${2:-4}"
            ;;
        "status")
            check_health
            echo ""
            show_resources
            ;;
        *)
            echo "Usage: $0 [health|resources|logs|stats|backup|maintenance|cleanup|restart|scale|status]"
            echo ""
            echo "Examples:"
            echo "  $0 health                    # Check service health"
            echo "  $0 logs nginx 100            # Show last 100 lines from nginx logs"
            echo "  $0 scale 6                   # Scale to 6 instances"
            echo "  $0 backup                    # Create database backup"
            exit 1
            ;;
    esac
}

main "$@"