from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from typing import Optional

from app.core.database import get_db
from app.models.models import FlightPrice, Flight, DemandForecast, TravelBooking
from app.schemas.schemas import PriceTrendAnalysis, DemandForecastResponse
from app.services.analytics.trend_analyzer import TrendAnalyzer

router = APIRouter()


@router.get("/trends")
async def get_price_trends(
    origin: str = Query(..., min_length=3, max_length=3),
    destination: str = Query(..., min_length=3, max_length=3),
    days: int = Query(30, ge=7, le=365),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze price trends for a route
    """
    analyzer = TrendAnalyzer(db)
    
    trends = await analyzer.analyze_route_trends(
        origin=origin,
        destination=destination,
        days_back=days
    )
    
    return trends


@router.get("/demand")
async def get_demand_patterns(
    route: Optional[str] = Query(None),
    airline: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Get demand forecasting data
    """
    query = select(DemandForecast)
    
    if route:
        query = query.where(DemandForecast.route == route)
    if airline:
        query = query.where(DemandForecast.airline == airline)
    if start_date:
        query = query.where(DemandForecast.forecast_date >= start_date)
    if end_date:
        query = query.where(DemandForecast.forecast_date <= end_date)
    
    query = query.order_by(DemandForecast.forecast_date.desc()).limit(100)
    
    result = await db.execute(query)
    forecasts = result.scalars().all()
    
    return [
        {
            "route": f.route,
            "airline": f.airline,
            "forecast_date": f.forecast_date,
            "predicted_demand": f.predicted_demand,
            "predicted_occupancy": f.predicted_occupancy,
            "confidence_interval": {
                "lower": f.confidence_lower,
                "upper": f.confidence_upper
            }
        }
        for f in forecasts
    ]


@router.get("/competitors")
async def get_competitor_analysis(
    origin: str = Query(..., min_length=3, max_length=3),
    destination: str = Query(..., min_length=3, max_length=3),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze competitor pricing for a route
    """
    # Get all airlines on this route
    query = select(
        Flight.airline,
        func.count(Flight.id).label('flight_count'),
        func.avg(FlightPrice.current_price).label('avg_price'),
        func.min(FlightPrice.current_price).label('min_price'),
        func.max(FlightPrice.current_price).label('max_price')
    ).join(FlightPrice).where(
        and_(
            Flight.origin == origin.upper(),
            Flight.destination == destination.upper()
        )
    ).group_by(Flight.airline)
    
    result = await db.execute(query)
    competitors = result.all()
    
    return {
        "route": f"{origin}-{destination}",
        "competitors": [
            {
                "airline": c.airline,
                "flight_count": c.flight_count,
                "avg_price": float(c.avg_price) if c.avg_price else 0,
                "min_price": float(c.min_price) if c.min_price else 0,
                "max_price": float(c.max_price) if c.max_price else 0
            }
            for c in competitors
        ],
        "market_leader": max(competitors, key=lambda x: x.flight_count).airline if competitors else None
    }


@router.get("/seasonality/{route}")
async def get_seasonality_analysis(
    route: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze seasonal pricing patterns
    """
    try:
        origin, destination = route.split('-')
    except:
        raise HTTPException(status_code=400, detail="Invalid route format")
    
    analyzer = TrendAnalyzer(db)
    seasonality = await analyzer.analyze_seasonality(origin, destination)
    
    return seasonality


@router.get("/dashboard")
async def get_analytics_dashboard(
    db: AsyncSession = Depends(get_db)
):
    """
    Get comprehensive analytics dashboard data
    """
    # Total flights
    total_flights_query = select(func.count(Flight.id))
    total_flights = (await db.execute(total_flights_query)).scalar()
    
    # Total bookings
    total_bookings_query = select(func.count(TravelBooking.id))
    total_bookings = (await db.execute(total_bookings_query)).scalar()
    
    # Average price
    avg_price_query = select(func.avg(FlightPrice.current_price))
    avg_price = (await db.execute(avg_price_query)).scalar()
    
    # Top routes
    top_routes_query = select(
        Flight.origin,
        Flight.destination,
        func.count(Flight.id).label('count')
    ).group_by(Flight.origin, Flight.destination).order_by(func.count(Flight.id).desc()).limit(5)
    
    top_routes_result = await db.execute(top_routes_query)
    top_routes = top_routes_result.all()
    
    return {
        "total_flights": total_flights,
        "total_bookings": total_bookings,
        "average_price": float(avg_price) if avg_price else 0,
        "top_routes": [
            {"route": f"{r.origin}-{r.destination}", "flights": r.count}
            for r in top_routes
        ],
        "last_updated": datetime.utcnow()
    }
