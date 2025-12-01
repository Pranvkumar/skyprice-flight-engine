"""
Amadeus API Client for Real Flight Data
Provides live flight prices, search, and historical data
"""

from amadeus import Client, ResponseError
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class AmadeusFlightClient:
    """
    Wrapper for Amadeus API to fetch real flight data
    """
    
    def __init__(self):
        self.client = Client(
            client_id=os.getenv('AMADEUS_API_KEY'),
            client_secret=os.getenv('AMADEUS_API_SECRET')
        )
        logger.info("Amadeus API client initialized")
    
    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        adults: int = 1,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Search for flights between origin and destination
        
        Args:
            origin: IATA code (e.g., 'BOM', 'DEL')
            destination: IATA code
            departure_date: Date in YYYY-MM-DD format
            adults: Number of adult passengers
            max_results: Maximum number of results to return
            
        Returns:
            List of flight offers with prices
        """
        try:
            response = self.client.shopping.flight_offers_search.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departure_date,
                adults=adults,
                max=max_results
            )
            
            flights = []
            for offer in response.data:
                flight_data = self._parse_flight_offer(offer)
                flights.append(flight_data)
            
            logger.info(f"Found {len(flights)} flights from {origin} to {destination}")
            return flights
            
        except ResponseError as error:
            logger.error(f"Amadeus API error: {error}")
            raise Exception(f"Flight search failed: {error}")
    
    def get_flight_price_analysis(
        self,
        origin: str,
        destination: str,
        departure_date: str
    ) -> Dict:
        """
        Get price analysis and recommendations using Amadeus ML
        
        Returns:
            Price insights including predictions and recommendations
        """
        try:
            response = self.client.analytics.itinerary_price_metrics.get(
                originIataCode=origin,
                destinationIataCode=destination,
                departureDate=departure_date
            )
            
            if response.data:
                metrics = response.data[0]
                return {
                    'price_metrics': {
                        'mean': float(metrics.get('priceMetrics', [{}])[0].get('amount', 0)),
                        'quartile_1': float(metrics.get('priceMetrics', [{}])[0].get('quartiles', {}).get('first', 0)),
                        'quartile_2': float(metrics.get('priceMetrics', [{}])[0].get('quartiles', {}).get('second', 0)),
                        'quartile_3': float(metrics.get('priceMetrics', [{}])[0].get('quartiles', {}).get('third', 0)),
                    },
                    'currency': metrics.get('currencyCode', 'USD')
                }
            
            return {}
            
        except ResponseError as error:
            logger.warning(f"Price analysis unavailable: {error}")
            return {}
    
    def search_airports(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        Search for airports by city name or IATA code
        Used for autocomplete functionality
        
        Args:
            keyword: Search term (city name or partial IATA code)
            max_results: Maximum number of results
            
        Returns:
            List of airport information
        """
        try:
            response = self.client.reference_data.locations.get(
                keyword=keyword,
                subType='AIRPORT',
                page={'limit': max_results}
            )
            
            airports = []
            for location in response.data:
                airport = {
                    'iata_code': location['iataCode'],
                    'name': location['name'],
                    'city': location['address'].get('cityName', ''),
                    'country': location['address'].get('countryName', ''),
                    'full_name': f"{location['name']} ({location['iataCode']})"
                }
                airports.append(airport)
            
            return airports
            
        except ResponseError as error:
            logger.error(f"Airport search error: {error}")
            return []
    
    def get_historical_prices(
        self,
        origin: str,
        destination: str,
        start_date: str,
        end_date: str
    ) -> List[Dict]:
        """
        Fetch historical price data for route
        This is simulated by searching multiple dates
        
        Args:
            origin: Origin IATA code
            destination: Destination IATA code
            start_date: Start date for historical data
            end_date: End date for historical data
            
        Returns:
            List of historical price points
        """
        historical_data = []
        
        try:
            # For real implementation, we'd query Amadeus historical API
            # For now, we'll sample a few dates
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            days_diff = (end - start).days
            
            # Sample 10 dates across the range
            sample_dates = []
            for i in range(0, min(10, days_diff), max(1, days_diff // 10)):
                sample_date = start + timedelta(days=i)
                sample_dates.append(sample_date.strftime('%Y-%m-%d'))
            
            for date in sample_dates:
                try:
                    flights = self.search_flights(origin, destination, date, max_results=3)
                    if flights:
                        # Get average price for the date
                        avg_price = sum(f['price'] for f in flights) / len(flights)
                        historical_data.append({
                            'date': date,
                            'price': avg_price,
                            'currency': flights[0]['currency'],
                            'sample_count': len(flights)
                        })
                except Exception as e:
                    logger.warning(f"Could not fetch price for {date}: {e}")
                    continue
            
            return historical_data
            
        except Exception as error:
            logger.error(f"Historical data fetch error: {error}")
            return []
    
    def get_cheapest_date(
        self,
        origin: str,
        destination: str,
        departure_date: str
    ) -> Dict:
        """
        Find the cheapest date to fly using Amadeus Flight Inspiration Search
        
        Args:
            origin: Origin IATA code
            destination: Destination IATA code  
            departure_date: Target departure date
            
        Returns:
            Cheapest flight date and price
        """
        try:
            response = self.client.shopping.flight_dates.get(
                origin=origin,
                destination=destination,
                departureDate=departure_date
            )
            
            if response.data:
                cheapest = response.data[0]
                return {
                    'departure_date': cheapest['departureDate'],
                    'return_date': cheapest.get('returnDate'),
                    'price': float(cheapest['price']['total']),
                    'currency': cheapest['price']['currency']
                }
            
            return {}
            
        except ResponseError as error:
            logger.warning(f"Cheapest date search failed: {error}")
            return {}
    
    def _parse_flight_offer(self, offer: Dict) -> Dict:
        """
        Parse Amadeus flight offer into simplified format
        
        Args:
            offer: Raw Amadeus API response
            
        Returns:
            Simplified flight data
        """
        itinerary = offer['itineraries'][0]
        segment = itinerary['segments'][0]
        
        return {
            'id': offer['id'],
            'price': float(offer['price']['total']),
            'currency': offer['price']['currency'],
            'airline': segment['carrierCode'],
            'flight_number': segment['number'],
            'departure': {
                'iata': segment['departure']['iataCode'],
                'time': segment['departure']['at']
            },
            'arrival': {
                'iata': segment['arrival']['iataCode'],
                'time': segment['arrival']['at']
            },
            'duration': itinerary['duration'],
            'seats_available': offer.get('numberOfBookableSeats', 0),
            'cabin_class': segment.get('cabin', 'ECONOMY')
        }


# Singleton instance
_client = None

def get_amadeus_client() -> AmadeusFlightClient:
    """Get or create Amadeus client singleton"""
    global _client
    if _client is None:
        _client = AmadeusFlightClient()
    return _client
