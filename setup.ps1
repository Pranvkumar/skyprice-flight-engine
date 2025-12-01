# Setup script for Flight Price Recommendation Engine
# For Windows PowerShell

Write-Host "🚀 Setting up Flight Price Recommendation Engine..." -ForegroundColor Green

# Check prerequisites
Write-Host "`nChecking prerequisites..." -ForegroundColor Yellow

# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Python found: $(python --version)" -ForegroundColor Green

# Check Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js is not installed. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Node.js found: $(node --version)" -ForegroundColor Green

# Check Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  Docker not found. You'll need to install PostgreSQL and Redis manually." -ForegroundColor Yellow
} else {
    Write-Host "✅ Docker found: $(docker --version)" -ForegroundColor Green
}

# Backend setup
Write-Host "`n📦 Setting up backend..." -ForegroundColor Yellow
Set-Location backend

# Create virtual environment
python -m venv venv
& .\venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file. Please edit it with your configuration." -ForegroundColor Green
}

Set-Location ..

# Frontend setup
Write-Host "`n📦 Setting up frontend..." -ForegroundColor Yellow
Set-Location frontend

# Install dependencies
npm install

# Copy environment file
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file." -ForegroundColor Green
}

Set-Location ..

# Docker setup
Write-Host "`n🐳 Starting Docker services..." -ForegroundColor Yellow
if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
    docker-compose up -d postgres redis
    Write-Host "✅ PostgreSQL and Redis started" -ForegroundColor Green
} else {
    Write-Host "⚠️  Docker Compose not available. Please start PostgreSQL and Redis manually." -ForegroundColor Yellow
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`nTo start the application:" -ForegroundColor Cyan
Write-Host "`n1. Backend:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host "`n2. Frontend (in another terminal):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm start" -ForegroundColor Gray
Write-Host "`n3. Or use Docker Compose:" -ForegroundColor White
Write-Host "   docker-compose up" -ForegroundColor Gray
Write-Host "`nAccess the application:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White
