"""
Unified Travel API Endpoints
Handles multi-modal travel search, booking, and management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.models import (
    Flight, Train, Bus, Hotel, CarRental, TravelBooking,
    TravelMode, TrainClass, HotelCategory, BusType, CarType
)
from app.schemas.travel import (
    TravelSearchRequest, TravelSearchResponse,
    BookingCreate, BookingResponse,
    TravelPackageRequest, TravelPackageResponse
)

router = APIRouter()


@router.post("/search", response_model=TravelSearchResponse)
async def search_travel_options(
    search_request: TravelSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Universal travel search across all modes (flights, trains, buses, hotels, cars)
    """
    results = {
        "flights": [],
        "trains": [],
        "buses": [],
        "hotels": [],
        "car_rentals": []
    }
    
    # Search flights
    if not search_request.travel_modes or TravelMode.FLIGHT in search_request.travel_modes:
        flight_query = select(Flight).where(
            and_(
                Flight.origin == search_request.origin,
                Flight.destination == search_request.destination,
                Flight.departure_time >= search_request.departure_date,
                Flight.departure_time < search_request.departure_date + timedelta(days=1),
                Flight.available_seats >= search_request.passenger_count
            )
        )
        flights = await db.execute(flight_query)
        results["flights"] = flights.scalars().all()
    
    # Search trains
    if not search_request.travel_modes or TravelMode.TRAIN in search_request.travel_modes:
        train_query = select(Train).where(
            and_(
                Train.origin_station == search_request.origin,
                Train.destination_station == search_request.destination,
                Train.departure_time >= search_request.departure_date,
                Train.departure_time < search_request.departure_date + timedelta(days=1),
                Train.available_seats >= search_request.passenger_count
            )
        )
        trains = await db.execute(train_query)
        results["trains"] = trains.scalars().all()
    
    # Search buses
    if not search_request.travel_modes or TravelMode.BUS in search_request.travel_modes:
        bus_query = select(Bus).where(
            and_(
                Bus.origin_city == search_request.origin,
                Bus.destination_city == search_request.destination,
                Bus.departure_time >= search_request.departure_date,
                Bus.departure_time < search_request.departure_date + timedelta(days=1),
                Bus.available_seats >= search_request.passenger_count
            )
        )
        buses = await db.execute(bus_query)
        results["buses"] = buses.scalars().all()
    
    # Search hotels
    if not search_request.travel_modes or TravelMode.HOTEL in search_request.travel_modes:
        if search_request.destination:
            hotel_query = select(Hotel).where(
                Hotel.city == search_request.destination
            )
            if search_request.hotel_category:
                hotel_query = hotel_query.where(Hotel.category == search_request.hotel_category)
            
            hotels = await db.execute(hotel_query)
            results["hotels"] = hotels.scalars().all()
    
    # Search car rentals
    if not search_request.travel_modes or TravelMode.CAR_RENTAL in search_request.travel_modes:
        if search_request.origin or search_request.destination:
            pickup_city = search_request.origin or search_request.destination
            car_query = select(CarRental).where(
                and_(
                    CarRental.pickup_city == pickup_city,
                    CarRental.is_available == True
                )
            )
            if search_request.car_type:
                car_query = car_query.where(CarRental.car_type == search_request.car_type)
            
            cars = await db.execute(car_query)
            results["car_rentals"] = cars.scalars().all()
    
    return TravelSearchResponse(**results)


