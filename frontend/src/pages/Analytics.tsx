import { useState } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Card, 
  CardContent,
  alpha,
  Stack,
  Chip,
  ToggleButton,
  ToggleButtonGroup,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  LinearProgress,
  Divider,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  BarChart,
  ShowChart,
  PieChart,
  CalendarMonth,
  Flight,
} from '@mui/icons-material';

// Mock analytics data
const weeklyPriceData = [
  { day: 'Mon', avgPrice: 4523, bookings: 234 },
  { day: 'Tue', avgPrice: 4789, bookings: 267 },
  { day: 'Wed', avgPrice: 4234, bookings: 312 },
  { day: 'Thu', avgPrice: 4567, bookings: 289 },
  { day: 'Fri', avgPrice: 5234, bookings: 456 },
  { day: 'Sat', avgPrice: 5678, bookings: 523 },
  { day: 'Sun', avgPrice: 5123, bookings: 412 },
];

const routeAnalytics = [
  { route: 'DEL → BOM', searches: 12345, bookings: 2345, conversion: 19, avgPrice: 4599 },
  { route: 'BLR → DEL', searches: 9876, bookings: 1876, conversion: 19, avgPrice: 5299 },
  { route: 'MAA → BOM', searches: 8765, bookings: 1567, conversion: 18, avgPrice: 3899 },
  { route: 'HYD → DEL', searches: 7654, bookings: 1234, conversion: 16, avgPrice: 4899 },
  { route: 'CCU → BLR', searches: 6543, bookings: 987, conversion: 15, avgPrice: 6299 },
  { route: 'GOI → DEL', searches: 5432, bookings: 876, conversion: 16, avgPrice: 5499 },
];

const demandForecast = [
  { month: 'Jan', demand: 78, priceIndex: 92 },
  { month: 'Feb', demand: 82, priceIndex: 95 },
  { month: 'Mar', demand: 89, priceIndex: 98 },
  { month: 'Apr', demand: 75, priceIndex: 88 },
  { month: 'May', demand: 68, priceIndex: 82 },
  { month: 'Jun', demand: 92, priceIndex: 105 },
];

