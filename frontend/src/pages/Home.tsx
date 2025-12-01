import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Container,
  alpha,
  Stack,
  Chip,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import {
  TrendingUp,
  Search,
  Analytics,
  Speed,
  FlightTakeoff,
  Schedule,
  Savings,
  AutoAwesome,
  ArrowForward,
  Bolt,
  LocalOffer,
} from '@mui/icons-material';

const Home = () => {
  const navigate = useNavigate();

  const features = [
    {
      title: 'Smart Search',
      description: 'AI-powered flight search with real-time pricing from Amadeus API',
      icon: <Search sx={{ fontSize: 40 }} />,
      path: '/search',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    },
    {
      title: 'Price Forecasting',
      description: 'Predict future prices using divide-and-conquer ML algorithms',
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      path: '/forecast',
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    },
    {
      title: 'Analytics Dashboard',
      description: 'Deep insights into pricing trends and market patterns',
      icon: <Analytics sx={{ fontSize: 40 }} />,
      path: '/analytics',
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    },
    {
      title: 'Price Alerts',
      description: 'Get notified when prices drop to your target',
      icon: <LocalOffer sx={{ fontSize: 40 }} />,
      path: '/alerts',
      gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    },
  ];

  const stats = [
    { label: 'Routes Monitored', value: '500+', icon: <FlightTakeoff /> },
    { label: 'Prediction Accuracy', value: '94%', icon: <Speed /> },
    { label: 'Avg. Savings', value: '₹3,500', icon: <Savings /> },
    { label: 'Response Time', value: '<100ms', icon: <Schedule /> },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          textAlign: 'center',
          py: { xs: 8, md: 12 },
          position: 'relative',
        }}
      >
        {/* Floating Elements */}
        <Box
          sx={{
            position: 'absolute',
            top: '20%',
            left: '10%',
            width: 100,
            height: 100,
            borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(99, 102, 241, 0.3) 0%, transparent 70%)',
            filter: 'blur(40px)',
            animation: 'float 6s ease-in-out infinite',
            '@keyframes float': {
              '0%, 100%': { transform: 'translateY(0px)' },
              '50%': { transform: 'translateY(-20px)' },
            },
          }}
        />
        <Box
          sx={{
            position: 'absolute',
            top: '60%',
            right: '15%',
            width: 120,
            height: 120,
            borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(236, 72, 153, 0.3) 0%, transparent 70%)',
            filter: 'blur(40px)',
            animation: 'float 8s ease-in-out infinite',
          }}
        />

        <Chip
          icon={<Bolt sx={{ fontSize: 16 }} />}
          label="Powered by Amadeus API"
          sx={{
            mb: 3,
            py: 2.5,
            px: 1,
            fontSize: '0.875rem',
            fontWeight: 600,
            background: 'rgba(99, 102, 241, 0.1)',
            border: '1px solid rgba(99, 102, 241, 0.3)',
            color: 'primary.main',
          }}
        />

        <Typography
          variant="h1"
          sx={{
            fontSize: { xs: '2.5rem', sm: '3.5rem', md: '4.5rem' },
            fontWeight: 900,
            mb: 2,
            background: 'linear-gradient(135deg, #ffffff 0%, #94a3b8 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            lineHeight: 1.1,
          }}
        >
          Never Overpay for
          <br />
          <Box
            component="span"
            sx={{
              background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Flights Again
          </Box>
        </Typography>

        <Typography
          variant="h5"
          sx={{
            mb: 5,
            color: 'text.secondary',
            fontSize: { xs: '1rem', md: '1.25rem' },
            maxWidth: 700,
            mx: 'auto',
            lineHeight: 1.6,
          }}
        >
          AI-powered price forecasting using divide-and-conquer algorithms.
          <br />
          Get real-time insights and save up to 40% on every booking.
        </Typography>

        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} justifyContent="center">
          <Button
            variant="contained"
            size="large"
            endIcon={<ArrowForward />}
            onClick={() => navigate('/search')}
            sx={{
              px: 5,
              py: 2,
              fontSize: '1.1rem',
              fontWeight: 700,
              background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
              boxShadow: '0 10px 40px rgba(99, 102, 241, 0.4)',
              '&:hover': {
                boxShadow: '0 15px 50px rgba(99, 102, 241, 0.5)',
              },
            }}
          >
            Start Searching
          </Button>
          <Button
            variant="outlined"
            size="large"
            startIcon={<AutoAwesome />}
            onClick={() => navigate('/forecast')}
            sx={{
              px: 5,
              py: 2,
              fontSize: '1.1rem',
              fontWeight: 700,
              borderColor: 'rgba(99, 102, 241, 0.5)',
              color: 'primary.main',
              '&:hover': {
                borderColor: 'primary.main',
                background: 'rgba(99, 102, 241, 0.1)',
              },
            }}
          >
            View Predictions
          </Button>
        </Stack>
      </Box>

      {/* Stats Section */}
      <Box sx={{ mb: 10 }}>
        <Grid container spacing={3}>
          {stats.map((stat, index) => (
            <Grid item xs={6} md={3} key={index}>
              <Card
                sx={{
                  textAlign: 'center',
                  py: 3,
                  background: 'rgba(19, 19, 26, 0.6)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    borderColor: 'rgba(99, 102, 241, 0.5)',
                  },
                }}
              >
                <Box
                  sx={{
                    display: 'inline-flex',
                    p: 2,
                    borderRadius: 2,
                    background: 'rgba(99, 102, 241, 0.1)',
                    color: 'primary.main',
                    mb: 2,
                  }}
                >
                  {stat.icon}
                </Box>
                <Typography variant="h3" sx={{ fontWeight: 800, mb: 1 }}>
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.label}
                </Typography>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Features Grid */}
      <Box sx={{ mb: 10 }}>
        <Typography
          variant="h2"
          textAlign="center"
          sx={{
            mb: 6,
            fontWeight: 800,
            fontSize: { xs: '2rem', md: '3rem' },
          }}
        >
          Powerful Features
        </Typography>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card
                onClick={() => navigate(feature.path)}
                sx={{
                  height: '100%',
                  cursor: 'pointer',
                  position: 'relative',
                  overflow: 'hidden',
                  background: 'rgba(19, 19, 26, 0.6)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                  '&:hover': {
                    transform: 'translateY(-8px) scale(1.02)',
                    borderColor: 'transparent',
                    boxShadow: '0 30px 60px rgba(0, 0, 0, 0.4)',
                    '& .feature-gradient': {
                      opacity: 1,
                    },
                    '& .feature-icon': {
                      transform: 'scale(1.1) rotate(5deg)',
                    },
                  },
                }}
              >
                <Box
                  className="feature-gradient"
                  sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    background: feature.gradient,
                    opacity: 0,
                    transition: 'opacity 0.4s ease',
                    zIndex: 0,
                  }}
                />
                <CardContent sx={{ position: 'relative', zIndex: 1, p: 4 }}>
                  <Box
                    className="feature-icon"
                    sx={{
                      display: 'inline-flex',
                      p: 2,
                      borderRadius: 2,
                      background: alpha('#fff', 0.1),
                      mb: 3,
                      transition: 'transform 0.4s ease',
                    }}
                  >
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" sx={{ fontWeight: 700, mb: 2 }}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.7 }}>
                    {feature.description}
                  </Typography>
                  <Box
                    sx={{
                      mt: 3,
                      display: 'flex',
                      alignItems: 'center',
                      gap: 1,
                      color: 'primary.main',
                      fontWeight: 600,
                    }}
                  >
                    Explore <ArrowForward sx={{ fontSize: 18 }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* CTA Section */}
      <Card
        sx={{
          p: { xs: 4, md: 8 },
          textAlign: 'center',
          background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%)',
          border: '1px solid rgba(99, 102, 241, 0.3)',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Typography
          variant="h3"
          sx={{
            fontWeight: 800,
            mb: 2,
            fontSize: { xs: '2rem', md: '2.5rem' },
          }}
        >
          Ready to Save on Your Next Flight?
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}>
          Join thousands of smart travelers using AI to find the best flight deals
        </Typography>
        <Button
          variant="contained"
          size="large"
          endIcon={<FlightTakeoff />}
          onClick={() => navigate('/search')}
          sx={{
            px: 6,
            py: 2.5,
            fontSize: '1.2rem',
            fontWeight: 700,
            background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
            boxShadow: '0 10px 40px rgba(99, 102, 241, 0.4)',
            '&:hover': {
              boxShadow: '0 15px 50px rgba(99, 102, 241, 0.5)',
              transform: 'translateY(-2px)',
            },
          }}
        >
          Get Started Now
        </Button>
      </Card>
    </Box>
  );
};

export default Home;
