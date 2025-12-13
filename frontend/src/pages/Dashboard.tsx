import { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Card, 
  CardContent,
  LinearProgress,
  alpha,
  Stack,
  Chip,
  Divider,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Flight,
  TrendingUp,
  TrendingDown,
  AttachMoney,
  Schedule,
  People,
  Analytics,
  Refresh,
  ArrowUpward,
  ArrowDownward,
  LocalOffer,
} from '@mui/icons-material';
import { useGetAnalyticsDashboardQuery } from '../store/apiSlice';

// Mock dashboard data for demo
const mockDashboardData = {
  total_flights: 1247,
  total_bookings: 8934,
  average_price: 5672,
  revenue_today: 4523000,
  top_routes: [
    { route: 'DEL → BOM', flights: 234, avg_price: 4599, trend: 'up', change: 12 },
    { route: 'BLR → DEL', flights: 198, avg_price: 5299, trend: 'down', change: -8 },
    { route: 'MAA → BOM', flights: 156, avg_price: 3899, trend: 'up', change: 5 },
    { route: 'HYD → DEL', flights: 143, avg_price: 4899, trend: 'stable', change: 0 },
    { route: 'CCU → BLR', flights: 121, avg_price: 6299, trend: 'down', change: -15 },
  ],
  hourly_bookings: [45, 32, 28, 15, 12, 23, 56, 89, 123, 156, 134, 112, 98, 87, 102, 145, 167, 189, 156, 134, 98, 67, 54, 43],
  price_alerts: [
    { route: 'DEL → GOI', message: 'Prices dropped 23%', type: 'drop' },
    { route: 'BOM → DXB', message: 'Limited seats available', type: 'warning' },
    { route: 'BLR → SIN', message: 'Prices rising rapidly', type: 'surge' },
  ],
  airline_performance: [
    { airline: 'Air India', bookings: 2345, satisfaction: 87 },
    { airline: 'IndiGo', bookings: 3456, satisfaction: 92 },
    { airline: 'Vistara', bookings: 1234, satisfaction: 95 },
    { airline: 'SpiceJet', bookings: 1899, satisfaction: 78 },
  ],
};

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: 'up' | 'down' | 'stable';
  trendValue?: string;
  color: string;
}

