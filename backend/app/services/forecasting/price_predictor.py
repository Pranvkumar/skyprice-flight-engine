"""
Price Predictor Service
Integrates divide-and-conquer forecasting with database operations
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, Dict, List

from app.models.models import Flight, FlightPrice, Route, ExternalFactor
from app.services.forecasting.divide_conquer_engine import DivideAndConquerForecaster
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class PricePredictor:
    """Main service for price prediction"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.forecaster = DivideAndConquerForecaster(
            min_segment_size=settings.SEGMENT_MIN_SIZE
        )
        
    async def predict_price(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        airline: Optional[str] = None,
        cabin_class: str = "economy",
        horizon_days: int = 7
    ) -> Dict:
        """
        Predict flight price using divide-and-conquer forecasting
        """
        # Step 1: Fetch historical data
        historical_data = await self._fetch_historical_data(
            origin, destination, airline, days_back=90
        )
        
        if historical_data.empty:
            raise ValueError(f"Insufficient historical data for route {origin}-{destination}")
        
        # Step 2: Prepare data for forecasting
        df = self._prepare_forecast_data(historical_data)
        
        # Step 3: Run divide-and-conquer forecast
        forecast_result = self.forecaster.predict(
            df=df,
            horizon=horizon_days,
            segmentation_strategy='hierarchical'  # Best for flight data
        )
        
        # Step 4: Get current price
        current_price = await self._get_current_price(origin, destination, airline)
        
        # Step 5: Generate price timeline
        predicted_prices = self._generate_price_timeline(
            forecast_result['forecast'],
            departure_date,
            horizon_days
        )
        
        # Step 6: Calculate optimal booking date
        optimal_date, expected_savings = self._calculate_optimal_booking(
            predicted_prices,
            current_price
        )
        
        # Step 7: Analyze influencing factors
        factors = await self._analyze_price_factors(origin, destination, departure_date)
        
        # Step 8: Generate recommendation
        recommendation = self._generate_recommendation(
            current_price,
            predicted_prices,
            forecast_result['confidence']
        )
        
        return {
            "flight_id": None,
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "current_price": current_price,
            "predicted_prices": predicted_prices,
            "recommendation": recommendation,
            "optimal_booking_date": optimal_date,
            "expected_savings": expected_savings,
            "confidence_score": forecast_result['confidence'],
            "factors": factors,
            "segmentation_strategy": forecast_result.get('segmentation_strategy'),
            "num_segments": forecast_result.get('num_segments', 0)
        }
    
    async def _fetch_historical_data(
        self,
        origin: str,
        destination: str,
        airline: Optional[str],
        days_back: int
    ) -> pd.DataFrame:
        """Fetch historical price data from database"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        query = select(FlightPrice, Flight).join(Flight).where(
            and_(
                Flight.origin == origin.upper(),
                Flight.destination == destination.upper(),
                FlightPrice.price_date >= cutoff_date
            )
        )
        
        if airline:
            query = query.where(Flight.airline == airline)
        
        result = await self.db.execute(query)
        rows = result.all()
        
        data = []
        for price, flight in rows:
            data.append({
                'date': price.price_date,
                'price': price.current_price,
                'origin': flight.origin,
                'destination': flight.destination,
                'airline': flight.airline,
                'days_to_departure': price.time_to_departure_days or 0,
                'occupancy_rate': price.occupancy_rate or 0.5,
                'demand_multiplier': price.demand_multiplier,
                'seasonality_factor': price.seasonality_factor
            })
        
        return pd.DataFrame(data)
    
    def _prepare_forecast_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for forecasting engine"""
        if df.empty:
            return df
        
        # Sort by date
        df = df.sort_values('date')
        
        # Add time features
        df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
        df['month'] = pd.to_datetime(df['date']).dt.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Fill missing values
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        return df
    
    async def _get_current_price(
        self,
        origin: str,
        destination: str,
        airline: Optional[str]
    ) -> float:
        """Get current average price for route"""
        query = select(FlightPrice.current_price).join(Flight).where(
            and_(
                Flight.origin == origin.upper(),
                Flight.destination == destination.upper(),
                FlightPrice.price_date >= datetime.utcnow() - timedelta(days=7)
            )
        )
        
        if airline:
            query = query.where(Flight.airline == airline)
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        return float(np.mean(prices)) if prices else 5000.0  # Default price
    
    def _generate_price_timeline(
        self,
        forecast: List[float],
        departure_date: datetime,
        horizon_days: int
    ) -> List[Dict]:
        """Generate timeline of predicted prices"""
        timeline = []
        current_date = datetime.utcnow()
        
        for i, price in enumerate(forecast[:horizon_days]):
            date = current_date + timedelta(days=i)
            days_until_departure = (departure_date - date).days
            
            # Add confidence bounds (±10%)
            confidence_range = price * 0.10
            
            timeline.append({
                "date": date.isoformat(),
                "price": round(float(price), 2),
                "confidence_lower": round(float(price - confidence_range), 2),
                "confidence_upper": round(float(price + confidence_range), 2),
                "days_until_departure": days_until_departure
            })
        
        return timeline
    
    def _calculate_optimal_booking(
        self,
        predicted_prices: List[Dict],
        current_price: float
    ) -> tuple:
        """Calculate optimal booking date and expected savings"""
        if not predicted_prices:
            return datetime.utcnow(), 0.0
        
        # Find minimum price in forecast
        min_price_entry = min(predicted_prices, key=lambda x: x['price'])
        optimal_date = datetime.fromisoformat(min_price_entry['date'])
        min_price = min_price_entry['price']
        
        # Calculate savings
        expected_savings = current_price - min_price
        
        return optimal_date, round(expected_savings, 2)
    
    async def _analyze_price_factors(
        self,
        origin: str,
        destination: str,
        departure_date: datetime
    ) -> Dict:
        """Analyze factors influencing price"""
        days_to_departure = (departure_date - datetime.utcnow()).days
        
        # Get external factors
        external_query = select(ExternalFactor).where(
            ExternalFactor.factor_date >= datetime.utcnow() - timedelta(days=7)
        ).order_by(ExternalFactor.factor_date.desc()).limit(1)
        
        result = await self.db.execute(external_query)
        external = result.scalar_one_or_none()
        
        factors = {
            "days_to_departure": days_to_departure,
            "booking_urgency": "high" if days_to_departure < 7 else "medium" if days_to_departure < 30 else "low",
            "is_peak_season": external.is_peak_season if external else False,
            "is_holiday": external.is_holiday if external else False,
            "fuel_price_trend": "stable",
            "demand_level": "medium"
        }
        
        return factors
    
    def _generate_recommendation(
        self,
        current_price: float,
        predicted_prices: List[Dict],
        confidence: float
    ) -> str:
        """Generate booking recommendation"""
        if not predicted_prices:
            return "Insufficient data for recommendation"
        
        min_price = min(p['price'] for p in predicted_prices)
        avg_price = np.mean([p['price'] for p in predicted_prices])
        
        if current_price <= min_price * 1.05:  # Within 5% of minimum
            return f"✅ BOOK NOW - Current price (₹{current_price:.0f}) is excellent. Prices may increase."
        elif current_price <= avg_price:
            return f"⏳ WAIT - Prices may drop further. Optimal: ₹{min_price:.0f}"
        else:
            return f"⚠️ WAIT - Current price is high. Expected to drop to ₹{min_price:.0f}"
    
    async def get_route_forecast(
        self,
        origin: str,
        destination: str,
        horizon_days: int = 30
    ) -> Dict:
        """Get comprehensive forecast for a route"""
        historical_data = await self._fetch_historical_data(
            origin, destination, None, days_back=180
        )
        
        if historical_data.empty:
            return {"error": "No data available"}
        
        df = self._prepare_forecast_data(historical_data)
        forecast_result = self.forecaster.predict(df, horizon_days, 'route')
        
        return {
            "route": f"{origin}-{destination}",
            "forecast_horizon_days": horizon_days,
            "forecast": forecast_result['forecast'],
            "confidence": forecast_result['confidence'],
            "avg_historical_price": float(df['price'].mean()),
            "price_volatility": float(df['price'].std()),
            "data_points": len(df)
        }
    
    async def get_confidence_metrics(self, flight_id: int) -> Dict:
        """Get confidence metrics for predictions"""
        query = select(FlightPrice).where(
            FlightPrice.flight_id == flight_id
        ).order_by(FlightPrice.price_date.desc()).limit(1)
        
        result = await self.db.execute(query)
        price = result.scalar_one_or_none()
        
        if not price:
            return {"error": "No prediction data"}
        
        return {
            "flight_id": flight_id,
            "prediction_confidence": price.prediction_confidence,
            "forecast_horizon_days": price.forecast_horizon_days,
            "model_version": price.model_version,
            "segment_id": price.segment_id,
            "last_updated": price.price_date
        }
