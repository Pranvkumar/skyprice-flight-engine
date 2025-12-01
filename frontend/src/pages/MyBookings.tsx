import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Button,
  Chip,
  Stack,
  Avatar,
  Divider,
  Tab,
  Tabs,
  TextField,
  Paper,
  IconButton,
} from '@mui/material';
import {
  Flight,
  Train,
  DirectionsBus,
  Hotel,
  DirectionsCar,
  QrCode2,
  Download,
  Cancel,
  CheckCircle,
  Schedule,
  LocalOffer,
} from '@mui/icons-material';

interface Booking {
  id: string;
  type: 'flight' | 'train' | 'bus' | 'hotel' | 'car';
  status: 'confirmed' | 'pending' | 'completed' | 'cancelled';
  bookingRef: string;
  from: string;
  to: string;
  date: string;
  time: string;
  passengers: number;
  price: number;
  provider: string;
  isPackage: boolean;
}

const MyBookings: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');

  // Sample booking data
  const bookings: Booking[] = [
    {
      id: 'BK001',
      type: 'flight',
      status: 'confirmed',
      bookingRef: 'FLT2024001',
      from: 'DEL',
      to: 'BOM',
      date: '2025-12-15',
      time: '14:30',
      passengers: 2,
      price: 12000,
      provider: 'IndiGo',
      isPackage: true,
    },
    {
      id: 'BK002',
      type: 'train',
      status: 'confirmed',
      bookingRef: 'TRN2024001',
      from: 'Mumbai',
      to: 'Pune',
      date: '2025-12-10',
      time: '08:00',
      passengers: 1,
      price: 500,
      provider: 'Shatabdi Express',
      isPackage: false,
    },
    {
      id: 'BK003',
      type: 'hotel',
      status: 'pending',
      bookingRef: 'HTL2024001',
      from: 'Mumbai',
      to: 'Mumbai',
      date: '2025-12-15',
      time: '14:00',
      passengers: 2,
      price: 8000,
      provider: 'Taj Hotels',
      isPackage: true,
    },
  ];

  const getIcon = (type: string) => {
    const icons = {
      flight: <Flight />,
      train: <Train />,
      bus: <DirectionsBus />,
      hotel: <Hotel />,
      car: <DirectionsCar />,
    };
    return icons[type as keyof typeof icons];
  };

  const getStatusColor = (status: string) => {
    const colors = {
      confirmed: 'success',
      pending: 'warning',
      completed: 'info',
      cancelled: 'error',
    };
    return colors[status as keyof typeof colors];
  };

  const getTypeColor = (type: string) => {
    const colors = {
      flight: '#2196f3',
      train: '#4caf50',
      bus: '#ff9800',
      hotel: '#9c27b0',
      car: '#f44336',
    };
    return colors[type as keyof typeof colors];
  };

  const filteredBookings = bookings.filter((booking) => {
    if (tabValue === 0) return true; // All
    if (tabValue === 1) return booking.status === 'confirmed';
    if (tabValue === 2) return booking.status === 'pending';
    if (tabValue === 3) return booking.status === 'completed';
    if (tabValue === 4) return booking.status === 'cancelled';
    return true;
  });

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" gutterBottom fontWeight="bold">
          📋 My Bookings
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Manage all your travel bookings in one place
        </Typography>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'success.light', color: 'white' }}>
            <Typography variant="h3" fontWeight="bold">
              {bookings.filter((b) => b.status === 'confirmed').length}
            </Typography>
            <Typography variant="body1">Confirmed</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'warning.light', color: 'white' }}>
            <Typography variant="h3" fontWeight="bold">
              {bookings.filter((b) => b.status === 'pending').length}
            </Typography>
            <Typography variant="body1">Pending</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'info.light', color: 'white' }}>
            <Typography variant="h3" fontWeight="bold">
              {bookings.filter((b) => b.status === 'completed').length}
            </Typography>
            <Typography variant="body1">Completed</Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'primary.main', color: 'white' }}>
            <Typography variant="h3" fontWeight="bold">
              ₹{bookings.reduce((sum, b) => sum + b.price, 0).toLocaleString()}
            </Typography>
            <Typography variant="body1">Total Spent</Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Search and Filter */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} alignItems="center">
            <TextField
              fullWidth
              placeholder="Search by booking ref, destination..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              variant="outlined"
              size="small"
            />
            <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)} sx={{ minWidth: 400 }}>
              <Tab label="All" />
              <Tab label="Confirmed" />
              <Tab label="Pending" />
              <Tab label="Completed" />
              <Tab label="Cancelled" />
            </Tabs>
          </Stack>
        </CardContent>
      </Card>

      {/* Bookings List */}
      <Stack spacing={3}>
        {filteredBookings.map((booking) => (
          <Card key={booking.id} sx={{ '&:hover': { boxShadow: 6 } }}>
            <CardContent sx={{ p: 3 }}>
              <Grid container spacing={3} alignItems="center">
                {/* Icon and Type */}
                <Grid item xs={12} md={2}>
                  <Stack direction="row" spacing={2} alignItems="center">
                    <Avatar sx={{ bgcolor: getTypeColor(booking.type), width: 56, height: 56 }}>
                      {getIcon(booking.type)}
                    </Avatar>
                    <Box>
                      <Typography variant="h6" textTransform="capitalize">
                        {booking.type}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {booking.bookingRef}
                      </Typography>
                    </Box>
                  </Stack>
                </Grid>

                {/* Route Info */}
                <Grid item xs={12} md={3}>
                  <Typography variant="body2" color="text.secondary">
                    Route
                  </Typography>
                  <Typography variant="h6" fontWeight="medium">
                    {booking.from} → {booking.to}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {booking.provider}
                  </Typography>
                </Grid>

                {/* Date and Time */}
                <Grid item xs={12} md={2}>
                  <Typography variant="body2" color="text.secondary">
                    Date & Time
                  </Typography>
                  <Typography variant="body1" fontWeight="medium">
                    {new Date(booking.date).toLocaleDateString()}
                  </Typography>
                  <Typography variant="body2">{booking.time}</Typography>
                </Grid>

                {/* Passengers and Price */}
                <Grid item xs={12} md={2}>
                  <Typography variant="body2" color="text.secondary">
                    Passengers
                  </Typography>
                  <Typography variant="body1" fontWeight="medium">
                    {booking.passengers}
                  </Typography>
                  <Typography variant="h6" color="primary" fontWeight="bold">
                    ₹{booking.price.toLocaleString()}
                  </Typography>
                </Grid>

                {/* Status and Actions */}
                <Grid item xs={12} md={3}>
                  <Stack spacing={1}>
                    <Stack direction="row" spacing={1}>
                      <Chip
                        label={booking.status.toUpperCase()}
                        color={getStatusColor(booking.status) as any}
                        size="small"
                        icon={booking.status === 'confirmed' ? <CheckCircle /> : <Schedule />}
                      />
                      {booking.isPackage && <Chip label="PACKAGE" color="secondary" size="small" icon={<LocalOffer />} />}
                    </Stack>

                    <Stack direction="row" spacing={1}>
                      <Button size="small" startIcon={<QrCode2 />} variant="outlined">
                        Ticket
                      </Button>
                      <IconButton size="small" color="primary">
                        <Download />
                      </IconButton>
                      {booking.status === 'confirmed' && (
                        <IconButton size="small" color="error">
                          <Cancel />
                        </IconButton>
                      )}
                    </Stack>
                  </Stack>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        ))}
      </Stack>

      {filteredBookings.length === 0 && (
        <Paper sx={{ p: 6, textAlign: 'center' }}>
          <Typography variant="h5" color="text.secondary">
            No bookings found
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
            Start planning your next trip!
          </Typography>
          <Button variant="contained" sx={{ mt: 3 }}>
            Search Travel Options
          </Button>
        </Paper>
      )}
    </Box>
  );
};

export default MyBookings;
