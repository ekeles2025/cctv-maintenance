#!/bin/bash
# Startup script for Camera System application

echo "📦 Camera System - Startup Script"
echo "=================================="

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📍 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade requirements
echo "📥 Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Check for .env file
if [ ! -f ".env" ] && [ ! -f ".env.local" ]; then
    echo "⚠️  No .env or .env.local file found"
    echo "📋 Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ .env created - please edit it with your settings"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p static/uploads
mkdir -p static/logo
mkdir -p logs
mkdir -p instance
echo "✅ Directories created"

# Start the application
echo ""
echo "🚀 Starting Camera System..."
echo "=================================="
python3 app.py