const StatCard = ({ title, value, icon, trend, trendValue, color }: StatCardProps) => (
  <Card
    sx={{
      background: alpha('#fff', 0.02),
      backdropFilter: 'blur(20px)',
      border: '1px solid',
      borderColor: alpha('#fff', 0.08),
      transition: 'all 0.3s ease',
      '&:hover': {
        transform: 'translateY(-4px)',
        boxShadow: `0 20px 40px ${alpha(color, 0.2)}`,
        borderColor: alpha(color, 0.3),
      },
    }}
  >
    <CardContent sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Box>
          <Typography color="text.secondary" variant="body2" gutterBottom>
            {title}
          </Typography>
          <Typography variant="h4" fontWeight="800" sx={{ color }}>
            {value}
          </Typography>
          {trend && trendValue && (
            <Stack direction="row" alignItems="center" spacing={0.5} mt={1}>
              {trend === 'up' && <ArrowUpward sx={{ fontSize: 16, color: 'success.main' }} />}
              {trend === 'down' && <ArrowDownward sx={{ fontSize: 16, color: 'error.main' }} />}
              <Typography 
                variant="caption" 
                color={trend === 'up' ? 'success.main' : trend === 'down' ? 'error.main' : 'text.secondary'}
              >
                {trendValue} vs last week
              </Typography>
            </Stack>
          )}
        </Box>
        <Box
          sx={{
            width: 56,
            height: 56,
            borderRadius: 3,
            background: `linear-gradient(135deg, ${alpha(color, 0.2)} 0%, ${alpha(color, 0.1)} 100%)`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          {icon}
        </Box>
      </Box>
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const { data: apiData, isLoading, refetch } = useGetAnalyticsDashboardQuery({});
  const [data] = useState(mockDashboardData);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Use API data if available, otherwise use mock data
  const dashboardData = apiData || data;

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
            Dashboard
          </Typography>
          <Typography color="text.secondary">
            Real-time flight analytics and insights
          </Typography>
        </Box>
        <Stack direction="row" alignItems="center" spacing={2}>
          <Chip 
            icon={<Schedule />} 
            label={currentTime.toLocaleTimeString()} 
            variant="outlined"
            sx={{ fontFamily: 'monospace' }}
          />
          <Tooltip title="Refresh data">
            <IconButton onClick={() => refetch()} sx={{ bgcolor: alpha('#fff', 0.05) }}>
              <Refresh />
            </IconButton>
          </Tooltip>
        </Stack>
      </Box>

      {isLoading && <LinearProgress sx={{ mb: 3 }} />}

      {/* Stats Grid */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Flights Today"
            value={dashboardData.total_flights?.toLocaleString() || '0'}
            icon={<Flight sx={{ fontSize: 28, color: '#6366f1' }} />}
            color="#6366f1"
            trend="up"
            trendValue="+12%"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Bookings Today"
            value={dashboardData.total_bookings?.toLocaleString() || '0'}
            icon={<People sx={{ fontSize: 28, color: '#10b981' }} />}
            color="#10b981"
            trend="up"
            trendValue="+8%"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Average Price"
            value={`₹${(dashboardData.average_price || 0).toLocaleString()}`}
            icon={<AttachMoney sx={{ fontSize: 28, color: '#f59e0b' }} />}
            color="#f59e0b"
            trend="down"
            trendValue="-5%"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Revenue Today"
            value={`₹${((data.revenue_today || 0) / 100000).toFixed(1)}L`}
            icon={<Analytics sx={{ fontSize: 28, color: '#ec4899' }} />}
            color="#ec4899"
            trend="up"
            trendValue="+18%"
          />
        </Grid>
      </Grid>

      {/* Main Content Grid */}
      <Grid container spacing={3}>
        {/* Top Routes */}
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
              Top Performing Routes
            </Typography>
            <Stack spacing={2}>
              {data.top_routes.map((route, index) => (
                <Box
                  key={index}
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    background: alpha('#fff', 0.02),
                    border: '1px solid',
                    borderColor: alpha('#fff', 0.05),
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Box
                      sx={{
                        width: 40,
                        height: 40,
                        borderRadius: 2,
                        background: `linear-gradient(135deg, ${alpha('#6366f1', 0.3)} 0%, ${alpha('#8b5cf6', 0.2)} 100%)`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: 700,
                      }}
                    >
                      {index + 1}
                    </Box>
                    <Box>
                      <Typography fontWeight="600">{route.route}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {route.flights} flights today
                      </Typography>
                    </Box>
                  </Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
                    <Box textAlign="right">
                      <Typography fontWeight="600">₹{route.avg_price.toLocaleString()}</Typography>
                      <Stack direction="row" alignItems="center" spacing={0.5} justifyContent="flex-end">
                        {route.trend === 'up' && <TrendingUp sx={{ fontSize: 14, color: 'error.main' }} />}
                        {route.trend === 'down' && <TrendingDown sx={{ fontSize: 14, color: 'success.main' }} />}
                        <Typography 
                          variant="caption" 
                          color={route.trend === 'up' ? 'error.main' : route.trend === 'down' ? 'success.main' : 'text.secondary'}
                        >
                          {route.change > 0 ? '+' : ''}{route.change}%
                        </Typography>
                      </Stack>
                    </Box>
                    <LinearProgress
                      variant="determinate"
                      value={(route.flights / 250) * 100}
                      sx={{ 
                        width: 100, 
                        height: 8, 
                        borderRadius: 1,
                        bgcolor: alpha('#fff', 0.05),
                        '& .MuiLinearProgress-bar': {
                          background: 'linear-gradient(90deg, #6366f1, #8b5cf6)',
                        }
                      }}
                    />
                  </Box>
                </Box>
              ))}
            </Stack>
          </Paper>
        </Grid>

        {/* Price Alerts */}
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
              Price Alerts
            </Typography>
            <Stack spacing={2}>
              {data.price_alerts.map((alert, index) => (
                <Box
                  key={index}
                  sx={{
                    p: 2,
                    borderRadius: 2,
                    background: alpha(
                      alert.type === 'drop' ? '#10b981' : 
                      alert.type === 'surge' ? '#ef4444' : '#f59e0b',
                      0.1
                    ),
                    border: '1px solid',
                    borderColor: alpha(
                      alert.type === 'drop' ? '#10b981' : 
                      alert.type === 'surge' ? '#ef4444' : '#f59e0b',
                      0.2
                    ),
                  }}
                >
                  <Stack direction="row" alignItems="center" spacing={1} mb={0.5}>
                    <LocalOffer sx={{ 
                      fontSize: 18, 
                      color: alert.type === 'drop' ? '#10b981' : 
                             alert.type === 'surge' ? '#ef4444' : '#f59e0b'
                    }} />
                    <Typography fontWeight="600">{alert.route}</Typography>
                  </Stack>
                  <Typography variant="body2" color="text.secondary">
                    {alert.message}
                  </Typography>
                </Box>
              ))}
            </Stack>

            <Divider sx={{ my: 3, borderColor: alpha('#fff', 0.1) }} />

            <Typography variant="h6" fontWeight="700" mb={2}>
              Airline Performance
            </Typography>
            <Stack spacing={2}>
              {data.airline_performance.map((airline, index) => (
                <Box key={index}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                    <Typography variant="body2">{airline.airline}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {airline.satisfaction}% satisfaction
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={airline.satisfaction}
                    sx={{ 
                      height: 6, 
                      borderRadius: 1,
                      bgcolor: alpha('#fff', 0.05),
                      '& .MuiLinearProgress-bar': {
                        background: airline.satisfaction > 90 ? 
                          'linear-gradient(90deg, #10b981, #34d399)' :
                          airline.satisfaction > 80 ?
                          'linear-gradient(90deg, #6366f1, #8b5cf6)' :
                          'linear-gradient(90deg, #f59e0b, #fbbf24)',
                      }
                    }}
                  />
                </Box>
              ))}
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
