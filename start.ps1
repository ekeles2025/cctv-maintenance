# Startup script for Camera System application (Windows PowerShell)

Write-Host "📦 Camera System - Startup Script" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
$venvPath = "venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "📍 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Install/upgrade requirements
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Check for .env file
if (-not ((Test-Path ".env") -or (Test-Path ".env.local"))) {
    Write-Host "⚠️  No .env or .env.local file found" -ForegroundColor Yellow
    Write-Host "📋 Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env created - please edit it with your settings" -ForegroundColor Green
}

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
$directories = @("static/uploads", "static/logo", "logs", "instance")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}
Write-Host "✅ Directories created" -ForegroundColor Green

# Start the application
Write-Host ""
Write-Host "🚀 Starting Camera System..." -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
python app.py
