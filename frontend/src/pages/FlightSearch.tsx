import { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Alert,
  Autocomplete,
  InputAdornment,
  Stack,
  alpha,
  IconButton,
  Tooltip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  FlightTakeoff,
  FlightLand,
  Search,
  SwapHoriz,
  TrendingDown,
  TrendingUp,
  AirlineSeatReclineNormal,
  CompareArrows,
  Favorite,
  FavoriteBorder,
  FilterList,
  CalendarMonth,
} from '@mui/icons-material';

// Popular airports
const airports = [
  { code: 'DEL', city: 'New Delhi', name: 'Indira Gandhi International' },
  { code: 'BOM', city: 'Mumbai', name: 'Chhatrapati Shivaji Maharaj' },
  { code: 'BLR', city: 'Bangalore', name: 'Kempegowda International' },
  { code: 'MAA', city: 'Chennai', name: 'Chennai International' },
  { code: 'CCU', city: 'Kolkata', name: 'Netaji Subhas Chandra Bose' },
  { code: 'HYD', city: 'Hyderabad', name: 'Rajiv Gandhi International' },
  { code: 'GOI', city: 'Goa', name: 'Dabolim Airport' },
  { code: 'COK', city: 'Kochi', name: 'Cochin International' },
  { code: 'AMD', city: 'Ahmedabad', name: 'Sardar Vallabhbhai Patel' },
  { code: 'PNQ', city: 'Pune', name: 'Pune Airport' },
  { code: 'DXB', city: 'Dubai', name: 'Dubai International' },
  { code: 'SIN', city: 'Singapore', name: 'Changi Airport' },
  { code: 'LHR', city: 'London', name: 'Heathrow Airport' },
  { code: 'JFK', city: 'New York', name: 'John F. Kennedy' },
];

// Mock flight data for demo
const mockFlights = [
  {
    id: 1,
    flight_number: 'AI-101',
    airline: 'Air India',
    origin: 'DEL',
    destination: 'BOM',
    departure_time: '2025-12-20T06:00:00',
    arrival_time: '2025-12-20T08:15:00',
    duration_minutes: 135,
    current_price: 4599,
    original_price: 5999,
    available_seats: 45,
    cabin_class: 'economy',
    is_direct: true,
    price_trend: 'down',
  },
  {
    id: 2,
    flight_number: 'UK-832',
    airline: 'Vistara',
    origin: 'DEL',
    destination: 'BOM',
    departure_time: '2025-12-20T09:30:00',
    arrival_time: '2025-12-20T11:45:00',
    duration_minutes: 135,
    current_price: 5299,
    original_price: 5299,
    available_seats: 23,
    cabin_class: 'economy',
    is_direct: true,
    price_trend: 'stable',
  },
  {
    id: 3,
    flight_number: '6E-234',
    airline: 'IndiGo',
    origin: 'DEL',
    destination: 'BOM',
    departure_time: '2025-12-20T14:00:00',
    arrival_time: '2025-12-20T16:10:00',
    duration_minutes: 130,
    current_price: 3899,
    original_price: 4299,
    available_seats: 12,
    cabin_class: 'economy',
    is_direct: true,
    price_trend: 'down',
  },
  {
    id: 4,
    flight_number: 'SG-456',
    airline: 'SpiceJet',
    origin: 'DEL',
    destination: 'BOM',
    departure_time: '2025-12-20T18:30:00',
    arrival_time: '2025-12-20T20:40:00',
    duration_minutes: 130,
    current_price: 3499,
    original_price: 3499,
    available_seats: 67,
    cabin_class: 'economy',
    is_direct: true,
    price_trend: 'up',
  },
  {
    id: 5,
    flight_number: 'AI-505',
    airline: 'Air India',
    origin: 'DEL',
    destination: 'BOM',
    departure_time: '2025-12-20T21:00:00',
    arrival_time: '2025-12-20T23:15:00',
    duration_minutes: 135,
    current_price: 4199,
    original_price: 4799,
    available_seats: 89,
    cabin_class: 'economy',
    is_direct: true,
    price_trend: 'down',
  },
];

