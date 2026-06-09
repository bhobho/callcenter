#!/bin/bash

# Voice Call Center AI - Startup Script for macOS

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "======================================"
echo "Voice Call Center AI - macOS Startup"
echo "======================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and fill in your credentials:"
    echo "  cp .env.example .env"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data logs

# Display configuration
echo ""
echo "Configuration:"
echo "  Port: $(grep -E "^PORT=" .env | cut -d'=' -f2 || echo '8000')"
echo "  Host: $(grep -E "^HOST=" .env | cut -d'=' -f2 || echo '0.0.0.0')"
echo "  Call Center Type: $(grep -E "^CALL_CENTER_TYPE=" .env | cut -d'=' -f2 || echo 'customer_service')"
echo ""

# Check API credentials
if grep -q "your_account_sid\|your_auth_token\|your_api_key" .env; then
    echo "Warning: Please update .env with your actual API credentials"
    echo ""
fi

# Start the application
echo "Starting Voice Call Center AI..."
echo "Access the API at: http://localhost:8000"
echo "API Documentation at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Use explicit path to venv python to avoid activation issues
venv/bin/python main.py
