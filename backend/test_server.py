"""
Simple FastAPI test server for Amadeus API
Minimal dependencies - just test the Amadeus integration
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import sys
import os
from datetime import datetime, timedelta

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment
from dotenv import load_dotenv
load_dotenv('.env')

# Import Amadeus client
from app.services.data_sources.amadeus_client import AmadeusFlightClient

# Create FastAPI app
app = FastAPI(
    title="Flight Price API - Test Server",
    description="Testing Amadeus API Integration",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Amadeus client
amadeus_client = AmadeusFlightClient()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.get("/api")
async def api_info():
    """API root - health check"""
    return {
        "status": "online",
        "message": "Amadeus Flight API Test Server",
        "amadeus_env": os.getenv('AMADEUS_ENVIRONMENT', 'test'),
        "endpoints": {
            "airport_search": "/airports?query=Paris",
            "flight_search": "/flights?origin=PAR&destination=LON&date=2025-12-15",
            "health": "/health"
        }
    }

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "amadeus_configured": bool(os.getenv('AMADEUS_API_KEY'))
    }

@app.get("/airports")
async def search_airports(query: str = Query(..., description="City name or IATA code")):
    """Search for airports"""
    try:
        airports = amadeus_client.search_airports(query, max_results=10)
        return {
            "success": True,
            "query": query,
            "count": len(airports),
            "airports": airports
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/flights")
async def search_flights(
    origin: str = Query(..., description="Origin IATA code (e.g., PAR)"),
    destination: str = Query(..., description="Destination IATA code (e.g., LON)"),
    date: Optional[str] = Query(None, description="Departure date YYYY-MM-DD")
):
    """Search for flights"""
    # Default to 2 weeks from now if no date provided
    if not date:
        date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    
    try:
        flights = amadeus_client.search_flights(origin, destination, date, max_results=10)
        
        if not flights:
            return {
                "success": True,
                "message": "No flights found for this route",
                "route": f"{origin} → {destination}",
                "date": date,
                "flights": []
            }
        
        # Calculate price stats
        prices = [f['price'] for f in flights]
        
        return {
            "success": True,
            "route": f"{origin} → {destination}",
            "date": date,
            "count": len(flights),
            "price_stats": {
                "lowest": min(prices),
                "highest": max(prices),
                "average": sum(prices) / len(prices),
                "currency": flights[0]['currency']
            },
            "flights": flights
        }
    except Exception as e:
        error_msg = str(e)
        
        # Handle test environment limitations gracefully
        if "[400]" in error_msg or "[401]" in error_msg:
            return {
                "success": False,
                "error": "Route not available in test environment",
                "message": "This route may not be supported in the Amadeus test environment. Try PAR→LON or NYC→LAX",
                "test_mode": True
            }
        
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": error_msg}
        )

@app.get("/price-analysis")
async def get_price_analysis(
    origin: str = Query(..., description="Origin IATA code"),
    destination: str = Query(..., description="Destination IATA code"),
    date: Optional[str] = Query(None, description="Departure date")
):
    """Get price analysis for route"""
    if not date:
        date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    
    try:
        analysis = amadeus_client.get_flight_price_analysis(origin, destination, date)
        
        if analysis:
            return {
                "success": True,
                "route": f"{origin} → {destination}",
                "date": date,
                "analysis": analysis
            }
        else:
            return {
                "success": False,
                "message": "Price analysis not available (test environment limitation)"
            }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("Starting Amadeus Flight API Test Server")
    print("=" * 70)
    print(f"   URL: http://localhost:8000")
    print(f"   Docs: http://localhost:8000/docs")
    print(f"   Amadeus Environment: {os.getenv('AMADEUS_ENVIRONMENT', 'test')}")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

