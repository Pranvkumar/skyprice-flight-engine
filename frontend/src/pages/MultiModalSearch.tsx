import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  TextField,
  Button,
  Tabs,
  Tab,
  Chip,
  Stack,
  Avatar,
  MenuItem,
  Alert,
  CircularProgress,
  Divider,
  Paper,
} from '@mui/material';
import {
  Flight,
  Train,
  DirectionsBus,
  Hotel,
  DirectionsCar,
  Search,
  CompareArrows,
  TrendingDown,
  AccessTime,
} from '@mui/icons-material';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div hidden={value !== index} {...other}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

const MultiModalSearch: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [origin, setOrigin] = useState('');
  const [destination, setDestination] = useState('');
  const [date, setDate] = useState('');
  const [passengers, setPassengers] = useState('1');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const travelModes = [
    { icon: <Flight />, label: 'Flights', value: 'flight', color: '#2196f3' },
    { icon: <Train />, label: 'Trains', value: 'train', color: '#4caf50' },
    { icon: <DirectionsBus />, label: 'Buses', value: 'bus', color: '#ff9800' },
    { icon: <Hotel />, label: 'Hotels', value: 'hotel', color: '#9c27b0' },
    { icon: <DirectionsCar />, label: 'Car Rentals', value: 'car', color: '#f44336' },
  ];

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/travel/compare', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          origin,
          destination,
          travel_date: date,
          passenger_count: parseInt(passengers),
        }),
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" gutterBottom fontWeight="bold">
          🌍 Search All Travel Options
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Compare flights, trains, buses, hotels, and car rentals in one place
        </Typography>
      </Box>

      {/* Travel Mode Tabs */}
      <Card sx={{ mb: 4 }}>
        <Tabs
          value={tabValue}
          onChange={(e, newValue) => setTabValue(newValue)}
          variant="fullWidth"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          {travelModes.map((mode, index) => (
            <Tab
              key={mode.value}
              icon={mode.icon}
              label={mode.label}
              sx={{ minHeight: 80, fontSize: '1rem' }}
            />
          ))}
        </Tabs>

        {/* Search Form */}
        <CardContent sx={{ p: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="From"
                placeholder="City or Airport Code"
                value={origin}
                onChange={(e) => setOrigin(e.target.value)}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <TextField
                fullWidth
                label="To"
                placeholder="City or Airport Code"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <TextField
                fullWidth
                label="Date"
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                InputLabelProps={{ shrink: true }}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <TextField
                fullWidth
                label="Passengers"
                type="number"
                value={passengers}
                onChange={(e) => setPassengers(e.target.value)}
                inputProps={{ min: 1, max: 10 }}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <Button
                fullWidth
                variant="contained"
                size="large"
                startIcon={loading ? <CircularProgress size={20} /> : <Search />}
                onClick={handleSearch}
                disabled={loading || !origin || !destination || !date}
                sx={{ height: 56 }}
              >
                Search
              </Button>
            </Grid>
          </Grid>

          {/* Mode-Specific Options */}
          {tabValue === 0 && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Flight Options:
              </Typography>
              <Stack direction="row" spacing={1}>
                <Chip label="Economy" />
                <Chip label="Business" />
                <Chip label="Direct Flights" />
              </Stack>
            </Box>
          )}

          {tabValue === 3 && (
            <Box sx={{ mt: 3 }}>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField fullWidth label="Check-in Date" type="date" InputLabelProps={{ shrink: true }} />
                </Grid>
                <Grid item xs={6}>
                  <TextField fullWidth label="Check-out Date" type="date" InputLabelProps={{ shrink: true }} />
                </Grid>
              </Grid>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Results Section */}
      {results && (
        <Box>
          {/* Price Comparison Summary */}
          <Card sx={{ mb: 3, bgcolor: 'primary.light', color: 'white' }}>
            <CardContent>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs={12} md={4}>
                  <Typography variant="h6">💰 Best Price</Typography>
                  <Typography variant="h4" fontWeight="bold">
                    ₹{results.recommendation?.cheapest_price || '---'}
                  </Typography>
                  <Typography variant="body2">
                    via {results.recommendation?.cheapest_mode || '---'}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Typography variant="h6">⚡ Fastest</Typography>
                  <Typography variant="h4" fontWeight="bold">
                    2h 30m
                  </Typography>
                  <Typography variant="body2">Flight option</Typography>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Typography variant="h6">🎯 Recommended</Typography>
                  <Typography variant="h4" fontWeight="bold">
                    Best Value
                  </Typography>
                  <Typography variant="body2">Train - AC 2 Tier</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>

          {/* Detailed Results */}
          <Grid container spacing={3}>
            {/* Flights */}
            {results.flight && !results.flight.error && (
              <Grid item xs={12} md={6} lg={4}>
                <ResultCard
                  icon={<Flight />}
                  title="Flight"
                  price={results.flight.predicted_price}
                  confidence={results.flight.confidence}
                  color="#2196f3"
                  details={{
                    duration: '2h 30m',
                    provider: 'IndiGo',
                    class: 'Economy',
                  }}
                />
              </Grid>
            )}

            {/* Trains */}
            {results.train && !results.train.error && (
              <Grid item xs={12} md={6} lg={4}>
                <ResultCard
                  icon={<Train />}
                  title="Train"
                  price={results.train.predicted_price}
                  confidence={results.train.confidence}
                  color="#4caf50"
                  details={{
                    duration: '5h 45m',
                    provider: 'Rajdhani Express',
                    class: 'AC 2-Tier',
                  }}
                />
              </Grid>
            )}

            {/* Buses */}
            {results.bus && !results.bus.error && (
              <Grid item xs={12} md={6} lg={4}>
                <ResultCard
                  icon={<DirectionsBus />}
                  title="Bus"
                  price={results.bus.predicted_price}
                  confidence={results.bus.confidence}
                  color="#ff9800"
                  details={{
                    duration: '6h 20m',
                    provider: 'Volvo Sleeper',
                    class: 'AC Sleeper',
                  }}
                />
              </Grid>
            )}
          </Grid>
        </Box>
      )}

      {/* Quick Actions */}
      <Box sx={{ mt: 4 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}>
              <CompareArrows fontSize="large" color="primary" />
              <Typography variant="h6" sx={{ mt: 1 }}>
                Compare All Modes
              </Typography>
              <Typography variant="body2" color="text.secondary">
                See side-by-side comparison
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper sx={{ p: 3, textAlign: 'center', cursor: 'pointer', '&:hover': { bgcolor: 'action.hover' } }}>
              <TrendingDown fontSize="large" color="success" />
              <Typography variant="h6" sx={{ mt: 1 }}>
                Price Alerts
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Get notified on price drops
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

// Result Card Component
interface ResultCardProps {
  icon: React.ReactNode;
  title: string;
  price: number;
  confidence: number;
  color: string;
  details: {
    duration: string;
    provider: string;
    class: string;
  };
}

const ResultCard: React.FC<ResultCardProps> = ({ icon, title, price, confidence, color, details }) => {
  return (
    <Card sx={{ height: '100%', position: 'relative', '&:hover': { boxShadow: 6 } }}>
      <Box sx={{ position: 'absolute', top: 16, right: 16 }}>
        <Chip label={`${(confidence * 100).toFixed(0)}% confident`} size="small" color="success" />
      </Box>
      
      <CardContent>
        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
          <Avatar sx={{ bgcolor: color, width: 48, height: 48 }}>{icon}</Avatar>
          <Box>
            <Typography variant="h6">{title}</Typography>
            <Typography variant="body2" color="text.secondary">
              {details.provider}
            </Typography>
          </Box>
        </Stack>

        <Typography variant="h3" fontWeight="bold" color="primary" gutterBottom>
          ₹{price.toFixed(0)}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Stack spacing={1}>
          <Stack direction="row" justifyContent="space-between">
            <Typography variant="body2" color="text.secondary">
              Duration:
            </Typography>
            <Typography variant="body2" fontWeight="medium">
              {details.duration}
            </Typography>
          </Stack>
          <Stack direction="row" justifyContent="space-between">
            <Typography variant="body2" color="text.secondary">
              Class:
            </Typography>
            <Typography variant="body2" fontWeight="medium">
              {details.class}
            </Typography>
          </Stack>
        </Stack>

        <Button fullWidth variant="contained" sx={{ mt: 3, bgcolor: color }}>
          Book Now
        </Button>
      </CardContent>
    </Card>
  );
};

export default MultiModalSearch;
