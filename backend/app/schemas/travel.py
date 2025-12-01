"""
Pydantic schemas for unified travel system
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.models import TravelMode, TrainClass, HotelCategory, BusType, CarType


class TravelSearchRequest(BaseModel):
    """Request for searching travel options"""
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_date: datetime
    return_date: Optional[datetime] = None
    passenger_count: int = Field(default=1, ge=1)
    travel_modes: Optional[List[TravelMode]] = None
    
    # Optional filters
    hotel_category: Optional[HotelCategory] = None
    car_type: Optional[CarType] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None


class TravelSearchResponse(BaseModel):
    """Response with all available travel options"""
    flights: List[dict] = []
    trains: List[dict] = []
    buses: List[dict] = []
    hotels: List[dict] = []
    car_rentals: List[dict] = []
    
    class Config:
        from_attributes = True


class BookingCreate(BaseModel):
    """Create a new booking"""
    user_email: EmailStr
    user_name: str
    user_phone: Optional[str] = None
    
    travel_mode: TravelMode
    item_id: int  # ID of flight/train/bus/hotel/car
    
    travel_date: datetime
    return_date: Optional[datetime] = None
    passenger_count: int = Field(default=1, ge=1)
    
    total_price: float
    base_price: Optional[float] = None
    taxes: Optional[float] = None
    discount: float = Field(default=0.0, ge=0)
    
    special_requests: Optional[str] = None


class BookingResponse(BaseModel):
    """Booking response"""
    id: int
    booking_id: str
    user_email: str
    user_name: Optional[str]
    
    travel_mode: TravelMode
    travel_date: datetime
    return_date: Optional[datetime]
    
    passenger_count: int
    total_price: float
    
    status: str
    payment_status: str
    
    is_package: bool
    package_id: Optional[str]
    
    created_at: datetime
    
    class Config:
        from_attributes = True


class TravelPackageRequest(BaseModel):
    """Request to create a travel package"""
    user_email: EmailStr
    user_name: str
    user_phone: Optional[str] = None
    
    # Flight details
    flight_id: Optional[int] = None
    flight_price: float = 0.0
    
    # Hotel details
    hotel_id: Optional[int] = None
    hotel_price: float = 0.0
    check_in_date: Optional[datetime] = None
    check_out_date: Optional[datetime] = None
    
    # Car rental details
    car_rental_id: Optional[int] = None
    car_rental_price: float = 0.0
    
    # Common details
    travel_date: datetime
    return_date: Optional[datetime] = None
    passenger_count: int = Field(default=1, ge=1)


class TravelPackageResponse(BaseModel):
    """Response for travel package"""
    package_id: str
    bookings: List[BookingResponse]
    total_price: float
    discount: float
    final_price: float
    
    class Config:
        from_attributes = True


class PriceComparisonRequest(BaseModel):
    """Request for price comparison across modes"""
    origin: str
    destination: str
    travel_date: datetime
    return_date: Optional[datetime] = None
    passenger_count: int = 1


class PriceComparisonResponse(BaseModel):
    """Price comparison response"""
    cheapest_option: dict
    fastest_option: dict
    best_value: dict
    all_options: List[dict]
