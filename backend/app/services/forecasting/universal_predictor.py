"""
Universal Price Predictor for All Travel Modes
Extends the divide-and-conquer engine to handle flights, trains, buses, hotels, and car rentals
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.models import (
    Flight, FlightPrice, Train, TrainPrice, Bus, BusPrice,
    Hotel, HotelPrice, CarRental, CarRentalPrice, TravelMode
)
from app.services.forecasting.divide_conquer_engine import DivideAndConquerForecaster


class UniversalTravelPricePredictor:
    """
    Unified price prediction system for all travel modes
    Uses divide-and-conquer forecasting adapted for each travel type
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.forecaster = DivideAndConquerForecaster()
    
    async def predict_flight_price(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        cabin_class: str = "economy"
    ) -> Dict:
        """Predict flight price using historical data"""
        
        # Fetch historical flight prices
        query = select(FlightPrice).join(Flight).where(
            and_(
                Flight.origin == origin,
                Flight.destination == destination,
                Flight.cabin_class == cabin_class
            )
        ).order_by(FlightPrice.created_at)
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        if not prices:
            return {"error": "No historical data available"}
        
        # Convert to DataFrame
        df = pd.DataFrame([{
            'date': p.created_at,
            'price': p.current_price,
            'occupancy': p.occupancy_rate,
            'days_before': p.time_to_departure_days
        } for p in prices])
        
        # Apply divide-and-conquer forecasting
        forecast = self.forecaster.forecast(
            df,
            target_date=departure_date,
            features=['occupancy', 'days_before']
        )
        
        return {
            "travel_mode": "flight",
            "predicted_price": forecast['price'],
            "confidence": forecast['confidence'],
            "price_range": {
                "min": forecast['price'] * 0.90,
                "max": forecast['price'] * 1.10
            },
            "recommendation": self._get_recommendation(forecast['price'], df['price'].mean())
        }
    
    async def predict_train_price(
        self,
        origin_station: str,
        destination_station: str,
        travel_date: datetime,
        train_class: str = "sleeper"
    ) -> Dict:
        """Predict train price"""
        
        query = select(TrainPrice).join(Train).where(
            and_(
                Train.origin_station == origin_station,
                Train.destination_station == destination_station,
                Train.train_class == train_class
            )
        ).order_by(TrainPrice.created_at)
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        if not prices:
            # Fallback: use average train prices
            return {
                "travel_mode": "train",
                "predicted_price": 500.0,  # Default estimate
                "confidence": 0.3,
                "message": "Limited historical data"
            }
        
        df = pd.DataFrame([{
            'date': p.booking_date,
            'price': p.price,
            'occupancy': p.occupancy_rate,
            'seats_sold': p.seats_sold
        } for p in prices])
        
        forecast = self.forecaster.forecast(df, target_date=travel_date)
        
        return {
            "travel_mode": "train",
            "predicted_price": forecast['price'],
            "confidence": forecast['confidence'],
            "price_trend": self._calculate_trend(df['price']),
            "recommendation": self._get_recommendation(forecast['price'], df['price'].mean())
        }
    
    async def predict_bus_price(
        self,
        origin_city: str,
        destination_city: str,
        travel_date: datetime,
        bus_type: str = "seater"
    ) -> Dict:
        """Predict bus price"""
        
        query = select(BusPrice).join(Bus).where(
            and_(
                Bus.origin_city == origin_city,
                Bus.destination_city == destination_city,
                Bus.bus_type == bus_type
            )
        ).order_by(BusPrice.created_at)
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        if not prices:
            return {
                "travel_mode": "bus",
                "predicted_price": 300.0,
                "confidence": 0.3,
                "message": "Limited historical data"
            }
        
        df = pd.DataFrame([{
            'date': p.booking_date,
            'price': p.price,
            'occupancy': p.occupancy_rate
        } for p in prices])
        
        forecast = self.forecaster.forecast(df, target_date=travel_date)
        
        return {
            "travel_mode": "bus",
            "predicted_price": forecast['price'],
            "confidence": forecast['confidence'],
            "recommendation": self._get_recommendation(forecast['price'], df['price'].mean())
        }
    
    async def predict_hotel_price(
        self,
        city: str,
        check_in_date: datetime,
        check_out_date: datetime,
        hotel_category: str = "three_star",
        room_type: str = "double"
    ) -> Dict:
        """Predict hotel price per night"""
        
        # Calculate number of nights
        nights = (check_out_date - check_in_date).days
        
        query = select(HotelPrice).join(Hotel).where(
            and_(
                Hotel.city == city,
                Hotel.category == hotel_category
            )
        ).order_by(HotelPrice.created_at).limit(1000)
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        if not prices:
            # Default pricing based on category
            base_prices = {
                "budget": 1000,
                "three_star": 2500,
                "four_star": 5000,
                "five_star": 10000,
                "luxury": 20000
            }
            price_per_night = base_prices.get(hotel_category, 2500)
            
            return {
                "travel_mode": "hotel",
                "price_per_night": price_per_night,
                "total_price": price_per_night * nights,
                "nights": nights,
                "confidence": 0.4,
                "message": "Estimated pricing"
            }
        
        df = pd.DataFrame([{
            'date': p.stay_date,
            'price': p.price_per_night,
            'occupancy': p.occupancy_rate,
            'is_weekend': p.is_weekend
        } for p in prices])
        
        # Check if check-in is weekend
        is_weekend = check_in_date.weekday() >= 5
        
        forecast = self.forecaster.forecast(
            df, 
            target_date=check_in_date,
            features=['occupancy', 'is_weekend']
        )
        
        price_per_night = forecast['price']
        
        # Weekend surcharge
        if is_weekend:
            price_per_night *= 1.20
        
        return {
            "travel_mode": "hotel",
            "price_per_night": price_per_night,
            "total_price": price_per_night * nights,
            "nights": nights,
            "confidence": forecast['confidence'],
            "is_weekend": is_weekend,
            "recommendation": self._get_recommendation(price_per_night, df['price'].mean())
        }
    
    async def predict_car_rental_price(
        self,
        pickup_city: str,
        rental_start_date: datetime,
        rental_duration_days: int,
        car_type: str = "sedan"
    ) -> Dict:
        """Predict car rental price"""
        
        query = select(CarRentalPrice).join(CarRental).where(
            and_(
                CarRental.pickup_city == pickup_city,
                CarRental.car_type == car_type
            )
        ).order_by(CarRentalPrice.created_at)
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        if not prices:
            # Default pricing by car type
            base_prices = {
                "hatchback": 1200,
                "sedan": 1800,
                "suv": 3000,
                "luxury": 6000,
                "van": 2500
            }
            price_per_day = base_prices.get(car_type, 1800)
            
            return {
                "travel_mode": "car_rental",
                "price_per_day": price_per_day,
                "total_price": price_per_day * rental_duration_days,
                "duration_days": rental_duration_days,
                "confidence": 0.4,
                "message": "Estimated pricing"
            }
        
        df = pd.DataFrame([{
            'date': p.rental_start_date,
            'price': p.price_per_day,
            'duration': p.rental_duration_days,
            'utilization': p.utilization_rate
        } for p in prices])
        
        forecast = self.forecaster.forecast(df, target_date=rental_start_date)
        
        price_per_day = forecast['price']
        
        # Multi-day discount
        if rental_duration_days >= 7:
            price_per_day *= 0.85  # 15% discount for week+
        elif rental_duration_days >= 3:
            price_per_day *= 0.92  # 8% discount for 3+ days
        
        return {
            "travel_mode": "car_rental",
            "price_per_day": price_per_day,
            "total_price": price_per_day * rental_duration_days,
            "duration_days": rental_duration_days,
            "confidence": forecast['confidence'],
            "discount_applied": rental_duration_days >= 3,
            "recommendation": self._get_recommendation(price_per_day, df['price'].mean())
        }
    
    async def compare_all_modes(
        self,
        origin: str,
        destination: str,
        travel_date: datetime
    ) -> Dict:
        """
        Compare prices across all available travel modes
        """
        results = {}
        
        # Predict flight price
        try:
            results['flight'] = await self.predict_flight_price(origin, destination, travel_date)
        except Exception as e:
            results['flight'] = {"error": str(e)}
        
        # Predict train price
        try:
            results['train'] = await self.predict_train_price(origin, destination, travel_date)
        except Exception as e:
            results['train'] = {"error": str(e)}
        
        # Predict bus price
        try:
            results['bus'] = await self.predict_bus_price(origin, destination, travel_date)
        except Exception as e:
            results['bus'] = {"error": str(e)}
        
        # Find cheapest option
        valid_options = {k: v for k, v in results.items() if 'error' not in v}
        if valid_options:
            cheapest = min(valid_options.items(), key=lambda x: x[1]['predicted_price'])
            results['recommendation'] = {
                "cheapest_mode": cheapest[0],
                "cheapest_price": cheapest[1]['predicted_price'],
                "savings_vs_alternatives": {}
            }
            
            for mode, data in valid_options.items():
                if mode != cheapest[0]:
                    savings = data['predicted_price'] - cheapest[1]['predicted_price']
                    results['recommendation']['savings_vs_alternatives'][mode] = savings
        
        return results
    
    def _calculate_trend(self, prices: pd.Series) -> str:
        """Calculate price trend"""
        if len(prices) < 2:
            return "stable"
        
        recent_avg = prices.tail(10).mean()
        overall_avg = prices.mean()
        
        if recent_avg > overall_avg * 1.1:
            return "increasing"
        elif recent_avg < overall_avg * 0.9:
            return "decreasing"
        else:
            return "stable"
    
    def _get_recommendation(self, predicted_price: float, historical_avg: float) -> str:
        """Get booking recommendation"""
        ratio = predicted_price / historical_avg
        
        if ratio < 0.85:
            return "Excellent price! Book now."
        elif ratio < 0.95:
            return "Good deal. Consider booking."
        elif ratio < 1.05:
            return "Average price. Book if convenient."
        elif ratio < 1.15:
            return "Slightly expensive. Consider waiting."
        else:
            return "High price. Wait for better rates."
