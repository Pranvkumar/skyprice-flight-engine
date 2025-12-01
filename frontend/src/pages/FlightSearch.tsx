import React from 'react';
import { Box, Typography, Paper, CircularProgress } from '@mui/material';

const FlightSearch = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Flight Search
      </Typography>
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" color="text.secondary">
          Flight search interface coming soon...
        </Typography>
      </Paper>
    </Box>
  );
};

export default FlightSearch;
