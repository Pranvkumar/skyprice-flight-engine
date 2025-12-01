# Real-time Flight Data Service
# Uses Amadeus API for live flight prices

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from app.services.data_sources.amadeus_client import get_amadeus_client

logger = logging.getLogger(__name__)


class RealTimeFlightDataService:
    """
    Service to fetch and process real-time flight data
    Integrates with Amadeus API
    """
    
    def __init__(self):
        self.amadeus = get_amadeus_client()
    
    async def get_live_prices(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        cabin_class: str = 'ECONOMY'
    ) -> List[Dict]:
        """
        Fetch live flight prices for a route
        
        Args:
            origin: Origin airport IATA code
            destination: Destination airport IATA code
            departure_date: Departure date (YYYY-MM-DD)
            cabin_class: Cabin class preference
            
        Returns:
            List of flight offers with real prices
        """
        try:
            flights = self.amadeus.search_flights(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                max_results=20
            )
            
            # Filter by cabin class if specified
            if cabin_class and cabin_class != 'ANY':
                flights = [f for f in flights if f['cabin_class'] == cabin_class]
            
            # Add metadata
            for flight in flights:
                flight['source'] = 'amadeus'
                flight['fetched_at'] = datetime.utcnow().isoformat()
            
            logger.info(f"Fetched {len(flights)} live prices for {origin}-{destination}")
            return flights
            
        except Exception as e:
            logger.error(f"Failed to fetch live prices: {e}")
            return []
    
    async def get_price_trends(
        self,
        origin: str,
        destination: str,
        days_back: int = 30
    ) -> Dict:
        """
        Get historical price trends for route
        
        Args:
            origin: Origin IATA code
            destination: Destination IATA code
            days_back: Number of days of historical data
            
        Returns:
            Historical price data and trends
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            historical_data = self.amadeus.get_historical_prices(
                origin=origin,
                destination=destination,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d')
            )
            
            if not historical_data:
                return {'error': 'No historical data available'}
            
            # Calculate trends
            prices = [d['price'] for d in historical_data]
            avg_price = sum(prices) / len(prices)
            min_price = min(prices)
            max_price = max(prices)
            
            # Price volatility
            volatility = (max_price - min_price) / avg_price if avg_price > 0 else 0
            
            return {
                'historical_prices': historical_data,
                'statistics': {
                    'average': round(avg_price, 2),
                    'minimum': round(min_price, 2),
                    'maximum': round(max_price, 2),
                    'volatility': round(volatility, 2),
                    'sample_size': len(historical_data)
                },
                'currency': historical_data[0]['currency'] if historical_data else 'USD'
            }
            
        except Exception as e:
            logger.error(f"Failed to get price trends: {e}")
            return {'error': str(e)}
    
    async def get_best_booking_time(
        self,
        origin: str,
        destination: str,
        target_date: str
    ) -> Dict:
        """
        Get recommendation for best time to book
        
        Args:
            origin: Origin IATA code
            destination: Destination IATA code
            target_date: Target departure date
            
        Returns:
            Booking recommendations with price insights
        """
        try:
            # Get cheapest date in the vicinity
            cheapest = self.amadeus.get_cheapest_date(
                origin=origin,
                destination=destination,
                departure_date=target_date
            )
            
            # Get price analysis
            price_metrics = self.amadeus.get_flight_price_analysis(
                origin=origin,
                destination=destination,
                departure_date=target_date
            )
            
            recommendation = {
                'target_date': target_date,
                'recommendation': 'Book now' if cheapest else 'Wait and monitor',
                'confidence': 'high' if price_metrics else 'medium'
            }
            
            if cheapest:
                recommendation['cheapest_option'] = cheapest
            
            if price_metrics:
                recommendation['price_analysis'] = price_metrics
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Failed to get booking recommendation: {e}")
            return {'error': str(e)}
    
    async def search_airports(self, keyword: str) -> List[Dict]:
        """
        Search airports for autocomplete
        
        Args:
            keyword: Search keyword (city name or IATA code)
            
        Returns:
            List of matching airports
        """
        try:
            return self.amadeus.search_airports(keyword, max_results=15)
        except Exception as e:
            logger.error(f"Airport search failed: {e}")
            return []
    
    async def get_route_insights(
        self,
        origin: str,
        destination: str,
        departure_date: str
    ) -> Dict:
        """
        Get comprehensive route insights combining multiple data sources
        
        Args:
            origin: Origin IATA code
            destination: Destination IATA code
            departure_date: Departure date
            
        Returns:
            Comprehensive route analysis
        """
        try:
            # Fetch live prices
            live_prices = await self.get_live_prices(origin, destination, departure_date)
            
            # Get price trends
            trends = await self.get_price_trends(origin, destination, days_back=30)
            
            # Get booking recommendation
            booking_rec = await self.get_best_booking_time(origin, destination, departure_date)
            
            if not live_prices:
                return {'error': 'No flight data available for this route'}
            
            # Calculate current price statistics
            current_prices = [f['price'] for f in live_prices]
            avg_current = sum(current_prices) / len(current_prices)
            min_current = min(current_prices)
            
            return {
                'route': f"{origin}-{destination}",
                'departure_date': departure_date,
                'current_prices': {
                    'average': round(avg_current, 2),
                    'minimum': round(min_current, 2),
                    'sample_size': len(current_prices),
                    'currency': live_prices[0]['currency']
                },
                'flights': live_prices[:5],  # Top 5 cheapest
                'trends': trends,
                'booking_recommendation': booking_rec,
                'fetched_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get route insights: {e}")
            return {'error': str(e)}


# Singleton instance
_service = None

def get_flight_data_service() -> RealTimeFlightDataService:
    """Get or create flight data service singleton"""
    global _service
    if _service is None:
        _service = RealTimeFlightDataService()
    return _service
