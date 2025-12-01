"""
Test script to demonstrate the Multi-Modal Travel API
Run this after the backend is running on http://localhost:8000
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api/v1"

def print_response(title, response):
    """Pretty print API responses"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
    print()

def test_health_check():
    """Test if API is running"""
    response = requests.get("http://localhost:8000/health")
    print_response("🏥 Health Check", response)
    return response.status_code == 200

def test_travel_search():
    """Test multi-modal travel search"""
    search_data = {
        "origin": "DEL",  # Delhi
        "destination": "BOM",  # Mumbai
        "departure_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "passenger_count": 2,
        "travel_modes": ["flight", "train", "bus"]
    }
    
    response = requests.post(f"{BASE_URL}/travel/search", json=search_data)
    print_response("🔍 Multi-Modal Search (Delhi to Mumbai)", response)

def test_compare_modes():
    """Test price comparison across travel modes"""
    params = {
        "origin": "DEL",
        "destination": "BOM",
        "travel_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "passenger_count": 1
    }
    
    response = requests.get(f"{BASE_URL}/travel/compare", params=params)
    print_response("💰 Price Comparison - All Modes", response)

def test_vacation_package():
    """Test creating a vacation package"""
    package_data = {
        "user_email": "pranav@example.com",
        "user_name": "Pranav Kumar",
        "flight_id": 1,
        "flight_price": 5000.0,
        "hotel_id": 1,
        "hotel_price": 3000.0,
        "check_in_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "check_out_date": (datetime.now() + timedelta(days=10)).isoformat(),
        "car_rental_id": 1,
        "car_rental_price": 1500.0,
        "travel_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "return_date": (datetime.now() + timedelta(days=10)).isoformat(),
        "passenger_count": 2
    }
    
    response = requests.post(f"{BASE_URL}/travel/package/create", json=package_data)
    print_response("🎁 Vacation Package (Flight + Hotel + Car)", response)

def test_price_prediction():
    """Test flight price prediction"""
    predict_data = {
        "origin": "DEL",
        "destination": "BOM",
        "departure_date": (datetime.now() + timedelta(days=15)).isoformat(),
        "cabin_class": "economy",
        "passengers": 1
    }
    
    response = requests.post(f"{BASE_URL}/forecast/predict", json=predict_data)
    print_response("📊 Price Prediction (Flight)", response)

def test_create_booking():
    """Test creating a booking"""
    booking_data = {
        "user_email": "pranav@example.com",
        "user_name": "Pranav Kumar",
        "user_phone": "+91-9876543210",
        "travel_mode": "flight",
        "item_id": 1,
        "travel_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "passenger_count": 1,
        "total_price": 5500.0,
        "base_price": 5000.0,
        "taxes": 500.0,
        "discount": 0.0,
        "special_requests": "Window seat preferred"
    }
    
    response = requests.post(f"{BASE_URL}/travel/book", json=booking_data)
    print_response("✈️ Create Booking", response)
    
    if response.status_code == 200:
        booking_id = response.json().get("booking_id")
        if booking_id:
            # Test getting the booking
            get_response = requests.get(f"{BASE_URL}/travel/bookings/{booking_id}")
            print_response(f"📋 Get Booking Details ({booking_id})", get_response)

def demo_all_features():
    """Run all demonstrations"""
    print("\n" + "🚀"*30)
    print("  MULTI-MODAL TRAVEL API DEMONSTRATION")
    print("  Project 17: Price Recommendation Engine")
    print("  Pranav Kumar (590011587) & Om (590014492)")
    print("🚀"*30)
    
    # Check if API is running
    if not test_health_check():
        print("\n❌ API is not running. Start it with:")
        print("   cd backend")
        print("   venv\\Scripts\\python.exe -m uvicorn app.main:app --reload")
        return
    
    print("\n✅ API is healthy! Running demonstrations...\n")
    
    # Run all tests
    test_travel_search()
    test_compare_modes()
    test_price_prediction()
    test_vacation_package()
    test_create_booking()
    
    print("\n" + "="*60)
    print("  🎉 DEMONSTRATION COMPLETE!")
    print("="*60)
    print("\n📖 View full API documentation at: http://localhost:8000/docs")
    print("📊 Interactive testing available at: http://localhost:8000/docs")
    print("\n💡 Key Features Demonstrated:")
    print("   ✓ Multi-modal search (flights, trains, buses)")
    print("   ✓ Price comparison across modes")
    print("   ✓ AI-powered price prediction")
    print("   ✓ Package bundling with discounts")
    print("   ✓ Unified booking system")
    print()

if __name__ == "__main__":
    try:
        demo_all_features()
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API.")
        print("   Make sure the backend is running on http://localhost:8000")
        print("\n   Start it with:")
        print("   cd C:\\Coding\\flight-price-recommendation-engine\\backend")
        print("   venv\\Scripts\\python.exe -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