@router.post("/book", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a unified booking for any travel mode
    """
    # Generate unique booking ID
    import uuid
    booking_id = f"BK{uuid.uuid4().hex[:10].upper()}"
    
    # Create booking based on travel mode
    booking = TravelBooking(
        booking_id=booking_id,
        user_email=booking_data.user_email,
        user_name=booking_data.user_name,
        user_phone=booking_data.user_phone,
        travel_mode=booking_data.travel_mode,
        travel_date=booking_data.travel_date,
        return_date=booking_data.return_date,
        passenger_count=booking_data.passenger_count,
        total_price=booking_data.total_price,
        base_price=booking_data.base_price,
        taxes=booking_data.taxes,
        discount=booking_data.discount,
        special_requests=booking_data.special_requests
    )
    
    # Set the appropriate foreign key based on travel mode
    if booking_data.travel_mode == TravelMode.FLIGHT:
        booking.flight_id = booking_data.item_id
    elif booking_data.travel_mode == TravelMode.TRAIN:
        booking.train_id = booking_data.item_id
    elif booking_data.travel_mode == TravelMode.BUS:
        booking.bus_id = booking_data.item_id
    elif booking_data.travel_mode == TravelMode.HOTEL:
        booking.hotel_id = booking_data.item_id
    elif booking_data.travel_mode == TravelMode.CAR_RENTAL:
        booking.car_rental_id = booking_data.item_id
    
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    
    return BookingResponse.from_orm(booking)


@router.get("/bookings/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get booking details by booking ID
    """
    query = select(TravelBooking).where(TravelBooking.booking_id == booking_id)
    result = await db.execute(query)
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return BookingResponse.from_orm(booking)


@router.get("/bookings/user/{user_email}", response_model=List[BookingResponse])
async def get_user_bookings(
    user_email: str,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all bookings for a user
    """
    query = select(TravelBooking).where(TravelBooking.user_email == user_email)
    
    if status:
        query = query.where(TravelBooking.status == status)
    
    query = query.order_by(TravelBooking.created_at.desc())
    
    result = await db.execute(query)
    bookings = result.scalars().all()
    
    return [BookingResponse.from_orm(b) for b in bookings]


@router.post("/package/create", response_model=TravelPackageResponse)
async def create_travel_package(
    package_request: TravelPackageRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a complete travel package (flight + hotel + car rental, etc.)
    """
    import uuid
    package_id = f"PKG{uuid.uuid4().hex[:10].upper()}"
    
    bookings = []
    total_package_price = 0
    
    # Book flight if requested
    if package_request.flight_id:
        flight_booking = TravelBooking(
            booking_id=f"BK{uuid.uuid4().hex[:10].upper()}",
            user_email=package_request.user_email,
            user_name=package_request.user_name,
            travel_mode=TravelMode.FLIGHT,
            flight_id=package_request.flight_id,
            travel_date=package_request.travel_date,
            return_date=package_request.return_date,
            passenger_count=package_request.passenger_count,
            total_price=package_request.flight_price,
            is_package=True,
            package_id=package_id
        )
        db.add(flight_booking)
        bookings.append(flight_booking)
        total_package_price += package_request.flight_price
    
    # Book hotel if requested
    if package_request.hotel_id:
        hotel_booking = TravelBooking(
            booking_id=f"BK{uuid.uuid4().hex[:10].upper()}",
            user_email=package_request.user_email,
            user_name=package_request.user_name,
            travel_mode=TravelMode.HOTEL,
            hotel_id=package_request.hotel_id,
            travel_date=package_request.check_in_date,
            return_date=package_request.check_out_date,
            passenger_count=package_request.passenger_count,
            total_price=package_request.hotel_price,
            is_package=True,
            package_id=package_id
        )
        db.add(hotel_booking)
        bookings.append(hotel_booking)
        total_package_price += package_request.hotel_price
    
    # Book car rental if requested
    if package_request.car_rental_id:
        car_booking = TravelBooking(
            booking_id=f"BK{uuid.uuid4().hex[:10].upper()}",
            user_email=package_request.user_email,
            user_name=package_request.user_name,
            travel_mode=TravelMode.CAR_RENTAL,
            car_rental_id=package_request.car_rental_id,
            travel_date=package_request.travel_date,
            return_date=package_request.return_date,
            passenger_count=package_request.passenger_count,
            total_price=package_request.car_rental_price,
            is_package=True,
            package_id=package_id
        )
        db.add(car_booking)
        bookings.append(car_booking)
        total_package_price += package_request.car_rental_price
    
    # Apply package discount (10% for packages)
    package_discount = total_package_price * 0.10
    final_price = total_package_price - package_discount
    
    await db.commit()
    
    return TravelPackageResponse(
        package_id=package_id,
        bookings=[BookingResponse.from_orm(b) for b in bookings],
        total_price=total_package_price,
        discount=package_discount,
        final_price=final_price
    )


@router.delete("/bookings/{booking_id}")
async def cancel_booking(
    booking_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Cancel a booking
    """
    query = select(TravelBooking).where(TravelBooking.booking_id == booking_id)
    result = await db.execute(query)
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    booking.status = "cancelled"
    await db.commit()
    
    return {"message": "Booking cancelled successfully", "booking_id": booking_id}


@router.get("/compare")
async def compare_travel_modes(
    origin: str,
    destination: str,
    travel_date: datetime,
    passenger_count: int = 1,
    db: AsyncSession = Depends(get_db)
):
    """
    Compare prices and durations across all travel modes
    """
    comparison = {
        "origin": origin,
        "destination": destination,
        "date": travel_date,
        "options": []
    }
    
    # Get flights
    flight_query = select(Flight).where(
        and_(
            Flight.origin == origin,
            Flight.destination == destination,
            Flight.departure_time >= travel_date,
            Flight.departure_time < travel_date + timedelta(days=1)
        )
    ).limit(3)
    flights = (await db.execute(flight_query)).scalars().all()
    
    for flight in flights:
        comparison["options"].append({
            "mode": "flight",
            "provider": flight.airline,
            "duration_minutes": flight.duration_minutes,
            "price": flight.base_price,
            "departure": flight.departure_time,
            "id": flight.id
        })
    
    # Get trains
    train_query = select(Train).where(
        and_(
            Train.origin_station == origin,
            Train.destination_station == destination,
            Train.departure_time >= travel_date,
            Train.departure_time < travel_date + timedelta(days=1)
        )
    ).limit(3)
    trains = (await db.execute(train_query)).scalars().all()
    
    for train in trains:
        comparison["options"].append({
            "mode": "train",
            "provider": train.railway_operator,
            "duration_minutes": train.duration_minutes,
            "price": train.base_price,
            "departure": train.departure_time,
            "id": train.id
        })
    
    # Get buses
    bus_query = select(Bus).where(
        and_(
            Bus.origin_city == origin,
            Bus.destination_city == destination,
            Bus.departure_time >= travel_date,
            Bus.departure_time < travel_date + timedelta(days=1)
        )
    ).limit(3)
    buses = (await db.execute(bus_query)).scalars().all()
    
    for bus in buses:
        comparison["options"].append({
            "mode": "bus",
            "provider": bus.operator_name,
            "duration_minutes": bus.duration_minutes,
            "price": bus.base_price,
            "departure": bus.departure_time,
            "id": bus.id
        })
    
    # Sort by price
    comparison["options"].sort(key=lambda x: x["price"])
    
    return comparison
