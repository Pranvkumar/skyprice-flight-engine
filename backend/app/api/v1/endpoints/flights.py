from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.models import Flight, FlightPrice
from app.schemas.schemas import FlightSearchRequest, FlightResponse

router = APIRouter()


@router.get("/search", response_model=List[FlightResponse])
async def search_flights(
    origin: str = Query(..., min_length=3, max_length=3),
    destination: str = Query(..., min_length=3, max_length=3),
    departure_date: datetime = Query(...),
    passengers: int = Query(1, ge=1, le=9),
    cabin_class: str = Query("economy"),
    db: AsyncSession = Depends(get_db)
):
    """
    Search for available flights
    """
    # Query flights
    query = select(Flight).where(
        and_(
            Flight.origin == origin.upper(),
            Flight.destination == destination.upper(),
            Flight.departure_time >= departure_date,
            Flight.departure_time < departure_date + timedelta(days=1),
            Flight.available_seats >= passengers,
            Flight.status == "scheduled"
        )
    ).order_by(Flight.departure_time)
    
    result = await db.execute(query)
    flights = result.scalars().all()
    
    # Get current prices
    flight_responses = []
    for flight in flights:
        # Get latest price
        price_query = select(FlightPrice).where(
            FlightPrice.flight_id == flight.id
        ).order_by(FlightPrice.price_date.desc()).limit(1)
        
        price_result = await db.execute(price_query)
        price = price_result.scalar_one_or_none()
        
        flight_responses.append(FlightResponse(
            id=flight.id,
            flight_number=flight.flight_number,
            airline=flight.airline,
            origin=flight.origin,
            destination=flight.destination,
            departure_time=flight.departure_time,
            arrival_time=flight.arrival_time,
            duration_minutes=flight.duration_minutes,
            current_price=price.current_price if price else 0.0,
            available_seats=flight.available_seats,
            cabin_class=flight.cabin_class.value,
            is_direct=flight.is_direct
        ))
    
    return flight_responses


@router.get("/{flight_id}", response_model=FlightResponse)
async def get_flight(
    flight_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed flight information
    """
    query = select(Flight).where(Flight.id == flight_id)
    result = await db.execute(query)
    flight = result.scalar_one_or_none()
    
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # Get current price
    price_query = select(FlightPrice).where(
        FlightPrice.flight_id == flight_id
    ).order_by(FlightPrice.price_date.desc()).limit(1)
    
    price_result = await db.execute(price_query)
    price = price_result.scalar_one_or_none()
    
    return FlightResponse(
        id=flight.id,
        flight_number=flight.flight_number,
        airline=flight.airline,
        origin=flight.origin,
        destination=flight.destination,
        departure_time=flight.departure_time,
        arrival_time=flight.arrival_time,
        duration_minutes=flight.duration_minutes,
        current_price=price.current_price if price else 0.0,
        available_seats=flight.available_seats,
        cabin_class=flight.cabin_class.value,
        is_direct=flight.is_direct
    )


@router.post("/compare")
async def compare_flights(
    flight_ids: List[int],
    db: AsyncSession = Depends(get_db)
):
    """
    Compare multiple flights side by side
    """
    comparisons = []
    
    for flight_id in flight_ids:
        try:
            flight = await get_flight(flight_id, db)
            comparisons.append(flight)
        except HTTPException:
            continue
    
    return {
        "flights": comparisons,
        "count": len(comparisons),
        "cheapest": min(comparisons, key=lambda x: x.current_price) if comparisons else None
    }


@router.get("/popular/routes")
async def get_popular_routes(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """
    Get most popular flight routes
    """
    from sqlalchemy import func
    
    query = select(
        Flight.origin,
        Flight.destination,
        func.count(Flight.id).label('flight_count'),
        func.avg(FlightPrice.current_price).label('avg_price')
    ).join(FlightPrice).group_by(
        Flight.origin, Flight.destination
    ).order_by(func.count(Flight.id).desc()).limit(limit)
    
    result = await db.execute(query)
    routes = result.all()
    
    return [
        {
            "route": f"{r.origin}-{r.destination}",
            "origin": r.origin,
            "destination": r.destination,
            "flight_count": r.flight_count,
            "avg_price": float(r.avg_price) if r.avg_price else 0
        }
        for r in routes
    ]
