import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const Analytics = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Analytics Dashboard
      </Typography>
      <Paper sx={{ p: 4, textAlign: 'center' }}>
        <Typography variant="h6" color="text.secondary">
          Analytics dashboard coming soon...
        </Typography>
      </Paper>
    </Box>
  );
};

export default Analytics;
