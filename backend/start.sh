#!/bin/bash
# Render.com startup script

echo "Starting SkyPrice Flight Engine..."
echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"

# Check if environment variables are set
if [ -z "$AMADEUS_API_KEY" ]; then
    echo "ERROR: AMADEUS_API_KEY not set!"
    exit 1
fi

if [ -z "$AMADEUS_API_SECRET" ]; then
    echo "ERROR: AMADEUS_API_SECRET not set!"
    exit 1
fi

echo "Environment variables configured ✓"
echo "Starting server on port ${PORT:-8000}..."

# Run the server
python test_server.py
