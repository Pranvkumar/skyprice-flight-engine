import React, { useState } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Grid,
  Autocomplete,
  Stack,
  Chip,
  Alert,
  alpha,
} from '@mui/material';
import {
  Search,
  CalendarToday,
  TrendingUp,
  Savings,
  Schedule,
  FlightTakeoff,
  Flight,
  LocalOffer,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { GlassCard, PriceCard, StatCard, SectionHeader, LoadingSpinner, Badge, FlightCard } from '../components/UIComponents';

const PriceForecasting = () => {
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState<any>(null);

  // Popular airports
  const airports = [
    { code: 'BOM', name: 'Mumbai', city: 'Mumbai, India' },
    { code: 'DEL', name: 'Delhi', city: 'New Delhi, India' },
    { code: 'BLR', name: 'Bangalore', city: 'Bengaluru, India' },
    { code: 'HYD', name: 'Hyderabad', city: 'Hyderabad, India' },
    { code: 'MAA', name: 'Chennai', city: 'Chennai, India' },
    { code: 'CCU', name: 'Kolkata', city: 'Kolkata, India' },
    { code: 'GOI', name: 'Goa', city: 'Goa, India' },
    { code: 'DXB', name: 'Dubai', city: 'Dubai, UAE' },
    { code: 'SIN', name: 'Singapore', city: 'Singapore' },
    { code: 'LHR', name: 'London', city: 'London, UK' },
  ];

  const [origin, setOrigin] = useState(airports[0]);
  const [destination, setDestination] = useState(airports[1]);
  const [departureDate, setDepartureDate] = useState('2025-12-15');

  // Mock prediction data
  const mockData = {
    currentPrice: 5420,
    predictedPrice: 4890,
    savings: 530,
    confidence: 92,
    bestTimeToBook: '7-14 days before',
    priceHistory: [
      { date: '2025-11-01', price: 5800, predicted: null },
      { date: '2025-11-08', price: 5600, predicted: null },
      { date: '2025-11-15', price: 5400, predicted: null },
      { date: '2025-11-22', price: 5500, predicted: null },
      { date: '2025-11-29', price: 5420, predicted: null },
      { date: '2025-12-06', price: null, predicted: 5100 },
      { date: '2025-12-13', price: null, predicted: 4890 },
      { date: '2025-12-20', price: null, predicted: 5200 },
      { date: '2025-12-27', price: null, predicted: 5600 },
    ],
    recommendation: 'Book in the next 2 weeks for best prices',
    flights: [
      { airline: 'Air India', price: 5420, departure: '08:30', arrival: '10:45', duration: '2h 15m' },
      { airline: 'IndiGo', price: 5280, departure: '14:20', arrival: '16:30', duration: '2h 10m' },
      { airline: 'SpiceJet', price: 4990, departure: '18:45', arrival: '21:00', duration: '2h 15m' },
    ],
  };

  const handlePredict = () => {
    setLoading(true);
    setTimeout(() => {
      setPrediction(mockData);
      setLoading(false);
    }, 1500);
  };

  return (
    <Box>
      {/* Hero Section */}
      <Box sx={{ mb: 6 }}>
        <Typography
          variant="h2"
          sx={{
            fontWeight: 900,
            mb: 2,
            background: 'linear-gradient(135deg, #ffffff 0%, #94a3b8 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          Price Forecasting
        </Typography>
        <Typography variant="h6" color="text.secondary">
          AI-powered predictions using divide-and-conquer algorithms
        </Typography>
      </Box>

      {/* Search Form */}
      <GlassCard sx={{ mb: 6, p: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={3}>
            <Autocomplete
              value={origin}
              onChange={(_, value) => value && setOrigin(value)}
              options={airports}
              getOptionLabel={(option) => `${option.name} (${option.code})`}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="From"
                  variant="outlined"
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: <FlightTakeoff sx={{ mr: 1, color: 'primary.main' }} />,
                  }}
                />
              )}
              renderOption={(props, option) => (
                <Box component="li" {...props}>
                  <Box>
                    <Typography variant="body1" fontWeight={600}>
                      {option.name} ({option.code})
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {option.city}
                    </Typography>
                  </Box>
                </Box>
              )}
            />
          </Grid>

          <Grid item xs={12} md={3}>
            <Autocomplete
              value={destination}
              onChange={(_, value) => value && setDestination(value)}
              options={airports}
              getOptionLabel={(option) => `${option.name} (${option.code})`}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="To"
                  variant="outlined"
                  InputProps={{
                    ...params.InputProps,
                    startAdornment: <Flight sx={{ mr: 1, color: 'secondary.main' }} />,
                  }}
                />
              )}
              renderOption={(props, option) => (
                <Box component="li" {...props}>
                  <Box>
                    <Typography variant="body1" fontWeight={600}>
                      {option.name} ({option.code})
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {option.city}
                    </Typography>
                  </Box>
                </Box>
              )}
            />
          </Grid>

          <Grid item xs={12} md={3}>
            <TextField
              fullWidth
              type="date"
              label="Departure Date"
              value={departureDate}
              onChange={(e) => setDepartureDate(e.target.value)}
              InputProps={{
                startAdornment: <CalendarToday sx={{ mr: 1, color: 'text.secondary' }} />,
              }}
              InputLabelProps={{ shrink: true }}
            />
          </Grid>

          <Grid item xs={12} md={3}>
            <Button
              fullWidth
              variant="contained"
              size="large"
              onClick={handlePredict}
              disabled={loading}
              startIcon={<TrendingUp />}
              sx={{
                height: '56px',
                background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
                fontWeight: 700,
                fontSize: '1rem',
                '&:hover': {
                  boxShadow: '0 10px 30px rgba(99, 102, 241, 0.4)',
                },
              }}
            >
              {loading ? 'Analyzing...' : 'Predict Prices'}
            </Button>
          </Grid>
        </Grid>
      </GlassCard>

      {/* Loading State */}
      {loading && <LoadingSpinner message="Analyzing flight prices with AI..." />}

      {/* Results */}
      {prediction && !loading && (
        <Box>
          {/* Stats Cards */}
          <Grid container spacing={3} sx={{ mb: 6 }}>
            <Grid item xs={12} md={3}>
              <StatCard
                label="Current Price"
                value={`₹${prediction.currentPrice.toLocaleString()}`}
                icon={<FlightTakeoff />}
                gradient="rgba(99, 102, 241, 0.1)"
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <StatCard
                label="Predicted Price"
                value={`₹${prediction.predictedPrice.toLocaleString()}`}
                icon={<TrendingUp />}
                gradient="rgba(34, 197, 94, 0.1)"
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <StatCard
                label="Potential Savings"
                value={`₹${prediction.savings.toLocaleString()}`}
                icon={<Savings />}
                gradient="rgba(251, 146, 60, 0.1)"
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <StatCard
                label="Confidence"
                value={`${prediction.confidence}%`}
                icon={<LocalOffer />}
                gradient="rgba(236, 72, 153, 0.1)"
              />
            </Grid>
          </Grid>

          {/* Recommendation Alert */}
          <Alert
            severity="success"
            icon={<Schedule />}
            sx={{
              mb: 6,
              background: 'rgba(34, 197, 94, 0.1)',
              border: '1px solid rgba(34, 197, 94, 0.3)',
              '& .MuiAlert-icon': { color: '#22c55e' },
            }}
          >
            <Typography variant="h6" sx={{ fontWeight: 700, mb: 1 }}>
              Best Time to Book: {prediction.bestTimeToBook}
            </Typography>
            <Typography variant="body2">{prediction.recommendation}</Typography>
          </Alert>

          {/* Price Trend Chart */}
          <GlassCard sx={{ mb: 6, p: 4 }}>
            <SectionHeader title="Price Trend Analysis" subtitle="Historical prices and AI predictions" />
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={prediction.priceHistory}>
                <defs>
                  <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorPredicted" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ec4899" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#ec4899" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="date" stroke="#94a3b8" style={{ fontSize: 12 }} />
                <YAxis stroke="#94a3b8" style={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    background: 'rgba(19, 19, 26, 0.95)',
                    border: '1px solid rgba(99, 102, 241, 0.3)',
                    borderRadius: 12,
                    color: '#fff',
                  }}
                />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="price"
                  stroke="#6366f1"
                  strokeWidth={3}
                  fill="url(#colorPrice)"
                  name="Historical Price"
                />
                <Area
                  type="monotone"
                  dataKey="predicted"
                  stroke="#ec4899"
                  strokeWidth={3}
                  strokeDasharray="5 5"
                  fill="url(#colorPredicted)"
                  name="Predicted Price"
                />
              </AreaChart>
            </ResponsiveContainer>
          </GlassCard>

          {/* Available Flights */}
          <Box>
            <SectionHeader
              title="Available Flights"
              subtitle={`${origin.code} → ${destination.code} on ${departureDate}`}
            />
            <Grid container spacing={3}>
              {prediction.flights.map((flight: any, index: number) => (
                <Grid item xs={12} md={4} key={index}>
                  <FlightCard {...flight} />
                </Grid>
              ))}
            </Grid>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default PriceForecasting;
