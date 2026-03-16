#!/bin/bash

# Camera System Deployment Script
# This script handles deployment of the camera system in production

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="camera-system"
BACKUP_DIR="./backups"
LOG_FILE="./logs/deploy.log"

# Logging function
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $*" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    echo -e "${RED}Error: $1${NC}" >&2
    log "ERROR: $1"
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}✓ $1${NC}"
    log "SUCCESS: $1"
}

# Warning message
warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    log "WARNING: $1"
}

# Info message
info() {
    echo -e "${BLUE}ℹ $1${NC}"
    log "INFO: $1"
}

# Create backup
create_backup() {
    info "Creating backup before deployment..."

    mkdir -p "$BACKUP_DIR"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)

    # Database backup
    if [ -f "camera_system.db" ]; then
        cp camera_system.db "$BACKUP_DIR/camera_system_$TIMESTAMP.db"
        success "Database backup created: $BACKUP_DIR/camera_system_$TIMESTAMP.db"
    fi

    # Uploads backup
    if [ -d "static/uploads" ]; then
        tar -czf "$BACKUP_DIR/uploads_$TIMESTAMP.tar.gz" static/uploads/
        success "Uploads backup created: $BACKUP_DIR/uploads_$TIMESTAMP.tar.gz"
    fi
}

# Pre-deployment checks
pre_deployment_checks() {
    info "Running pre-deployment checks..."

    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        error_exit "Docker is not running. Please start Docker first."
    fi

    # Check if docker-compose is available
    if ! command -v docker-compose >/dev/null 2>&1; then
        error_exit "docker-compose is not installed."
    fi

    # Check environment file
    if [ ! -f ".env" ]; then
        warning "No .env file found. Using default values."
        cp environment.example .env
        warning "Please update .env file with production values!"
    fi

    success "Pre-deployment checks completed"
}

# Build and deploy
deploy() {
    info "Starting deployment..."

    # Pull latest changes (if using git)
    if [ -d ".git" ]; then
        info "Pulling latest changes from git..."
        git pull origin main
    fi

    # Create logs directory
    mkdir -p logs

    # Stop existing containers
    info "Stopping existing containers..."
    docker-compose down || true

    # Build new images
    info "Building Docker images..."
    docker-compose build --no-cache

    # Start services
    info "Starting services..."
    docker-compose up -d

    # Wait for services to be healthy
    info "Waiting for services to be healthy..."
    max_attempts=30
    attempt=1

    while [ $attempt -le $max_attempts ]; do
        if docker-compose ps | grep -q "healthy\|running"; then
            success "Services are healthy!"
            break
        fi

        info "Waiting for services... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done

    if [ $attempt -gt $max_attempts ]; then
        warning "Services may not be fully healthy yet. Check logs with: docker-compose logs"
    fi
}

# Post-deployment checks
post_deployment_checks() {
    info "Running post-deployment checks..."

    # Check if nginx is responding
    if curl -f -s http://localhost:8080/health >/dev/null 2>&1; then
        success "Nginx is responding correctly"
    else
        error_exit "Nginx is not responding. Check logs with: docker-compose logs nginx"
    fi

    # Check database connection
    if docker-compose exec -T db pg_isready -U camera_user -d camera_system >/dev/null 2>&1; then
        success "Database is accessible"
    else
        warning "Database may not be ready yet"
    fi

    # Check application health
    if docker-compose exec -T app1 curl -f -s http://localhost:8000/health >/dev/null 2>&1; then
        success "Application is healthy"
    else
        warning "Application health check failed"
    fi
}

# Show status
show_status() {
    info "Deployment status:"
    echo ""
    docker-compose ps
    echo ""
    info "Service URLs:"
    echo "  Application: http://localhost:8080"
    echo "  PgAdmin:     http://localhost:8082"
    echo "  Redis Cmdr:  http://localhost:8081"
    echo ""
    info "Useful commands:"
    echo "  View logs:    docker-compose logs -f"
    echo "  Stop app:     docker-compose down"
    echo "  Restart app:  docker-compose restart"
    echo "  Scale app:    docker-compose up -d --scale app1=2 app2=2 app3=2 app4=2"
}

# Rollback function
rollback() {
    warning "Starting rollback..."

    # Stop current deployment
    docker-compose down

    # Restore from backup (if available)
    if [ -d "$BACKUP_DIR" ]; then
        LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/*.db 2>/dev/null | head -1)
        if [ -n "$LATEST_BACKUP" ]; then
            cp "$LATEST_BACKUP" camera_system.db
            success "Database restored from backup"
        fi
    fi

    # Restart previous version
    docker-compose up -d
    success "Rollback completed"
}

# Main deployment function
main() {
    echo -e "${BLUE}"
    echo "=================================================="
    echo "🚀 Camera System Production Deployment"
    echo "=================================================="
    echo -e "${NC}"

    mkdir -p logs

    case "${1:-deploy}" in
        "deploy")
            create_backup
            pre_deployment_checks
            deploy
            post_deployment_checks
            show_status
            ;;
        "backup")
            create_backup
            ;;
        "rollback")
            rollback
            ;;
        "status")
            show_status
            ;;
        "logs")
            docker-compose logs -f
            ;;
        *)
            echo "Usage: $0 [deploy|backup|rollback|status|logs]"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"