import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme,
  useMediaQuery,
  Avatar,
  Menu,
  MenuItem,
  Badge,
  Chip,
} from '@mui/material';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import {
  FlightTakeoff,
  Menu as MenuIcon,
  Search,
  TrendingUp,
  CardGiftcard,
  BookOnline,
  Dashboard,
  Analytics,
  AccountCircle,
  Notifications,
  DirectionsBus,
  Hotel,
  Train,
  Sparkles,
} from '@mui/icons-material';

const Navigation = () => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const location = useLocation();

  const menuItems = [
    { text: 'Home', icon: <FlightTakeoff />, path: '/' },
    { text: 'Search', icon: <Search />, path: '/search' },
    { text: 'Forecast', icon: <TrendingUp />, path: '/forecast' },
    { text: 'Analytics', icon: <Analytics />, path: '/analytics' },
    { text: 'Packages', icon: <CardGiftcard />, path: '/packages' },
  ];

  const isActive = (path: string) => location.pathname === path;

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <AppBar 
        position="sticky" 
        elevation={0}
        sx={{ 
          background: 'rgba(19, 19, 26, 0.8)',
          backdropFilter: 'blur(20px)',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        }}
      >
        <Toolbar sx={{ py: 1 }}>
          {isMobile && (
            <IconButton
              color="inherit"
              edge="start"
              onClick={() => setDrawerOpen(true)}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, flexGrow: isMobile ? 1 : 0 }}>
            <Box
              sx={{
                background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
                borderRadius: 2,
                p: 0.8,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <FlightTakeoff sx={{ fontSize: 24 }} />
            </Box>
            <Box>
              <Typography 
                variant="h6" 
                component="div" 
                sx={{ 
                  fontWeight: 800, 
                  lineHeight: 1,
                  background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                SkyPrice
              </Typography>
              <Typography 
                variant="caption" 
                sx={{ 
                  color: 'text.secondary',
                  fontSize: '0.7rem',
                  lineHeight: 1,
                }}
              >
                AI-Powered Flight Intelligence
              </Typography>
            </Box>
            <Chip 
              label="BETA" 
              size="small" 
              sx={{ 
                ml: 1,
                height: 20,
                fontSize: '0.65rem',
                fontWeight: 700,
                background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
                color: 'white',
              }}
            />
          </Box>

          <Box sx={{ flexGrow: 1 }} />

          {!isMobile && (
            <Box sx={{ display: 'flex', gap: 0.5, mr: 2 }}>
              {menuItems.map((item) => (
                <Button
                  key={item.path}
                  color="inherit"
                  component={RouterLink}
                  to={item.path}
                  startIcon={item.icon}
                  sx={{
                    px: 2.5,
                    py: 1,
                    borderRadius: 2,
                    fontSize: '0.875rem',
                    fontWeight: 600,
                    color: isActive(item.path) ? 'primary.main' : 'text.secondary',
                    bgcolor: isActive(item.path) ? 'rgba(99, 102, 241, 0.1)' : 'transparent',
                    border: isActive(item.path) ? '1px solid rgba(99, 102, 241, 0.3)' : '1px solid transparent',
                    transition: 'all 0.2s ease',
                    '&:hover': { 
                      bgcolor: 'rgba(99, 102, 241, 0.1)',
                      borderColor: 'rgba(99, 102, 241, 0.3)',
                      color: 'primary.main',
                    },
                  }}
                >
                  {item.text}
                </Button>
              ))}
            </Box>
          )}

          <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
            <IconButton color="inherit">
              <Badge badgeContent={3} color="error">
                <Notifications />
              </Badge>
            </IconButton>
            <IconButton color="inherit" onClick={handleProfileMenuOpen}>
              <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>P</Avatar>
            </IconButton>
          </Box>
        </Toolbar>

        {/* Quick Access Bar */}
        <Box sx={{ bgcolor: 'rgba(0,0,0,0.1)', px: 2, py: 0.5, display: 'flex', gap: 2, overflowX: 'auto' }}>
          <Button size="small" startIcon={<FlightTakeoff />} sx={{ color: 'white', minWidth: 'auto' }}>
            Flights
          </Button>
          <Button size="small" startIcon={<Train />} sx={{ color: 'white', minWidth: 'auto' }}>
            Trains
          </Button>
          <Button size="small" startIcon={<DirectionsBus />} sx={{ color: 'white', minWidth: 'auto' }}>
            Buses
          </Button>
          <Button size="small" startIcon={<Hotel />} sx={{ color: 'white', minWidth: 'auto' }}>
            Hotels
          </Button>
        </Box>
      </AppBar>

      {/* Mobile Drawer */}
      <Drawer anchor="left" open={drawerOpen} onClose={() => setDrawerOpen(false)}>
        <Box sx={{ width: 250 }} role="presentation" onClick={() => setDrawerOpen(false)}>
          <Box sx={{ p: 2, bgcolor: 'primary.main', color: 'white' }}>
            <Typography variant="h6" fontWeight="bold">
              Travel Engine
            </Typography>
            <Typography variant="body2">DAA Project 17</Typography>
          </Box>
          <List>
            {menuItems.map((item) => (
              <ListItem
                button
                key={item.path}
                component={RouterLink}
                to={item.path}
                selected={isActive(item.path)}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>

      {/* Profile Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <MenuItem onClick={handleMenuClose}>Profile</MenuItem>
        <MenuItem onClick={handleMenuClose}>My Bookings</MenuItem>
        <MenuItem onClick={handleMenuClose}>Settings</MenuItem>
        <MenuItem onClick={handleMenuClose}>Logout</MenuItem>
      </Menu>
    </>
  );
};

export default Navigation;
