from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Index, Enum, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class CabinClass(str, enum.Enum):
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium_economy"
    BUSINESS = "business"
    FIRST = "first"


class FlightStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TrainClass(str, enum.Enum):
    SLEEPER = "sleeper"
    AC_3_TIER = "ac_3_tier"
    AC_2_TIER = "ac_2_tier"
    AC_1_TIER = "ac_1_tier"
    GENERAL = "general"
    EXECUTIVE = "executive"


class HotelCategory(str, enum.Enum):
    BUDGET = "budget"
    THREE_STAR = "three_star"
    FOUR_STAR = "four_star"
    FIVE_STAR = "five_star"
    LUXURY = "luxury"


class RoomType(str, enum.Enum):
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"
    DELUXE = "deluxe"
    FAMILY = "family"


class BusType(str, enum.Enum):
    SEATER = "seater"
    SLEEPER = "sleeper"
    AC = "ac"
    NON_AC = "non_ac"
    VOLVO = "volvo"
    LUXURY = "luxury"


class CarType(str, enum.Enum):
    SEDAN = "sedan"
    SUV = "suv"
    HATCHBACK = "hatchback"
    LUXURY = "luxury"
    VAN = "van"


class TravelMode(str, enum.Enum):
    FLIGHT = "flight"
    TRAIN = "train"
    BUS = "bus"
    HOTEL = "hotel"
    CAR_RENTAL = "car_rental"


class Flight(Base):
    """Flight model"""
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String(20), unique=True, nullable=False, index=True)
    airline = Column(String(100), nullable=False, index=True)
    aircraft_type = Column(String(50))
    
    # Route information
    origin = Column(String(3), nullable=False, index=True)  # IATA code
    destination = Column(String(3), nullable=False, index=True)
    origin_city = Column(String(100))
    destination_city = Column(String(100))
    
    # Timing
    departure_time = Column(DateTime, nullable=False, index=True)
    arrival_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer)
    
    # Capacity
    total_seats = Column(Integer, default=180)
    available_seats = Column(Integer)
    cabin_class = Column(Enum(CabinClass), default=CabinClass.ECONOMY)
    
    # Status
    status = Column(Enum(FlightStatus), default=FlightStatus.SCHEDULED, index=True)
    is_direct = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    prices = relationship("FlightPrice", back_populates="flight", cascade="all, delete-orphan")
    bookings = relationship("TravelBooking", back_populates="flight")
    
    # Indexes
    __table_args__ = (
        Index('idx_route', 'origin', 'destination'),
        Index('idx_departure_date', 'departure_time'),
        Index('idx_airline_route', 'airline', 'origin', 'destination'),
    )


class FlightPrice(Base):
    """Historical and predicted flight prices"""
    __tablename__ = "flight_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False, index=True)
    
    # Price information
    base_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    predicted_price = Column(Float)
    competitor_avg_price = Column(Float)
    
    # Pricing factors
    demand_multiplier = Column(Float, default=1.0)
    seasonality_factor = Column(Float, default=1.0)
    time_to_departure_days = Column(Integer)
    occupancy_rate = Column(Float)
    
    # Confidence metrics
    prediction_confidence = Column(Float)
    forecast_horizon_days = Column(Integer)
    
    # Metadata
    model_version = Column(String(50))
    segment_id = Column(String(100), index=True)
    
    # Timestamps
    price_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    valid_until = Column(DateTime(timezone=True))
    
    # Relationships
    flight = relationship("Flight", back_populates="prices")
    
    __table_args__ = (
        Index('idx_flight_date', 'flight_id', 'price_date'),
        Index('idx_segment', 'segment_id', 'price_date'),
    )


