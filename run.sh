#!/bin/bash

# Simple run script - just starts the app
cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d venv ]; then
    echo "Virtual environment not found. Run: python3 -m venv venv"
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Run: cp .env.example .env"
    exit 1
fi

# Run the app using venv python
echo "Starting Voice Call Center AI..."
venv/bin/python main.py
