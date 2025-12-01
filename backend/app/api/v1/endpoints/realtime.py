"""
Real-time flight data endpoints
Integrates Amadeus API for live pricing
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from app.services.data_sources.flight_data_service import get_flight_data_service

router = APIRouter()


@router.get("/live-prices")
async def get_live_prices(
    origin: str = Query(..., description="Origin airport IATA code (e.g., BOM)"),
    destination: str = Query(..., description="Destination airport IATA code (e.g., DEL)"),
    departure_date: str = Query(..., description="Departure date (YYYY-MM-DD)"),
    cabin_class: str = Query("ECONOMY", description="Cabin class: ECONOMY, BUSINESS, FIRST")
):
    """
    Get live flight prices from Amadeus API
    
    **Example:** `/api/v1/realtime/live-prices?origin=BOM&destination=DEL&departure_date=2025-12-15`
    """
    service = get_flight_data_service()
    
    try:
        prices = await service.get_live_prices(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            cabin_class=cabin_class
        )
        
        if not prices:
            raise HTTPException(
                status_code=404,
                detail="No flights found for this route and date"
            )
        
        return {
            "success": True,
            "route": f"{origin}-{destination}",
            "departure_date": departure_date,
            "flights": prices,
            "count": len(prices)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/price-trends")
async def get_price_trends(
    origin: str = Query(..., description="Origin airport IATA code"),
    destination: str = Query(..., description="Destination airport IATA code"),
    days_back: int = Query(30, ge=7, le=90, description="Days of historical data")
):
    """
    Get historical price trends for a route
    
    **Returns:** Historical prices, average, min, max, volatility
    """
    service = get_flight_data_service()
    
    try:
        trends = await service.get_price_trends(
            origin=origin,
            destination=destination,
            days_back=days_back
        )
        
        if 'error' in trends:
            raise HTTPException(status_code=404, detail=trends['error'])
        
        return {
            "success": True,
            "route": f"{origin}-{destination}",
            "data": trends
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/booking-recommendation")
async def get_booking_recommendation(
    origin: str = Query(..., description="Origin airport IATA code"),
    destination: str = Query(..., description="Destination airport IATA code"),
    target_date: str = Query(..., description="Target departure date (YYYY-MM-DD)")
):
    """
    Get recommendation for when to book
    
    **Returns:** Book now vs wait, cheapest dates, price analysis
    """
    service = get_flight_data_service()
    
    try:
        recommendation = await service.get_best_booking_time(
            origin=origin,
            destination=destination,
            target_date=target_date
        )
        
        if 'error' in recommendation:
            raise HTTPException(status_code=404, detail=recommendation['error'])
        
        return {
            "success": True,
            "recommendation": recommendation
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/route-insights")
async def get_route_insights(
    origin: str = Query(..., description="Origin airport IATA code"),
    destination: str = Query(..., description="Destination airport IATA code"),
    departure_date: str = Query(..., description="Departure date (YYYY-MM-DD)")
):
    """
    Get comprehensive route analysis
    
    **Combines:**
    - Live prices
    - Historical trends
    - Booking recommendations
    - Price statistics
    """
    service = get_flight_data_service()
    
    try:
        insights = await service.get_route_insights(
            origin=origin,
            destination=destination,
            departure_date=departure_date
        )
        
        if 'error' in insights:
            raise HTTPException(status_code=404, detail=insights['error'])
        
        return {
            "success": True,
            "insights": insights
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search-airports")
async def search_airports(
    keyword: str = Query(..., min_length=2, description="Search keyword (city or IATA code)")
):
    """
    Search airports for autocomplete
    
    **Example:** `/api/v1/realtime/search-airports?keyword=Mumbai`
    
    **Returns:** List of matching airports with IATA codes
    """
    service = get_flight_data_service()
    
    try:
        airports = await service.search_airports(keyword)
        
        return {
            "success": True,
            "keyword": keyword,
            "airports": airports,
            "count": len(airports)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Check if Amadeus API integration is working
    """
    try:
        service = get_flight_data_service()
        # Try a simple airport search to verify API is working
        result = await service.search_airports("Mumbai")
        
        return {
            "status": "healthy",
            "amadeus_api": "connected" if result else "error",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "amadeus_api": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