class Route(Base):
    """Route analytics and metadata"""
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(3), nullable=False, index=True)
    destination = Column(String(3), nullable=False, index=True)
    
    # Route characteristics
    distance_km = Column(Float)
    average_duration_minutes = Column(Integer)
    is_international = Column(Boolean, default=False)
    is_popular = Column(Boolean, default=False)
    
    # Demand analytics
    avg_daily_searches = Column(Integer, default=0)
    avg_daily_bookings = Column(Integer, default=0)
    peak_season_months = Column(JSON)  # List of peak months
    
    # Price statistics
    historical_avg_price = Column(Float)
    price_volatility = Column(Float)
    min_observed_price = Column(Float)
    max_observed_price = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_route_pair', 'origin', 'destination', unique=True),
    )


class DemandForecast(Base):
    """Demand forecasting data"""
    __tablename__ = "demand_forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Segment information
    route = Column(String(10), nullable=False, index=True)  # e.g., "BOM-DEL"
    airline = Column(String(100), index=True)
    forecast_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Forecast values
    predicted_demand = Column(Float)
    predicted_bookings = Column(Integer)
    predicted_occupancy = Column(Float)
    
    # Confidence
    confidence_lower = Column(Float)
    confidence_upper = Column(Float)
    confidence_level = Column(Float, default=0.95)
    
    # Model metadata
    model_type = Column(String(50))
    features_used = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_route_forecast_date', 'route', 'forecast_date'),
    )


class ExternalFactor(Base):
    """External factors affecting pricing"""
    __tablename__ = "external_factors"
    
    id = Column(Integer, primary_key=True, index=True)
    factor_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Economic factors
    fuel_price_per_gallon = Column(Float)
    exchange_rate = Column(Float)
    inflation_rate = Column(Float)
    
    # Events and seasonality
    is_holiday = Column(Boolean, default=False)
    is_peak_season = Column(Boolean, default=False)
    special_event = Column(String(200))
    weather_impact_score = Column(Float)
    
    # Competition
    competitor_count = Column(Integer)
    market_share = Column(Float)
    
    # Additional metadata
    additional_metadata = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Train(Base):
    """Train model for railway bookings"""
    __tablename__ = "trains"
    
    id = Column(Integer, primary_key=True, index=True)
    train_number = Column(String(20), unique=True, nullable=False, index=True)
    train_name = Column(String(200), nullable=False)
    railway_operator = Column(String(100))  # Indian Railways, Amtrak, etc.
    
    # Route information
    origin_station = Column(String(10), nullable=False, index=True)  # Station code
    destination_station = Column(String(10), nullable=False, index=True)
    origin_city = Column(String(100))
    destination_city = Column(String(100))
    
    # Timing
    departure_time = Column(DateTime, nullable=False, index=True)
    arrival_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer)
    
    # Capacity and class
    train_class = Column(Enum(TrainClass), default=TrainClass.SLEEPER)
    total_seats = Column(Integer, default=72)
    available_seats = Column(Integer)
    
    # Pricing and features
    base_price = Column(Float, nullable=False)
    has_food = Column(Boolean, default=True)
    has_wifi = Column(Boolean, default=False)
    is_express = Column(Boolean, default=False)
    
    # Relationships
    prices = relationship("TrainPrice", back_populates="train")
    bookings = relationship("TravelBooking", back_populates="train")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_train_route', 'origin_station', 'destination_station'),
        Index('idx_train_departure', 'departure_time'),
    )