const competitorPricing = [
  { airline: 'Air India', avgPrice: 4899, marketShare: 28 },
  { airline: 'IndiGo', avgPrice: 4299, marketShare: 35 },
  { airline: 'Vistara', avgPrice: 5499, marketShare: 18 },
  { airline: 'SpiceJet', avgPrice: 3899, marketShare: 15 },
  { airline: 'Go First', avgPrice: 3699, marketShare: 4 },
];

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('7d');
  const [selectedRoute, setSelectedRoute] = useState('all');
  const maxPrice = Math.max(...weeklyPriceData.map(d => d.avgPrice));

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography 
            variant="h3" 
            fontWeight="800"
            sx={{
              background: 'linear-gradient(135deg, #fff 0%, #a78bfa 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Analytics
          </Typography>
          <Typography color="text.secondary">
            In-depth analysis of flight prices and booking trends
          </Typography>
        </Box>
        <Stack direction="row" spacing={2}>
          <ToggleButtonGroup
            value={timeRange}
            exclusive
            onChange={(_, val) => val && setTimeRange(val)}
            size="small"
          >
            <ToggleButton value="24h">24H</ToggleButton>
            <ToggleButton value="7d">7D</ToggleButton>
            <ToggleButton value="30d">30D</ToggleButton>
            <ToggleButton value="90d">90D</ToggleButton>
          </ToggleButtonGroup>
        </Stack>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              background: alpha('#fff', 0.02),
              backdropFilter: 'blur(20px)',
              border: '1px solid',
              borderColor: alpha('#fff', 0.08),
            }}
          >
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={1} mb={1}>
                <ShowChart sx={{ color: '#6366f1' }} />
                <Typography color="text.secondary" variant="body2">Avg. Price Trend</Typography>
              </Stack>
              <Typography variant="h4" fontWeight="700" color="#6366f1">
                ₹4,735
              </Typography>
              <Stack direction="row" alignItems="center" spacing={0.5} mt={1}>
                <TrendingDown sx={{ fontSize: 16, color: 'success.main' }} />
                <Typography variant="caption" color="success.main">-5.2% from last week</Typography>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              background: alpha('#fff', 0.02),
              backdropFilter: 'blur(20px)',
              border: '1px solid',
              borderColor: alpha('#fff', 0.08),
            }}
          >
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={1} mb={1}>
                <BarChart sx={{ color: '#10b981' }} />
                <Typography color="text.secondary" variant="body2">Total Searches</Typography>
              </Stack>
              <Typography variant="h4" fontWeight="700" color="#10b981">
                48.5K
              </Typography>
              <Stack direction="row" alignItems="center" spacing={0.5} mt={1}>
                <TrendingUp sx={{ fontSize: 16, color: 'success.main' }} />
                <Typography variant="caption" color="success.main">+12.8% from last week</Typography>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              background: alpha('#fff', 0.02),
              backdropFilter: 'blur(20px)',
              border: '1px solid',
              borderColor: alpha('#fff', 0.08),
            }}
          >
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={1} mb={1}>
                <PieChart sx={{ color: '#f59e0b' }} />
                <Typography color="text.secondary" variant="body2">Conversion Rate</Typography>
              </Stack>
              <Typography variant="h4" fontWeight="700" color="#f59e0b">
                17.3%
              </Typography>
              <Stack direction="row" alignItems="center" spacing={0.5} mt={1}>
                <TrendingUp sx={{ fontSize: 16, color: 'success.main' }} />
                <Typography variant="caption" color="success.main">+2.1% from last week</Typography>
              </Stack>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card
            sx={{
              background: alpha('#fff', 0.02),
              backdropFilter: 'blur(20px)',
              border: '1px solid',
              borderColor: alpha('#fff', 0.08),
            }}
          >
            <CardContent>
              <Stack direction="row" alignItems="center" spacing={1} mb={1}>
                <CalendarMonth sx={{ color: '#ec4899' }} />
                <Typography color="text.secondary" variant="body2">Best Day to Book</Typography>
              </Stack>
              <Typography variant="h4" fontWeight="700" color="#ec4899">
                Tuesday
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Avg. 8% cheaper than weekends
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Price Trend Chart */}
        <Grid item xs={12} lg={8}>
          <Paper
            sx={{
              p: 3,
              background: alpha('#fff', 0.02),
              backdropFilter: 'blur(20px)',
              border: '1px solid',
              borderColor: alpha('#fff', 0.08),
              borderRadius: 3,
            }}
          >
            <Typography variant="h6" fontWeight="700" mb={3}>
              Weekly Price & Booking Trends
            </Typography>
            
            {/* Simple Bar Chart Visualization */}
            <Box sx={{ display: 'flex', alignItems: 'flex-end', gap: 2, height: 200, mb: 2 }}>
              {weeklyPriceData.map((day, index) => (
                <Box key={index} sx={{ flex: 1, textAlign: 'center' }}>
                  <Box
                    sx={{
                      height: (day.avgPrice / maxPrice) * 160,
                      background: 'linear-gradient(180deg, #6366f1 0%, #8b5cf6 100%)',
                      borderRadius: '8px 8px 0 0',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        transform: 'scaleY(1.05)',
                        transformOrigin: 'bottom',
                      },
                    }}
                  />
                  <Typography variant="caption" color="text.secondary" mt={1}>
                    {day.day}
                  </Typography>
                </Box>
              ))}
            </Box>

            <Divider sx={{ my: 3, borderColor: alpha('#fff', 0.1) }} />

            <Grid container spacing={3}>
              {weeklyPriceData.map((day, index) => (
                <Grid item xs={6} sm={4} md={12 / 7} key={index}>
                  <Box textAlign="center">
                    <Typography variant="body2" color="text.secondary">{day.day}</Typography>
                    <Typography fontWeight="700">₹{day.avgPrice.toLocaleString()}</Typography>
                    <Typography variant="caption" color="text.secondary">{day.bookings} bookings</Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Competitor Analysis */}
        <Grid item xs={12} lg={4}>
          <Paper
            sx={{
              p: 3,
              background: alpha('#fff', 0.02),
              backdropFilter: 'blur(20px)',
              border: '1px solid',
              borderColor: alpha('#fff', 0.08),
              borderRadius: 3,
              height: '100%',
            }}
          >
            <Typography variant="h6" fontWeight="700" mb={3}>
              Competitor Pricing
            </Typography>
            <Stack spacing={2}>
              {competitorPricing.map((airline, index) => (
                <Box key={index}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                    <Typography variant="body2" fontWeight="600">{airline.airline}</Typography>
                    <Typography variant="body2" color="primary.main" fontWeight="600">
                      ₹{airline.avgPrice.toLocaleString()}
                    </Typography>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <LinearProgress
                      variant="determinate"
                      value={airline.marketShare}
                      sx={{ 
                        flex: 1,
                        height: 8, 
                        borderRadius: 1,
                        bgcolor: alpha('#fff', 0.05),
                        '& .MuiLinearProgress-bar': {
                          background: `linear-gradient(90deg, ${
                            index === 0 ? '#6366f1' : 
                            index === 1 ? '#10b981' : 
                            index === 2 ? '#f59e0b' : 
                            index === 3 ? '#ec4899' : '#8b5cf6'
                          }, ${
                            index === 0 ? '#8b5cf6' : 
                            index === 1 ? '#34d399' : 
                            index === 2 ? '#fbbf24' : 
                            index === 3 ? '#f472b6' : '#a78bfa'
                          })`,
                        }
                      }}
                    />
                    <Typography variant="caption" color="text.secondary" sx={{ minWidth: 40 }}>
                      {airline.marketShare}%
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Stack>
          </Paper>
        </Grid>

        {/* Route Analytics Table */}
        <Grid item xs={12}>
          <Paper
            sx={{
              p: 3,
              background: alpha('#fff', 0.02),
              backdropFilter: 'blur(20px)',
              border: '1px solid',
              borderColor: alpha('#fff', 0.08),
              borderRadius: 3,
            }}
          >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
              <Typography variant="h6" fontWeight="700">
                Route Performance Analysis
              </Typography>
              <FormControl size="small" sx={{ minWidth: 200 }}>
                <InputLabel>Filter by Route</InputLabel>
                <Select
                  value={selectedRoute}
                  label="Filter by Route"
                  onChange={(e) => setSelectedRoute(e.target.value)}
                >
                  <MenuItem value="all">All Routes</MenuItem>
                  {routeAnalytics.map((route, index) => (
                    <MenuItem key={index} value={route.route}>{route.route}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Box>

            <Box sx={{ overflowX: 'auto' }}>
              <Box sx={{ minWidth: 800 }}>
                {/* Table Header */}
                <Box 
                  sx={{ 
                    display: 'grid', 
                    gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr',
                    gap: 2,
                    p: 2,
                    bgcolor: alpha('#fff', 0.03),
                    borderRadius: 2,
                    mb: 1,
                  }}
                >
                  <Typography variant="body2" color="text.secondary" fontWeight="600">Route</Typography>
                  <Typography variant="body2" color="text.secondary" fontWeight="600">Searches</Typography>
                  <Typography variant="body2" color="text.secondary" fontWeight="600">Bookings</Typography>
                  <Typography variant="body2" color="text.secondary" fontWeight="600">Conversion</Typography>
                  <Typography variant="body2" color="text.secondary" fontWeight="600">Avg. Price</Typography>
                </Box>

                {/* Table Rows */}
                <Stack spacing={1}>
                  {routeAnalytics.map((route, index) => (
                    <Box 
                      key={index}
                      sx={{ 
                        display: 'grid', 
                        gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr',
                        gap: 2,
                        p: 2,
                        borderRadius: 2,
                        transition: 'all 0.2s ease',
                        '&:hover': {
                          bgcolor: alpha('#fff', 0.03),
                        }
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Flight sx={{ fontSize: 18, color: 'primary.main' }} />
                        <Typography fontWeight="600">{route.route}</Typography>
                      </Box>
                      <Typography>{route.searches.toLocaleString()}</Typography>
                      <Typography>{route.bookings.toLocaleString()}</Typography>
                      <Box>
                        <Chip 
                          label={`${route.conversion}%`}
                          size="small"
                          sx={{
                            bgcolor: route.conversion >= 18 ? alpha('#10b981', 0.2) : alpha('#f59e0b', 0.2),
                            color: route.conversion >= 18 ? '#10b981' : '#f59e0b',
                          }}
                        />
                      </Box>
                      <Typography fontWeight="600" color="primary.main">
                        ₹{route.avgPrice.toLocaleString()}
                      </Typography>
                    </Box>
                  ))}
                </Stack>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Demand Forecast */}
        <Grid item xs={12}>
          <Paper
            sx={{
              p: 3,
              background: alpha('#fff', 0.02),
              backdropFilter: 'blur(20px)',
              border: '1px solid',
              borderColor: alpha('#fff', 0.08),
              borderRadius: 3,
            }}
          >
            <Typography variant="h6" fontWeight="700" mb={3}>
              6-Month Demand & Price Forecast
            </Typography>
            <Grid container spacing={2}>
              {demandForecast.map((month, index) => (
                <Grid item xs={6} sm={4} md={2} key={index}>
                  <Box
                    sx={{
                      p: 2,
                      borderRadius: 2,
                      background: alpha('#fff', 0.02),
                      border: '1px solid',
                      borderColor: alpha('#fff', 0.05),
                      textAlign: 'center',
                    }}
                  >
                    <Typography variant="body2" color="text.secondary" mb={1}>
                      {month.month}
                    </Typography>
                    <Box sx={{ mb: 1 }}>
                      <Typography variant="caption" color="text.secondary">Demand</Typography>
                      <LinearProgress
                        variant="determinate"
                        value={month.demand}
                        sx={{ 
                          height: 6, 
                          borderRadius: 1,
                          bgcolor: alpha('#fff', 0.05),
                          '& .MuiLinearProgress-bar': {
                            background: 'linear-gradient(90deg, #6366f1, #8b5cf6)',
                          }
                        }}
                      />
                    </Box>
                    <Box>
                      <Typography variant="caption" color="text.secondary">Price Index</Typography>
                      <LinearProgress
                        variant="determinate"
                        value={month.priceIndex}
                        sx={{ 
                          height: 6, 
                          borderRadius: 1,
                          bgcolor: alpha('#fff', 0.05),
                          '& .MuiLinearProgress-bar': {
                            background: month.priceIndex > 100 ? 
                              'linear-gradient(90deg, #ef4444, #f87171)' :
                              'linear-gradient(90deg, #10b981, #34d399)',
                          }
                        }}
                      />
                    </Box>
                    <Stack direction="row" justifyContent="space-between" mt={1}>
                      <Typography variant="caption">{month.demand}%</Typography>
                      <Typography 
                        variant="caption" 
                        color={month.priceIndex > 100 ? 'error.main' : 'success.main'}
                      >
                        {month.priceIndex}
                      </Typography>
                    </Stack>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;
