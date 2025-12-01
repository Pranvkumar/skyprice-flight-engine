# Amadeus API Integration Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your Amadeus API Credentials

1. **Visit:** https://developers.amadeus.com
2. **Click:** "Register" (top right)
3. **Fill in:** Your details (free account)
4. **Verify:** Your email
5. **Create App:**
   - Go to "My Self-Service Workspace"
   - Click "Create New App"
   - Name: "Flight Price Engine"
   - Click "Create"
6. **Copy Credentials:**
   - API Key (looks like: `xxxxxxxxxxxxxxxxxxx`)
   - API Secret (looks like: `yyyyyyyyyyyyyyyyyy`)

### Step 2: Configure Environment Variables

1. **Create `.env` file** in `backend/` directory:

```bash
cd C:\Coding\Web\backend
copy .env.example .env
```

2. **Edit `.env` file** and add your credentials:

```env
# Amadeus API Configuration
AMADEUS_API_KEY=your_api_key_here
AMADEUS_API_SECRET=your_api_secret_here
AMADEUS_ENVIRONMENT=test  # Use 'production' for live data
```

### Step 3: Install Dependencies

```bash
# Already done! ✅
# amadeus==12.0.0 is now installed
```

### Step 4: Test the Integration

```bash
cd C:\Coding\Web\backend
python -c "from app.services.data_sources.amadeus_client import get_amadeus_client; client = get_amadeus_client(); print('✅ Amadeus API connected!')"
```

## 📡 Available Endpoints

### 1. Live Flight Prices
```http
GET /api/v1/realtime/live-prices?origin=BOM&destination=DEL&departure_date=2025-12-15
```

**Response:**
```json
{
  "success": true,
  "route": "BOM-DEL",
  "flights": [
    {
      "price": 5420.50,
      "currency": "INR",
      "airline": "AI",
      "departure": {"iata": "BOM", "time": "2025-12-15T08:30:00"},
      "arrival": {"iata": "DEL", "time": "2025-12-15T10:45:00"}
    }
  ]
}
```

### 2. Price Trends (Historical)
```http
GET /api/v1/realtime/price-trends?origin=BOM&destination=DEL&days_back=30
```

**Returns:** 30 days of historical prices, average, min, max, volatility

### 3. Booking Recommendation
```http
GET /api/v1/realtime/booking-recommendation?origin=BOM&destination=DEL&target_date=2025-12-20
```

**Returns:** Book now vs wait, cheapest dates, price analysis

### 4. Route Insights (All-in-One)
```http
GET /api/v1/realtime/route-insights?origin=BOM&destination=DEL&departure_date=2025-12-15
```

**Returns:** Live prices + trends + recommendations in one call

### 5. Airport Search (Autocomplete)
```http
GET /api/v1/realtime/search-airports?keyword=Mumbai
```

**Returns:** List of airports matching "Mumbai"

## 🔔 Price Alerts

### Create Alert
```http
POST /api/v1/alerts/create
Content-Type: application/json

{
  "user_email": "user@example.com",
  "origin": "BOM",
  "destination": "DEL",
  "target_price": 5000,
  "departure_date": "2025-12-15",
  "cabin_class": "ECONOMY"
}
```

### Get User Alerts
```http
GET /api/v1/alerts/user/user@example.com
```

### Check Alert
```http
POST /api/v1/alerts/check/alert_1
Content-Type: application/json

{
  "current_price": 4800
}
```

## 🧪 Testing

### Test Live Prices
```bash
curl "http://localhost:8000/api/v1/realtime/live-prices?origin=BOM&destination=DEL&departure_date=2025-12-15"
```

### Test Airport Search
```bash
curl "http://localhost:8000/api/v1/realtime/search-airports?keyword=Delhi"
```

### Test Health Check
```bash
curl "http://localhost:8000/api/v1/realtime/health"
```

## 📊 Amadeus Free Tier Limits

| Feature | Free Tier | Notes |
|---------|-----------|-------|
| API Calls | 1,000/month | Plenty for development |
| Flight Search | ✅ | Real-time prices |
| Airport Search | ✅ | Autocomplete data |
| Price Analytics | ✅ | ML predictions |
| Historical Data | Limited | Sampled data |

## 🎯 Popular Routes to Test

```python
# Indian Domestic Routes
BOM → DEL  # Mumbai to Delhi
DEL → BLR  # Delhi to Bangalore
BOM → BLR  # Mumbai to Bangalore
DEL → GOI  # Delhi to Goa
BOM → CCU  # Mumbai to Kolkata

# International Routes
DEL → DXB  # Delhi to Dubai
BOM → LHR  # Mumbai to London
DEL → SIN  # Delhi to Singapore
BOM → JFK  # Mumbai to New York
DEL → LAX  # Delhi to Los Angeles
```

## 🐛 Troubleshooting

### Error: "Invalid API credentials"
- ✅ Check `.env` file has correct API key and secret
- ✅ Ensure no extra spaces in credentials
- ✅ Verify account is activated on Amadeus portal

### Error: "No flights found"
- ✅ Try a popular route (BOM-DEL)
- ✅ Use a future date (at least 7 days ahead)
- ✅ Check IATA codes are correct (3 letters)

### Error: "Rate limit exceeded"
- ✅ Free tier: 1,000 calls/month
- ✅ Implement caching (Redis)
- ✅ Batch requests when possible

## 🚀 Production Deployment

### Railway.app (Recommended)
```bash
# 1. Install Railway CLI
npm i -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
cd C:\Coding\Web\backend
railway init

# 4. Add environment variables
railway variables set AMADEUS_API_KEY=your_key
railway variables set AMADEUS_API_SECRET=your_secret

# 5. Deploy
railway up
```

### Render.com
1. Connect GitHub repo
2. Set environment variables in dashboard
3. Deploy automatically on push

## 📚 Additional Resources

- **Amadeus Docs:** https://developers.amadeus.com/self-service
- **API Reference:** https://developers.amadeus.com/self-service/category/air
- **Python SDK:** https://github.com/amadeus4dev/amadeus-python
- **Code Examples:** https://github.com/amadeus4dev/amadeus-code-examples

## 💡 Next Steps

1. ✅ **Get API credentials** from Amadeus
2. ✅ **Update `.env`** file with your keys
3. ✅ **Test endpoints** using curl or browser
4. 🎨 **Update frontend** to use new endpoints
5. 🚀 **Deploy** to Railway/Render

**Ready to go!** Your DAA project now has real flight data! 🎉