class TrainPrice(Base):
    """Historical train pricing data"""
    __tablename__ = "train_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    train_id = Column(Integer, ForeignKey("trains.id"), nullable=False)
    
    # Pricing details
    price = Column(Float, nullable=False)
    train_class = Column(Enum(TrainClass))
    booking_date = Column(DateTime(timezone=True), nullable=False, index=True)
    travel_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Demand metrics
    seats_sold = Column(Integer, default=0)
    occupancy_rate = Column(Float)
    
    train = relationship("Train", back_populates="prices")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Hotel(Base):
    """Hotel model for accommodation bookings"""
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String(200), nullable=False, index=True)
    hotel_chain = Column(String(100))  # Marriott, Hilton, etc.
    
    # Location
    city = Column(String(100), nullable=False, index=True)
    area = Column(String(200))
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Category and rating
    category = Column(Enum(HotelCategory), default=HotelCategory.THREE_STAR)
    star_rating = Column(Float)  # 1.0 to 5.0
    guest_rating = Column(Float)  # User reviews
    
    # Facilities
    has_wifi = Column(Boolean, default=True)
    has_pool = Column(Boolean, default=False)
    has_gym = Column(Boolean, default=False)
    has_restaurant = Column(Boolean, default=True)
    has_parking = Column(Boolean, default=True)
    has_spa = Column(Boolean, default=False)
    
    # Rooms
    total_rooms = Column(Integer, default=100)
    
    # Relationships
    rooms = relationship("HotelRoom", back_populates="hotel")
    bookings = relationship("TravelBooking", back_populates="hotel")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class HotelRoom(Base):
    """Hotel room inventory and pricing"""
    __tablename__ = "hotel_rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    
    # Room details
    room_type = Column(Enum(RoomType), nullable=False)
    room_count = Column(Integer, default=1)
    available_rooms = Column(Integer)
    max_occupancy = Column(Integer, default=2)
    
    # Pricing
    base_price_per_night = Column(Float, nullable=False)
    weekend_price = Column(Float)
    peak_season_price = Column(Float)
    
    # Dates
    check_in_date = Column(DateTime(timezone=True), index=True)
    check_out_date = Column(DateTime(timezone=True), index=True)
    
    # Features
    has_breakfast = Column(Boolean, default=False)
    is_refundable = Column(Boolean, default=True)
    
    hotel = relationship("Hotel", back_populates="rooms")
    prices = relationship("HotelPrice", back_populates="room")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HotelPrice(Base):
    """Historical hotel pricing data"""
    __tablename__ = "hotel_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("hotel_rooms.id"), nullable=False)
    
    # Pricing details
    price_per_night = Column(Float, nullable=False)
    booking_date = Column(DateTime(timezone=True), nullable=False, index=True)
    stay_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Demand metrics
    rooms_booked = Column(Integer, default=0)
    occupancy_rate = Column(Float)
    is_weekend = Column(Boolean, default=False)
    
    room = relationship("HotelRoom", back_populates="prices")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Bus(Base):
    """Bus model for road travel"""
    __tablename__ = "buses"
    
    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String(20), unique=True, nullable=False, index=True)
    operator_name = Column(String(200), nullable=False)
    
    # Route information
    origin_city = Column(String(100), nullable=False, index=True)
    destination_city = Column(String(100), nullable=False, index=True)
    route_stops = Column(JSON)  # List of intermediate stops
    
    # Timing
    departure_time = Column(DateTime, nullable=False, index=True)
    arrival_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer)
    
    # Bus details
    bus_type = Column(Enum(BusType), default=BusType.SEATER)
    total_seats = Column(Integer, default=40)
    available_seats = Column(Integer)
    
    # Pricing and features
    base_price = Column(Float, nullable=False)
    has_charging = Column(Boolean, default=False)
    has_wifi = Column(Boolean, default=False)
    has_entertainment = Column(Boolean, default=False)
    
    # Relationships
    prices = relationship("BusPrice", back_populates="bus")
    bookings = relationship("TravelBooking", back_populates="bus")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_bus_route', 'origin_city', 'destination_city'),
        Index('idx_bus_departure', 'departure_time'),
    )


