# Test Amadeus API
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AMADEUS API LIVE TEST RESULTS" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Test 1: Health Check
Write-Host "[1/3] Health Check..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "  STATUS: " -NoNewline; Write-Host $health.status.ToUpper() -ForegroundColor Green
    Write-Host "  Amadeus Configured: " -NoNewline; Write-Host $health.amadeus_configured -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Server not responding" -ForegroundColor Red
    Write-Host "  Make sure server is running: python test_server.py" -ForegroundColor Yellow
    exit 1
}

# Test 2: Airport Search
Write-Host "`n[2/3] Airport Search (Paris)..." -ForegroundColor Yellow
try {
    $airports = Invoke-RestMethod "http://localhost:8000/airports?query=Paris" -TimeoutSec 5
    Write-Host "  SUCCESS! Found $($airports.count) airports" -ForegroundColor Green
    Write-Host "`n  Top 3 Results:" -ForegroundColor Cyan
    $airports.airports[0..2] | ForEach-Object {
        Write-Host "    - $($_.full_name) - $($_.city), $($_.country)"
    }
} catch {
    Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Flight Search
Write-Host "`n[3/3] Flight Search (PAR -> LON, Dec 15)..." -ForegroundColor Yellow
try {
    $flights = Invoke-RestMethod "http://localhost:8000/flights?origin=PAR&destination=LON&date=2025-12-15" -TimeoutSec 10
    
    if ($flights.success) {
        Write-Host "  SUCCESS! Found $($flights.count) flights" -ForegroundColor Green
        Write-Host "`n  Price Range:" -ForegroundColor Cyan
        Write-Host "    Lowest:  $($flights.price_stats.lowest) $($flights.price_stats.currency)"
        Write-Host "    Highest: $($flights.price_stats.highest) $($flights.price_stats.currency)"
        Write-Host "    Average: $([math]::Round($flights.price_stats.average, 2)) $($flights.price_stats.currency)"
        
        Write-Host "`n  First Flight Details:" -ForegroundColor Cyan
        $flight = $flights.flights[0]
        Write-Host "    Price: $($flight.price) $($flight.currency)"
        Write-Host "    Airline: $($flight.airline) $($flight.flight_number)"
        Write-Host "    Departure: $($flight.departure.time)"
        Write-Host "    Arrival: $($flight.arrival.time)"
        Write-Host "    Duration: $($flight.duration)"
    } else {
        Write-Host "  INFO: $($flights.message)" -ForegroundColor Yellow
        if ($flights.test_mode) {
            Write-Host "  (This is normal for test environment)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  TEST COMPLETE!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "View interactive API docs at: http://localhost:8000/docs" -ForegroundColor Blue
