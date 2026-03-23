#!/bin/bash

# Render deployment script for CCTV Maintenance System

echo "🚀 Starting deployment to Render..."

# Create necessary directories
mkdir -p static/uploads
mkdir -p static/logo

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export PORT=10000
export SECRET_KEY=${SECRET_KEY:-"production-secret-key-change-this"}
export DATABASE_URL=${DATABASE_URL:-"sqlite:///camera_system.db"}
export COMPANY_NAME=${COMPANY_NAME:-"CCTV Portal EG"}
export LOGO_SIZE=${LOGO_SIZE:-50}
export MAX_CONTENT_LENGTH=${MAX_CONTENT_LENGTH:-16777216}

# Initialize database
echo "🗄️ Initializing database..."
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully')
"

echo "✅ Deployment ready!"
echo "🌐 Application will be available on port 10000"