const FlightSearch = () => {
  const [origin, setOrigin] = useState<any>(null);
  const [destination, setDestination] = useState<any>(null);
  const [date, setDate] = useState('2025-12-20');
  const [passengers, setPassengers] = useState(1);
  const [searched, setSearched] = useState(false);
  const [loading, setLoading] = useState(false);
  const [flights, setFlights] = useState<any[]>([]);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [sortBy, setSortBy] = useState('price');
  const [showFilters, setShowFilters] = useState(false);

  const handleSearch = async () => {
    if (!origin || !destination) return;
    
    setLoading(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Use mock data for demo
    setFlights(mockFlights);
    setSearched(true);
    setLoading(false);
  };

  const swapAirports = () => {
    const temp = origin;
    setOrigin(destination);
    setDestination(temp);
  };

  const toggleFavorite = (id: number) => {
    setFavorites(prev => 
      prev.includes(id) ? prev.filter(f => f !== id) : [...prev, id]
    );
  };

  const formatTime = (dateStr: string) => {
    return new Date(dateStr).toLocaleTimeString('en-IN', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  };

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  const sortedFlights = [...flights].sort((a, b) => {
    switch (sortBy) {
      case 'price': return a.current_price - b.current_price;
      case 'duration': return a.duration_minutes - b.duration_minutes;
      case 'departure': return new Date(a.departure_time).getTime() - new Date(b.departure_time).getTime();
      default: return 0;
    }
  });

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          textAlign: 'center',
          mb: 5,
          position: 'relative',
        }}
      >
        <Typography 
          variant="h3" 
          fontWeight="800"
          sx={{
            background: 'linear-gradient(135deg, #fff 0%, #a78bfa 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            mb: 2,
          }}
        >
          Find Your Perfect Flight
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Compare prices across airlines and save up to 40%
        </Typography>
      </Box>

      {/* Search Card */}
      <Paper
        elevation={0}
        sx={{
          p: 4,
          mb: 4,
          background: alpha('#fff', 0.02),
          backdropFilter: 'blur(40px)',
          borderRadius: 4,
          border: '1px solid',
          borderColor: alpha('#fff', 0.08),
        }}
      >
        <Grid container spacing={3} alignItems="center">
          {/* Origin */}
          <Grid item xs={12} md={3}>
            <Autocomplete
              options={airports}
              getOptionLabel={(option) => `${option.code} - ${option.city}`}
              value={origin}
              onChange={(_, value) => setOrigin(value)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="From"
                  placeholder="Select origin"
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <InputAdornment position="start">
                        <FlightTakeoff sx={{ color: 'primary.main' }} />
                      </InputAdornment>
                    ),
                  }}
                />
              )}
              renderOption={(props, option) => (
                <Box component="li" {...props}>
                  <Box>
                    <Typography fontWeight="600">{option.code}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {option.city} - {option.name}
                    </Typography>
                  </Box>
                </Box>
              )}
            />
          </Grid>

          {/* Swap Button */}
          <Grid item xs={12} md="auto">
            <IconButton 
              onClick={swapAirports}
              sx={{ 
                bgcolor: alpha('#6366f1', 0.1),
                '&:hover': { bgcolor: alpha('#6366f1', 0.2) }
              }}
            >
              <SwapHoriz />
            </IconButton>
          </Grid>

          {/* Destination */}
          <Grid item xs={12} md={3}>
            <Autocomplete
              options={airports}
              getOptionLabel={(option) => `${option.code} - ${option.city}`}
              value={destination}
              onChange={(_, value) => setDestination(value)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="To"
                  placeholder="Select destination"
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: (
                      <InputAdornment position="start">
                        <FlightLand sx={{ color: 'secondary.main' }} />
                      </InputAdornment>
                    ),
                  }}
                />
              )}
              renderOption={(props, option) => (
                <Box component="li" {...props}>
                  <Box>
                    <Typography fontWeight="600">{option.code}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {option.city} - {option.name}
                    </Typography>
                  </Box>
                </Box>
              )}
            />
          </Grid>

          {/* Date */}
          <Grid item xs={12} md={2}>
            <TextField
              label="Departure Date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              fullWidth
              InputLabelProps={{ shrink: true }}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <CalendarMonth sx={{ color: 'text.secondary' }} />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>

          {/* Passengers */}
          <Grid item xs={6} md={1}>
            <TextField
              label="Passengers"
              type="number"
              value={passengers}
              onChange={(e) => setPassengers(parseInt(e.target.value) || 1)}
              inputProps={{ min: 1, max: 9 }}
              fullWidth
            />
          </Grid>

          {/* Search Button */}
          <Grid item xs={6} md={2}>
            <Button
              variant="contained"
              size="large"
              fullWidth
              onClick={handleSearch}
              disabled={!origin || !destination || loading}
              startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <Search />}
              sx={{
                py: 1.8,
                background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)',
                },
              }}
            >
              {loading ? 'Searching...' : 'Search'}
            </Button>
          </Grid>
        </Grid>

        {/* Quick Filters */}
        <Stack direction="row" spacing={1} mt={3} flexWrap="wrap" gap={1}>
          <Chip label="Direct flights only" variant="outlined" onClick={() => {}} />
          <Chip label="Morning departure" variant="outlined" onClick={() => {}} />
          <Chip label="Evening departure" variant="outlined" onClick={() => {}} />
          <Chip label="Refundable" variant="outlined" onClick={() => {}} />
        </Stack>
      </Paper>

      {/* Results Section */}
      {searched && (
        <Box>
          {/* Results Header */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Box>
              <Typography variant="h5" fontWeight="700">
                {origin?.code} → {destination?.code}
              </Typography>
              <Typography color="text.secondary">
                {flights.length} flights found • {new Date(date).toLocaleDateString('en-IN', { 
                  weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
                })}
              </Typography>
            </Box>
            <Stack direction="row" spacing={2}>
              <FormControl size="small" sx={{ minWidth: 150 }}>
                <InputLabel>Sort by</InputLabel>
                <Select
                  value={sortBy}
                  label="Sort by"
                  onChange={(e) => setSortBy(e.target.value)}
                >
                  <MenuItem value="price">Price: Low to High</MenuItem>
                  <MenuItem value="duration">Duration: Shortest</MenuItem>
                  <MenuItem value="departure">Departure: Earliest</MenuItem>
                </Select>
              </FormControl>
              <Button 
                variant="outlined" 
                startIcon={<FilterList />}
                onClick={() => setShowFilters(!showFilters)}
              >
                Filters
              </Button>
            </Stack>
          </Box>

          {/* Price Alert Banner */}
          <Alert 
            severity="info" 
            sx={{ 
              mb: 3, 
              background: alpha('#6366f1', 0.1),
              border: '1px solid',
              borderColor: alpha('#6366f1', 0.3),
            }}
          >
            <Typography fontWeight="600">💡 Price Drop Alert!</Typography>
            Prices for this route have dropped 12% in the last 24 hours. Book now to save!
          </Alert>

          {/* Flight Cards */}
          <Stack spacing={2}>
            {sortedFlights.map((flight) => (
              <Card
                key={flight.id}
                sx={{
                  background: alpha('#fff', 0.02),
                  backdropFilter: 'blur(20px)',
                  border: '1px solid',
                  borderColor: alpha('#fff', 0.08),
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 20px 40px rgba(0,0,0,0.3)',
                    borderColor: alpha('#6366f1', 0.3),
                  },
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Grid container alignItems="center" spacing={3}>
                    {/* Airline Info */}
                    <Grid item xs={12} md={2}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Box
                          sx={{
                            width: 48,
                            height: 48,
                            borderRadius: 2,
                            background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontWeight: 700,
                            fontSize: '0.8rem',
                          }}
                        >
                          {flight.airline.substring(0, 2).toUpperCase()}
                        </Box>
                        <Box>
                          <Typography fontWeight="600">{flight.airline}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {flight.flight_number}
                          </Typography>
                        </Box>
                      </Box>
                    </Grid>

                    {/* Flight Times */}
                    <Grid item xs={12} md={4}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                        <Box textAlign="center">
                          <Typography variant="h5" fontWeight="700">
                            {formatTime(flight.departure_time)}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {flight.origin}
                          </Typography>
                        </Box>
                        <Box sx={{ flex: 1, textAlign: 'center', px: 2 }}>
                          <Typography variant="body2" color="text.secondary">
                            {formatDuration(flight.duration_minutes)}
                          </Typography>
                          <Box
                            sx={{
                              height: 2,
                              background: 'linear-gradient(90deg, #6366f1, #ec4899)',
                              borderRadius: 1,
                              position: 'relative',
                              my: 0.5,
                            }}
                          >
                            <Box
                              sx={{
                                position: 'absolute',
                                right: 0,
                                top: '50%',
                                transform: 'translate(50%, -50%)',
                                width: 8,
                                height: 8,
                                borderRadius: '50%',
                                bgcolor: '#ec4899',
                              }}
                            />
                          </Box>
                          <Chip 
                            label={flight.is_direct ? 'Non-stop' : '1 Stop'} 
                            size="small"
                            sx={{ 
                              height: 20, 
                              fontSize: '0.7rem',
                              bgcolor: flight.is_direct ? alpha('#10b981', 0.2) : alpha('#f59e0b', 0.2),
                              color: flight.is_direct ? '#10b981' : '#f59e0b',
                            }}
                          />
                        </Box>
                        <Box textAlign="center">
                          <Typography variant="h5" fontWeight="700">
                            {formatTime(flight.arrival_time)}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {flight.destination}
                          </Typography>
                        </Box>
                      </Box>
                    </Grid>

                    {/* Availability */}
                    <Grid item xs={6} md={2}>
                      <Stack direction="row" alignItems="center" spacing={1}>
                        <AirlineSeatReclineNormal sx={{ color: 'text.secondary' }} />
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            Seats left
                          </Typography>
                          <Typography fontWeight="600" color={flight.available_seats < 20 ? 'error.main' : 'success.main'}>
                            {flight.available_seats}
                          </Typography>
                        </Box>
                      </Stack>
                    </Grid>

                    {/* Price */}
                    <Grid item xs={6} md={2}>
                      <Box textAlign="right">
                        {flight.current_price < flight.original_price && (
                          <Typography 
                            variant="body2" 
                            sx={{ textDecoration: 'line-through', color: 'text.secondary' }}
                          >
                            ₹{flight.original_price.toLocaleString()}
                          </Typography>
                        )}
                        <Typography variant="h5" fontWeight="800" color="primary.main">
                          ₹{flight.current_price.toLocaleString()}
                        </Typography>
                        <Stack direction="row" alignItems="center" justifyContent="flex-end" spacing={0.5}>
                          {flight.price_trend === 'down' && (
                            <>
                              <TrendingDown sx={{ fontSize: 16, color: 'success.main' }} />
                              <Typography variant="caption" color="success.main">
                                Price dropping
                              </Typography>
                            </>
                          )}
                          {flight.price_trend === 'up' && (
                            <>
                              <TrendingUp sx={{ fontSize: 16, color: 'error.main' }} />
                              <Typography variant="caption" color="error.main">
                                Price rising
                              </Typography>
                            </>
                          )}
                        </Stack>
                      </Box>
                    </Grid>

                    {/* Actions */}
                    <Grid item xs={12} md={2}>
                      <Stack spacing={1}>
                        <Button
                          variant="contained"
                          fullWidth
                          sx={{
                            background: 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                          }}
                        >
                          Select
                        </Button>
                        <Stack direction="row" spacing={1}>
                          <Tooltip title={favorites.includes(flight.id) ? 'Remove from favorites' : 'Add to favorites'}>
                            <IconButton 
                              size="small"
                              onClick={() => toggleFavorite(flight.id)}
                              sx={{ flex: 1, border: '1px solid', borderColor: alpha('#fff', 0.1) }}
                            >
                              {favorites.includes(flight.id) ? 
                                <Favorite sx={{ color: 'error.main' }} /> : 
                                <FavoriteBorder />
                              }
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Compare">
                            <IconButton 
                              size="small"
                              sx={{ flex: 1, border: '1px solid', borderColor: alpha('#fff', 0.1) }}
                            >
                              <CompareArrows />
                            </IconButton>
                          </Tooltip>
                        </Stack>
                      </Stack>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            ))}
          </Stack>
        </Box>
      )}

      {/* Empty State */}
      {!searched && (
        <Box textAlign="center" py={8}>
          <FlightTakeoff sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h5" color="text.secondary" gutterBottom>
            Search for flights to get started
          </Typography>
          <Typography color="text.secondary">
            Enter your origin, destination and travel date to find the best deals
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default FlightSearch;
