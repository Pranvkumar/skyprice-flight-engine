import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box, ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import FlightSearch from './pages/FlightSearch';
import PriceForecasting from './pages/PriceForecasting';
import Analytics from './pages/Analytics';
import Dashboard from './pages/Dashboard';
import MultiModalSearch from './pages/MultiModalSearch';
import PackageBuilder from './pages/PackageBuilder';
import MyBookings from './pages/MyBookings';

// Modern dark theme inspired by Godly designs
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#6366f1',
      light: '#818cf8',
      dark: '#4f46e5',
    },
    secondary: {
      main: '#ec4899',
      light: '#f472b6',
      dark: '#db2777',
    },
    background: {
      default: '#0a0a0f',
      paper: '#13131a',
    },
    text: {
      primary: '#f8fafc',
      secondary: '#94a3b8',
    },
  },
  typography: {
    fontFamily: '"Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    h1: {
      fontSize: '4rem',
      fontWeight: 800,
      lineHeight: 1.1,
      letterSpacing: '-0.02em',
    },
    h2: {
      fontSize: '3rem',
      fontWeight: 700,
      lineHeight: 1.2,
      letterSpacing: '-0.01em',
    },
    h3: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
    },
  },
  shape: {
    borderRadius: 16,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 12,
          padding: '12px 32px',
          fontSize: '1rem',
          fontWeight: 600,
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 20px 40px rgba(99, 102, 241, 0.3)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          background: 'rgba(19, 19, 26, 0.8)',
          backdropFilter: 'blur(20px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0 24px 48px rgba(0, 0, 0, 0.3)',
            borderColor: 'rgba(99, 102, 241, 0.3)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box 
        sx={{ 
          display: 'flex', 
          flexDirection: 'column', 
          minHeight: '100vh',
          background: 'linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #16213e 100%)',
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.1) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 50%)',
            pointerEvents: 'none',
          }
        }}
      >
        <Navigation />
        <Box 
          component="main"
          sx={{ 
            flex: 1, 
            position: 'relative',
            zIndex: 1,
            width: '100%',
            maxWidth: '1400px',
            margin: '0 auto',
            px: { xs: 2, sm: 3, md: 4 },
            py: { xs: 3, sm: 4, md: 6 },
          }}
        >
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<MultiModalSearch />} />
            <Route path="/flights" element={<FlightSearch />} />
            <Route path="/forecast" element={<PriceForecasting />} />
            <Route path="/packages" element={<PackageBuilder />} />
            <Route path="/bookings" element={<MyBookings />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </Box>
        
        {/* Modern Footer */}
        <Box
          component="footer"
          sx={{
            position: 'relative',
            zIndex: 1,
            py: 4,
            px: 2,
            mt: 'auto',
            borderTop: '1px solid rgba(255, 255, 255, 0.1)',
            background: 'rgba(19, 19, 26, 0.5)',
            backdropFilter: 'blur(20px)',
          }}
        >
          <Box 
            sx={{ 
              maxWidth: '1400px',
              margin: '0 auto',
              textAlign: 'center',
              color: 'text.secondary',
              fontSize: '0.875rem',
            }}
          >
            <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center', alignItems: 'center', flexWrap: 'wrap' }}>
              <Box component="span" sx={{ color: 'text.primary', fontWeight: 600 }}>
                Flight Price Intelligence
              </Box>
              <Box component="span" sx={{ opacity: 0.5 }}>•</Box>
              <Box component="span">
                Pranav (590011587) & Om (590014492)
              </Box>
              <Box component="span" sx={{ opacity: 0.5 }}>•</Box>
              <Box component="span">DAA Project 17 • 2025</Box>
            </Box>
          </Box>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
