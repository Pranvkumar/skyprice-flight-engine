#!/bin/bash

# Setup script for Flight Price Recommendation Engine
# For Linux/Mac

echo "🚀 Setting up Flight Price Recommendation Engine..."

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker not found. You'll need to install PostgreSQL and Redis manually."
else
    echo "✅ Docker found: $(docker --version)"
fi

# Backend setup
echo ""
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your configuration."
fi

cd ..

# Frontend setup
echo ""
echo "📦 Setting up frontend..."
cd frontend

# Install dependencies
npm install

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file."
fi

cd ..

# Docker setup
echo ""
echo "🐳 Starting Docker services..."
if command -v docker-compose &> /dev/null; then
    docker-compose up -d postgres redis
    echo "✅ PostgreSQL and Redis started"
else
    echo "⚠️  Docker Compose not available. Please start PostgreSQL and Redis manually."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo ""
echo "1. Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Frontend (in another terminal):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Or use Docker Compose:"
echo "   docker-compose up"
echo ""
echo "Access the application:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