class BusPrice(Base):
    """Historical bus pricing data"""
    __tablename__ = "bus_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    bus_id = Column(Integer, ForeignKey("buses.id"), nullable=False)
    
    # Pricing details
    price = Column(Float, nullable=False)
    booking_date = Column(DateTime(timezone=True), nullable=False, index=True)
    travel_date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Demand metrics
    seats_sold = Column(Integer, default=0)
    occupancy_rate = Column(Float)
    
    bus = relationship("Bus", back_populates="prices")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CarRental(Base):
    """Car rental model"""
    __tablename__ = "car_rentals"
    
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(String(50), unique=True, nullable=False, index=True)
    rental_company = Column(String(200), nullable=False)
    
    # Car details
    car_type = Column(Enum(CarType), nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    year = Column(Integer)
    
    # Location
    pickup_city = Column(String(100), nullable=False, index=True)
    pickup_location = Column(String(200))
    dropoff_city = Column(String(100))
    dropoff_location = Column(String(200))
    
    # Pricing
    price_per_day = Column(Float, nullable=False)
    price_per_hour = Column(Float)
    insurance_per_day = Column(Float)
    
    # Features
    seating_capacity = Column(Integer, default=5)
    has_gps = Column(Boolean, default=True)
    has_driver = Column(Boolean, default=False)
    fuel_type = Column(String(20))  # Petrol, Diesel, Electric, Hybrid
    
    # Availability
    is_available = Column(Boolean, default=True)
    total_cars = Column(Integer, default=1)
    
    # Relationships
    prices = relationship("CarRentalPrice", back_populates="car")
    bookings = relationship("TravelBooking", back_populates="car_rental")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CarRentalPrice(Base):
    """Historical car rental pricing data"""
    __tablename__ = "car_rental_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("car_rentals.id"), nullable=False)
    
    # Pricing details
    price_per_day = Column(Float, nullable=False)
    booking_date = Column(DateTime(timezone=True), nullable=False, index=True)
    rental_start_date = Column(DateTime(timezone=True), nullable=False, index=True)
    rental_duration_days = Column(Integer)
    
    # Demand metrics
    bookings_count = Column(Integer, default=0)
    utilization_rate = Column(Float)
    
    car = relationship("CarRental", back_populates="prices")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TravelBooking(Base):
    """Unified booking model for all travel types"""
    __tablename__ = "travel_bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # User information
    user_email = Column(String(255), nullable=False, index=True)
    user_name = Column(String(200))
    user_phone = Column(String(20))
    
    # Travel mode (what type of booking)
    travel_mode = Column(Enum(TravelMode), nullable=False, index=True)
    
    # Foreign keys to different travel types (only one will be used)
    flight_id = Column(Integer, ForeignKey("flights.id"))
    train_id = Column(Integer, ForeignKey("trains.id"))
    bus_id = Column(Integer, ForeignKey("buses.id"))
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    car_rental_id = Column(Integer, ForeignKey("car_rentals.id"))
    
    # Booking details
    booking_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    travel_date = Column(DateTime(timezone=True), nullable=False)
    return_date = Column(DateTime(timezone=True))  # For round trips or hotel stays
    
    # Passengers/guests
    passenger_count = Column(Integer, default=1)
    
    # Pricing
    total_price = Column(Float, nullable=False)
    base_price = Column(Float)
    taxes = Column(Float)
    discount = Column(Float, default=0)
    
    # Status
    status = Column(String(50), default="confirmed")  # confirmed, cancelled, completed
    payment_status = Column(String(50), default="pending")
    
    # Package information (if part of a bundle)
    is_package = Column(Boolean, default=False)
    package_id = Column(String(50))
    
    # Additional data
    special_requests = Column(Text)
    booking_metadata = Column(JSON)
    
    # Relationships
    flight = relationship("Flight", back_populates="bookings")
    train = relationship("Train", back_populates="bookings")
    bus = relationship("Bus", back_populates="bookings")
    hotel = relationship("Hotel", back_populates="bookings")
    car_rental = relationship("CarRental", back_populates="bookings")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_booking_user', 'user_email'),
        Index('idx_booking_travel_date', 'travel_date'),
        Index('idx_booking_mode', 'travel_mode'),
    )
