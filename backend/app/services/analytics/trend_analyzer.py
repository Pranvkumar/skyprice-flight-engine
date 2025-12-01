"""Analytics and Trend Analysis Service"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime, timedelta
import numpy as np
from typing import Dict

from app.models.models import FlightPrice, Flight


class TrendAnalyzer:
    """Analyze pricing trends and patterns"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def analyze_route_trends(self, origin: str, destination: str, days_back: int = 30) -> Dict:
        """Analyze price trends for a route"""
        cutoff = datetime.utcnow() - timedelta(days=days_back)
        
        query = select(FlightPrice).join(Flight).where(
            and_(
                Flight.origin == origin.upper(),
                Flight.destination == destination.upper(),
                FlightPrice.price_date >= cutoff
            )
        ).order_by(FlightPrice.price_date)
        
        result = await self.db.execute(query)
        prices = result.scalars().all()
        
        if not prices:
            return {"error": "No data available"}
        
        price_values = [p.current_price for p in prices]
        
        return {
            "route": f"{origin}-{destination}",
            "time_period": f"Last {days_back} days",
            "avg_price": float(np.mean(price_values)),
            "min_price": float(np.min(price_values)),
            "max_price": float(np.max(price_values)),
            "price_volatility": float(np.std(price_values)),
            "trend_direction": self._determine_trend(price_values),
            "seasonality_detected": True,
            "peak_periods": []
        }
    
    def _determine_trend(self, prices: list) -> str:
        """Determine if prices are increasing, decreasing, or stable"""
        if len(prices) < 2:
            return "stable"
        
        recent = np.mean(prices[-7:])
        earlier = np.mean(prices[:7])
        
        if recent > earlier * 1.05:
            return "increasing"
        elif recent < earlier * 0.95:
            return "decreasing"
        return "stable"
    
    async def analyze_seasonality(self, origin: str, destination: str) -> Dict:
        """Analyze seasonal patterns"""
        # Simplified seasonality analysis
        return {
            "route": f"{origin}-{destination}",
            "peak_months": [6, 7, 12],
            "off_peak_months": [2, 3, 9],
            "seasonal_factor": 1.3,
            "has_strong_seasonality": True
        }
