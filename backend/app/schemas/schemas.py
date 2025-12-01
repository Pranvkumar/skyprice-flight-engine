from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class CabinClassEnum(str, Enum):
    ECONOMY = "economy"
    PREMIUM_ECONOMY = "premium_economy"
    BUSINESS = "business"
    FIRST = "first"


class FlightSearchRequest(BaseModel):
    """Flight search request"""
    origin: str = Field(..., min_length=3, max_length=3, description="Origin IATA code")
    destination: str = Field(..., min_length=3, max_length=3, description="Destination IATA code")
    departure_date: datetime
    return_date: Optional[datetime] = None
    cabin_class: CabinClassEnum = CabinClassEnum.ECONOMY
    passengers: int = Field(1, ge=1, le=9)


class FlightResponse(BaseModel):
    """Flight information response"""
    id: int
    flight_number: str
    airline: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    duration_minutes: int
    current_price: float
    available_seats: int
    cabin_class: str
    is_direct: bool


class PricePredictionRequest(BaseModel):
    """Price prediction request"""
    flight_id: Optional[int] = None
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    departure_date: datetime
    airline: Optional[str] = None
    cabin_class: CabinClassEnum = CabinClassEnum.ECONOMY
    days_ahead: int = Field(7, ge=1, le=90, description="Forecast horizon in days")


class PricePredictionResponse(BaseModel):
    """Price prediction response"""
    flight_id: Optional[int]
    origin: str
    destination: str
    departure_date: datetime
    current_price: float
    predicted_prices: List[dict]  # List of {date, price, confidence}
    recommendation: str
    optimal_booking_date: datetime
    expected_savings: float
    confidence_score: float
    factors: dict


class PriceTrendAnalysis(BaseModel):
    """Price trend analysis"""
    route: str
    time_period: str
    avg_price: float
    min_price: float
    max_price: float
    price_volatility: float
    trend_direction: str  # "increasing", "decreasing", "stable"
    seasonality_detected: bool
    peak_periods: List[dict]


class DemandForecastResponse(BaseModel):
    """Demand forecast response"""
    route: str
    forecast_date: datetime
    predicted_demand: float
    predicted_occupancy: float
    confidence_interval: dict
    demand_level: str  # "low", "medium", "high"
    pricing_strategy: str


class RouteAnalytics(BaseModel):
    """Route analytics"""
    origin: str
    destination: str
    distance_km: float
    avg_flight_duration: int
    total_flights_per_day: int
    avg_price: float
    price_range: dict
    demand_score: float
    competition_level: str
    best_time_to_book: str


class OptimalPriceRecommendation(BaseModel):
    """Optimal price recommendation"""
    flight_id: int
    current_price: float
    recommended_price: float
    price_change_percentage: float
    expected_revenue_impact: float
    demand_elasticity: float
    confidence: float
    reasoning: List[str]
    

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    environment: str
    database: str
    timestamp: datetime
