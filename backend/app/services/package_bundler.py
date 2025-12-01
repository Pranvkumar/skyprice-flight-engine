"""
Travel Package Bundling Service
Intelligently combines flights, hotels, and car rentals for optimal pricing
"""
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.models import Flight, Hotel, CarRental, TravelMode
from app.services.forecasting.universal_predictor import UniversalTravelPricePredictor


class TravelPackageBundler:
    """
    Creates optimized travel packages by combining multiple travel modes
    Applies smart bundling discounts and finds best combinations
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.predictor = UniversalTravelPricePredictor(db)
    
    async def create_vacation_package(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: datetime,
        passenger_count: int = 1,
        budget: Optional[float] = None
    ) -> Dict:
        """
        Create a complete vacation package with flight + hotel + car
        """
        
        # Concurrent predictions for all components
        flight_pred, hotel_pred, car_pred = await asyncio.gather(
            self.predictor.predict_flight_price(origin, destination, departure_date),
            self.predictor.predict_hotel_price(
                destination, 
                departure_date, 
                return_date
            ),
            self.predictor.predict_car_rental_price(
                destination,
                departure_date,
                (return_date - departure_date).days
            )
        )
        
        # Calculate package pricing
        base_total = (
            flight_pred.get('predicted_price', 0) +
            hotel_pred.get('total_price', 0) +
            car_pred.get('total_price', 0)
        )
        
        # Package discount (15% when booking all 3)
        package_discount = base_total * 0.15
        final_price = base_total - package_discount
        
        # Check budget constraint
        within_budget = True
        if budget and final_price > budget:
            within_budget = False
            # Try to adjust
            final_price = await self._optimize_for_budget(
                origin, destination, departure_date, return_date, budget
            )
        
        return {
            "package_type": "vacation_complete",
            "components": {
                "flight": flight_pred,
                "hotel": hotel_pred,
                "car_rental": car_pred
            },
            "pricing": {
                "base_total": base_total,
                "package_discount": package_discount,
                "discount_percentage": 15.0,
                "final_price": final_price,
                "price_per_person": final_price / passenger_count
            },
            "within_budget": within_budget,
            "savings": package_discount,
            "trip_duration_days": (return_date - departure_date).days
        }
    
    async def create_business_package(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: datetime,
        include_car: bool = True
    ) -> Dict:
        """
        Business travel package (flight + business hotel + optional car)
        """
        
        # Get flight prediction
        flight_pred = await self.predictor.predict_flight_price(
            origin, destination, departure_date, cabin_class="business"
        )
        
        # Get 4-star hotel prediction
        hotel_pred = await self.predictor.predict_hotel_price(
            destination,
            departure_date,
            return_date,
            hotel_category="four_star"
        )
        
        base_total = flight_pred.get('predicted_price', 0) + hotel_pred.get('total_price', 0)
        
        car_pred = None
        if include_car:
            car_pred = await self.predictor.predict_car_rental_price(
                destination,
                departure_date,
                (return_date - departure_date).days,
                car_type="sedan"
            )
            base_total += car_pred.get('total_price', 0)
        
        # Business package discount (10%)
        package_discount = base_total * 0.10
        final_price = base_total - package_discount
        
        components = {
            "flight": flight_pred,
            "hotel": hotel_pred
        }
        if car_pred:
            components["car_rental"] = car_pred
        
        return {
            "package_type": "business",
            "components": components,
            "pricing": {
                "base_total": base_total,
                "package_discount": package_discount,
                "discount_percentage": 10.0,
                "final_price": final_price
            },
            "features": [
                "Business class flight",
                "4-star hotel",
                "Airport transfers" if include_car else None,
                "Fast-track check-in"
            ]
        }
    
    async def create_budget_package(
        self,
        origin: str,
        destination: str,
        travel_date: datetime,
        return_date: Optional[datetime] = None,
        travel_mode_preference: str = "cheapest"
    ) -> Dict:
        """
        Budget-friendly package - finds cheapest combination
        """
        
        # Compare all travel modes
        comparison = await self.predictor.compare_all_modes(
            origin, destination, travel_date
        )
        
        # Select cheapest travel mode
        valid_modes = {k: v for k, v in comparison.items() 
                      if k != 'recommendation' and 'error' not in v}
        
        if not valid_modes:
            return {"error": "No available options"}
        
        cheapest_mode = min(valid_modes.items(), 
                           key=lambda x: x[1].get('predicted_price', float('inf')))
        
        package = {
            "package_type": "budget",
            "selected_mode": cheapest_mode[0],
            "pricing": {
                "travel_price": cheapest_mode[1].get('predicted_price'),
                "final_price": cheapest_mode[1].get('predicted_price')
            },
            "alternatives": {}
        }
        
        # Show how much more expensive other modes are
        for mode, data in valid_modes.items():
            if mode != cheapest_mode[0]:
                price_diff = data.get('predicted_price', 0) - cheapest_mode[1].get('predicted_price', 0)
                package["alternatives"][mode] = {
                    "price": data.get('predicted_price'),
                    "extra_cost": price_diff
                }
        
        # If overnight stay needed, add budget hotel
        if return_date and (return_date - travel_date).days > 0:
            hotel_pred = await self.predictor.predict_hotel_price(
                destination,
                travel_date,
                return_date,
                hotel_category="budget"
            )
            package["components"] = {
                "travel": cheapest_mode[1],
                "accommodation": hotel_pred
            }
            package["pricing"]["hotel_price"] = hotel_pred.get('total_price', 0)
            package["pricing"]["final_price"] += hotel_pred.get('total_price', 0)
        
        return package
    
    async def create_weekend_getaway(
        self,
        origin: str,
        destination: str,
        departure_date: datetime
    ) -> Dict:
        """
        Weekend package (Fri-Sun or Sat-Mon)
        """
        
        # Ensure it's a weekend
        if departure_date.weekday() not in [4, 5]:  # Friday or Saturday
            # Adjust to next Friday
            days_ahead = (4 - departure_date.weekday()) % 7
            departure_date = departure_date + timedelta(days=days_ahead)
        
        return_date = departure_date + timedelta(days=2)  # 2 nights
        
        # Get predictions
        flight_pred = await self.predictor.predict_flight_price(
            origin, destination, departure_date
        )
        
        hotel_pred = await self.predictor.predict_hotel_price(
            destination,
            departure_date,
            return_date,
            hotel_category="three_star"
        )
        
        base_total = flight_pred.get('predicted_price', 0) + hotel_pred.get('total_price', 0)
        
        # Weekend package discount (12%)
        package_discount = base_total * 0.12
        final_price = base_total - package_discount
        
        return {
            "package_type": "weekend_getaway",
            "dates": {
                "departure": departure_date.isoformat(),
                "return": return_date.isoformat(),
                "nights": 2
            },
            "components": {
                "flight": flight_pred,
                "hotel": hotel_pred
            },
            "pricing": {
                "base_total": base_total,
                "package_discount": package_discount,
                "discount_percentage": 12.0,
                "final_price": final_price
            },
            "includes": [
                "Round-trip flight",
                "2 nights accommodation",
                "Breakfast included",
                "Late checkout"
            ]
        }
    
    async def create_group_package(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: datetime,
        group_size: int
    ) -> Dict:
        """
        Group travel package with volume discounts
        """
        
        if group_size < 4:
            return {"error": "Group package requires minimum 4 people"}
        
        # Get base predictions
        flight_pred = await self.predictor.predict_flight_price(
            origin, destination, departure_date
        )
        
        hotel_pred = await self.predictor.predict_hotel_price(
            destination,
            departure_date,
            return_date,
            room_type="family"
        )
        
        # Calculate per-person costs
        flight_cost_per_person = flight_pred.get('predicted_price', 0)
        rooms_needed = (group_size + 3) // 4  # 4 per family room
        hotel_cost_per_person = (hotel_pred.get('total_price', 0) * rooms_needed) / group_size
        
        base_per_person = flight_cost_per_person + hotel_cost_per_person
        
        # Group discounts (scales with group size)
        if group_size >= 20:
            discount_rate = 0.20  # 20% for 20+
        elif group_size >= 10:
            discount_rate = 0.15  # 15% for 10-19
        else:
            discount_rate = 0.10  # 10% for 4-9
        
        discounted_per_person = base_per_person * (1 - discount_rate)
        total_price = discounted_per_person * group_size
        total_savings = (base_per_person * group_size) - total_price
        
        return {
            "package_type": "group_travel",
            "group_size": group_size,
            "pricing": {
                "base_per_person": base_per_person,
                "discounted_per_person": discounted_per_person,
                "total_price": total_price,
                "discount_percentage": discount_rate * 100,
                "total_savings": total_savings
            },
            "components": {
                "flights": f"{group_size} passengers",
                "rooms": f"{rooms_needed} family rooms",
                "hotel": hotel_pred
            },
            "benefits": [
                f"{int(discount_rate * 100)}% group discount",
                "Dedicated travel coordinator",
                "Flexible payment plan",
                "Group activities included"
            ]
        }
    
    async def _optimize_for_budget(
        self,
        origin: str,
        destination: str,
        departure_date: datetime,
        return_date: datetime,
        budget: float
    ) -> float:
        """
        Try to fit package within budget by adjusting options
        """
        
        # Try economy flight + budget hotel
        flight_pred = await self.predictor.predict_flight_price(
            origin, destination, departure_date, cabin_class="economy"
        )
        
        hotel_pred = await self.predictor.predict_hotel_price(
            destination,
            departure_date,
            return_date,
            hotel_category="budget"
        )
        
        # Skip car rental to save money
        adjusted_total = (
            flight_pred.get('predicted_price', 0) +
            hotel_pred.get('total_price', 0)
        )
        
        # Still apply 10% package discount
        adjusted_total *= 0.90
        
        return adjusted_total


# Utility function to suggest best package type
def suggest_package_type(
    trip_duration_days: int,
    is_business: bool,
    budget_conscious: bool,
    group_size: int
) -> str:
    """Suggest the most appropriate package type"""
    
    if group_size >= 4:
        return "group_package"
    
    if is_business:
        return "business_package"
    
    if budget_conscious:
        return "budget_package"
    
    if trip_duration_days <= 3:
        return "weekend_getaway"
    
    return "vacation_package"
