import React from 'react';
import { Box, Typography, Paper, Grid, Card, CardContent } from '@mui/material';
import { useGetAnalyticsDashboardQuery } from '../store/apiSlice';

const Dashboard = () => {
  const { data, isLoading } = useGetAnalyticsDashboardQuery({});

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        System Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Flights
              </Typography>
              <Typography variant="h4">
                {data?.total_flights || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Total Bookings
              </Typography>
              <Typography variant="h4">
                {data?.total_bookings || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Average Price
              </Typography>
              <Typography variant="h4">
                ₹{data?.average_price?.toFixed(0) || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>
                Active Routes
              </Typography>
              <Typography variant="h4">
                {data?.top_routes?.length || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
