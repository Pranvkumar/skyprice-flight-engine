import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  Button,
  Stepper,
  Step,
  StepLabel,
  Checkbox,
  FormControlLabel,
  Chip,
  Stack,
  Alert,
  Paper,
  Divider,
  Radio,
  RadioGroup,
  Avatar,
} from '@mui/material';
import {
  Flight,
  Hotel,
  DirectionsCar,
  CheckCircle,
  Savings,
  Star,
} from '@mui/icons-material';

const PackageBuilder: React.FC = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [selectedPackage, setSelectedPackage] = useState('vacation');
  const [includeFlight, setIncludeFlight] = useState(true);
  const [includeHotel, setIncludeHotel] = useState(true);
  const [includeCar, setIncludeCar] = useState(false);

  const steps = ['Choose Package Type', 'Select Services', 'Review & Book'];

  const packageTypes = [
    {
      id: 'vacation',
      title: '🏖️ Vacation Package',
      subtitle: 'Perfect for leisure trips',
      discount: 15,
      includes: ['Flight', 'Hotel', 'Car Rental'],
      price: 25000,
      savings: 4500,
    },
    {
      id: 'business',
      title: '💼 Business Package',
      subtitle: 'For professional travel',
      discount: 10,
      includes: ['Business Class', '4-Star Hotel', 'Airport Transfer'],
      price: 45000,
      savings: 5000,
    },
    {
      id: 'weekend',
      title: '🎉 Weekend Getaway',
      subtitle: 'Quick 2-night escape',
      discount: 12,
      includes: ['Flight', '2 Nights Hotel', 'Breakfast'],
      price: 15000,
      savings: 2000,
    },
    {
      id: 'group',
      title: '👥 Group Package',
      subtitle: 'For 4+ people',
      discount: 20,
      includes: ['Group Discount', 'Flexible Booking', 'Coordinator'],
      price: 18000,
      savings: 4500,
    },
  ];

  const handleNext = () => {
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const calculateTotal = () => {
    const selected = packageTypes.find((p) => p.id === selectedPackage);
    return selected ? selected.price : 0;
  };

  const calculateSavings = () => {
    const selected = packageTypes.find((p) => p.id === selectedPackage);
    return selected ? selected.savings : 0;
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4, textAlign: 'center' }}>
        <Typography variant="h3" gutterBottom fontWeight="bold">
          🎁 Build Your Perfect Package
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Save up to 20% by bundling your travel services
        </Typography>
      </Box>

      {/* Stepper */}
      <Card sx={{ mb: 4 }}>
        <CardContent sx={{ p: 4 }}>
          <Stepper activeStep={activeStep}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>
        </CardContent>
      </Card>

      {/* Step 1: Choose Package Type */}
      {activeStep === 0 && (
        <Grid container spacing={3}>
          {packageTypes.map((pkg) => (
            <Grid item xs={12} md={6} key={pkg.id}>
              <Card
                sx={{
                  cursor: 'pointer',
                  border: selectedPackage === pkg.id ? 3 : 1,
                  borderColor: selectedPackage === pkg.id ? 'primary.main' : 'divider',
                  position: 'relative',
                  '&:hover': { boxShadow: 6 },
                }}
                onClick={() => setSelectedPackage(pkg.id)}
              >
                {selectedPackage === pkg.id && (
                  <Chip
                    label="Selected"
                    color="primary"
                    icon={<CheckCircle />}
                    sx={{ position: 'absolute', top: 16, right: 16 }}
                  />
                )}

                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h4" gutterBottom>
                    {pkg.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" gutterBottom>
                    {pkg.subtitle}
                  </Typography>

                  <Box sx={{ my: 3 }}>
                    <Chip label={`${pkg.discount}% OFF`} color="success" size="medium" icon={<Savings />} />
                  </Box>

                  <Stack spacing={1} sx={{ mb: 3 }}>
                    {pkg.includes.map((item, index) => (
                      <Typography key={index} variant="body2">
                        ✓ {item}
                      </Typography>
                    ))}
                  </Stack>

                  <Divider sx={{ my: 2 }} />

                  <Stack direction="row" justifyContent="space-between" alignItems="center">
                    <Box>
                      <Typography variant="h4" fontWeight="bold" color="primary">
                        ₹{pkg.price.toLocaleString()}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        You save ₹{pkg.savings.toLocaleString()}
                      </Typography>
                    </Box>
                    <Button variant="contained" disabled={selectedPackage !== pkg.id}>
                      Choose
                    </Button>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      {/* Step 2: Select Services */}
      {activeStep === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <ServiceCard
              icon={<Flight />}
              title="Flight"
              description="Round-trip flights"
              price={12000}
              checked={includeFlight}
              onChange={(e) => setIncludeFlight(e.target.checked)}
              color="#2196f3"
              features={['Free cancellation', 'Extra baggage', 'Seat selection']}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <ServiceCard
              icon={<Hotel />}
              title="Hotel"
              description="3-4 star hotels"
              price={8000}
              checked={includeHotel}
              onChange={(e) => setIncludeHotel(e.target.checked)}
              color="#9c27b0"
              features={['Free breakfast', 'Pool access', 'Free WiFi']}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <ServiceCard
              icon={<DirectionsCar />}
              title="Car Rental"
              description="Self-drive cars"
              price={5000}
              checked={includeCar}
              onChange={(e) => setIncludeCar(e.target.checked)}
              color="#f44336"
              features={['Unlimited km', 'GPS included', 'Insurance']}
            />
          </Grid>

          <Grid item xs={12}>
            <Alert severity="info" icon={<Star />}>
              <strong>Smart Tip:</strong> Adding more services increases your discount! Bundle all 3 for maximum savings.
            </Alert>
          </Grid>
        </Grid>
      )}

      {/* Step 3: Review & Book */}
      {activeStep === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h5" gutterBottom fontWeight="bold">
                  Package Summary
                </Typography>
                <Divider sx={{ my: 2 }} />

                <Stack spacing={2}>
                  {includeFlight && (
                    <Stack direction="row" justifyContent="space-between">
                      <Stack direction="row" spacing={2}>
                        <Avatar sx={{ bgcolor: '#2196f3' }}>
                          <Flight />
                        </Avatar>
                        <Box>
                          <Typography variant="body1" fontWeight="medium">
                            Round-trip Flight
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Economy class • 2 passengers
                          </Typography>
                        </Box>
                      </Stack>
                      <Typography variant="h6">₹12,000</Typography>
                    </Stack>
                  )}

                  {includeHotel && (
                    <Stack direction="row" justifyContent="space-between">
                      <Stack direction="row" spacing={2}>
                        <Avatar sx={{ bgcolor: '#9c27b0' }}>
                          <Hotel />
                        </Avatar>
                        <Box>
                          <Typography variant="body1" fontWeight="medium">
                            Hotel Stay
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            3 nights • Double room
                          </Typography>
                        </Box>
                      </Stack>
                      <Typography variant="h6">₹8,000</Typography>
                    </Stack>
                  )}

                  {includeCar && (
                    <Stack direction="row" justifyContent="space-between">
                      <Stack direction="row" spacing={2}>
                        <Avatar sx={{ bgcolor: '#f44336' }}>
                          <DirectionsCar />
                        </Avatar>
                        <Box>
                          <Typography variant="body1" fontWeight="medium">
                            Car Rental
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            Sedan • 3 days
                          </Typography>
                        </Box>
                      </Stack>
                      <Typography variant="h6">₹5,000</Typography>
                    </Stack>
                  )}
                </Stack>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card sx={{ position: 'sticky', top: 16 }}>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Price Breakdown
                </Typography>
                <Divider sx={{ my: 2 }} />

                <Stack spacing={2}>
                  <Stack direction="row" justifyContent="space-between">
                    <Typography>Subtotal</Typography>
                    <Typography fontWeight="medium">₹{calculateTotal().toLocaleString()}</Typography>
                  </Stack>
                  <Stack direction="row" justifyContent="space-between">
                    <Typography color="success.main">Package Discount</Typography>
                    <Typography color="success.main" fontWeight="medium">
                      -₹{calculateSavings().toLocaleString()}
                    </Typography>
                  </Stack>
                  <Divider />
                  <Stack direction="row" justifyContent="space-between">
                    <Typography variant="h6">Total</Typography>
                    <Typography variant="h5" fontWeight="bold" color="primary">
                      ₹{(calculateTotal() - calculateSavings()).toLocaleString()}
                    </Typography>
                  </Stack>
                </Stack>

                <Button fullWidth variant="contained" size="large" sx={{ mt: 3 }}>
                  Confirm Booking
                </Button>

                <Alert severity="success" sx={{ mt: 2 }}>
                  You're saving ₹{calculateSavings().toLocaleString()} with this package!
                </Alert>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Navigation Buttons */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button disabled={activeStep === 0} onClick={handleBack} size="large">
          Back
        </Button>
        <Button variant="contained" onClick={handleNext} size="large" disabled={activeStep === steps.length - 1}>
          {activeStep === steps.length - 2 ? 'Review Booking' : 'Next'}
        </Button>
      </Box>
    </Box>
  );
};

// Service Card Component
interface ServiceCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  price: number;
  checked: boolean;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  color: string;
  features: string[];
}

const ServiceCard: React.FC<ServiceCardProps> = ({ icon, title, description, price, checked, onChange, color, features }) => {
  return (
    <Card sx={{ height: '100%', border: checked ? 3 : 1, borderColor: checked ? color : 'divider' }}>
      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="start" sx={{ mb: 2 }}>
          <Avatar sx={{ bgcolor: color, width: 56, height: 56 }}>{icon}</Avatar>
          <Checkbox checked={checked} onChange={onChange} sx={{ '& .MuiSvgIcon-root': { fontSize: 32 } }} />
        </Stack>

        <Typography variant="h5" gutterBottom>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {description}
        </Typography>

        <Typography variant="h4" fontWeight="bold" color="primary" sx={{ my: 2 }}>
          ₹{price.toLocaleString()}
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Stack spacing={1}>
          {features.map((feature, index) => (
            <Typography key={index} variant="body2">
              ✓ {feature}
            </Typography>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
};

export default PackageBuilder;
