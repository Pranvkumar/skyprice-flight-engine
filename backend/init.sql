-- Database initialization script

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create enum types
DO $$ BEGIN
    CREATE TYPE cabin_class AS ENUM ('economy', 'premium_economy', 'business', 'first');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE flight_status AS ENUM ('scheduled', 'active', 'completed', 'cancelled');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Seed data
INSERT INTO flights (flight_number, airline, aircraft_type, origin, destination, origin_city, destination_city, 
                     departure_time, arrival_time, duration_minutes, total_seats, available_seats, cabin_class, status, is_direct)
VALUES
('AI101', 'Air India', 'Boeing 787', 'BOM', 'DEL', 'Mumbai', 'Delhi', 
 '2025-12-01 06:00:00', '2025-12-01 08:30:00', 150, 200, 150, 'economy', 'scheduled', true),
('6E202', 'IndiGo', 'Airbus A320', 'BOM', 'BLR', 'Mumbai', 'Bangalore', 
 '2025-12-01 09:00:00', '2025-12-01 10:30:00', 90, 180, 120, 'economy', 'scheduled', true),
('SG303', 'SpiceJet', 'Boeing 737', 'DEL', 'BOM', 'Delhi', 'Mumbai', 
 '2025-12-01 14:00:00', '2025-12-01 16:30:00', 150, 189, 100, 'economy', 'scheduled', true);

-- Seed price data
INSERT INTO flight_prices (flight_id, base_price, current_price, predicted_price, demand_multiplier, 
                          seasonality_factor, time_to_departure_days, occupancy_rate, prediction_confidence, segment_id)
VALUES
(1, 4500, 5200, 5500, 1.15, 1.0, 30, 0.75, 0.88, 'route_BOM_DEL'),
(2, 3800, 4100, 4300, 1.08, 1.0, 30, 0.67, 0.85, 'route_BOM_BLR'),
(3, 4500, 5000, 5200, 1.11, 1.0, 30, 0.53, 0.82, 'route_DEL_BOM');

-- Seed route data
INSERT INTO routes (origin, destination, distance_km, average_duration_minutes, is_international, is_popular, 
                   avg_daily_searches, avg_daily_bookings, historical_avg_price, price_volatility)
VALUES
('BOM', 'DEL', 1400, 150, false, true, 5000, 500, 5000, 800),
('BOM', 'BLR', 850, 90, false, true, 3500, 400, 4000, 600),
('DEL', 'BOM', 1400, 150, false, true, 4800, 480, 5100, 750);

COMMIT;
