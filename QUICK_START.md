# 🚀 Quick Start Guide

## Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)
- Redis 7+ (or use Docker)

## Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
cd flight-price-recommendation-engine

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Grafana (monitoring): http://localhost:3001

## Option 2: Manual Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
copy .env.example .env
# Edit .env with your configuration

# Run database migrations
# Make sure PostgreSQL is running
python -m alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
copy .env.example .env
# Edit .env with your configuration

# Start development server
npm start
```

### Redis Setup (if not using Docker)

```bash
# Windows (using Chocolatey):
choco install redis-64

# Start Redis
redis-server

# Linux:
sudo apt-get install redis-server
sudo systemctl start redis
```

## Environment Variables

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://flightuser:flightpass123@localhost:5432/flight_pricing

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
ENVIRONMENT=development
DEBUG=true
ML_MODEL_PATH=./models

# API Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### Frontend (.env)

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_ENVIRONMENT=development
```

## Testing the Application

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Predict price
curl -X POST "http://localhost:8000/api/v1/forecast/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "BOM",
    "destination": "DEL",
    "departure_date": "2025-12-15T00:00:00",
    "days_ahead": 7
  }'
```

### Test Frontend

1. Open http://localhost:3000
2. Navigate to "Price Forecast"
3. Enter:
   - Origin: BOM
   - Destination: DEL
   - Departure Date: Future date
4. Click "Generate Forecast"

## Sample Data

The system comes with sample data for testing:

**Routes:**
- BOM (Mumbai) ↔ DEL (Delhi)
- BOM (Mumbai) → BLR (Bangalore)
- DEL (Delhi) → BOM (Mumbai)

**Airlines:**
- Air India (AI)
- IndiGo (6E)
- SpiceJet (SG)

## Running Tests

### Backend Tests

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

## Common Issues & Solutions

### Issue: Database connection error

**Solution:**
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify credentials

### Issue: Redis connection error

**Solution:**
- Ensure Redis is running
- Check REDIS_URL in .env
- On Windows, start Redis service

### Issue: Port already in use

**Solution:**
```bash
# Backend (port 8000)
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Frontend (port 3000)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Issue: CORS errors

**Solution:**
- Check ALLOWED_ORIGINS in backend .env
- Ensure frontend URL is included
- Restart backend server

## Next Steps

1. **Explore API Documentation**: http://localhost:8000/docs
2. **Test Price Forecasting**: Generate predictions for different routes
3. **View Analytics**: Check price trends and demand patterns
4. **Monitor System**: Access Grafana dashboard (if using monitoring profile)

## Development Workflow

```bash
# 1. Start services
docker-compose up -d postgres redis

# 2. Backend development
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload

# 3. Frontend development (new terminal)
cd frontend
npm start

# 4. Make changes and test

# 5. Run tests
# Backend
pytest tests/ -v

# Frontend
npm test
```

## Production Deployment

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for production deployment instructions.

## Support

For issues or questions:
- Check [API Documentation](http://localhost:8000/docs)
- Review [README.md](./README.md)
- Contact: Pranav (590011587) or Om (590014492)
