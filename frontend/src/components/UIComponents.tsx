// Modern UI Components Library

import React from 'react';
import { Box, Card, CardContent, Typography, alpha, Chip, CircularProgress } from '@mui/material';
import { TrendingUp, TrendingDown, Remove } from '@mui/icons-material';

// Glassmorphism Card
export const GlassCard = ({ children, ...props }: any) => (
  <Card
    {...props}
    sx={{
      background: 'rgba(19, 19, 26, 0.7)',
      backdropFilter: 'blur(20px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderRadius: 3,
      transition: 'all 0.3s ease',
      '&:hover': {
        transform: 'translateY(-4px)',
        borderColor: 'rgba(99, 102, 241, 0.3)',
        boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
      },
      ...props.sx,
    }}
  >
    {children}
  </Card>
);

// Price Display Card
interface PriceCardProps {
  price: number;
  currency?: string;
  label: string;
  change?: number;
  size?: 'small' | 'medium' | 'large';
}

export const PriceCard: React.FC<PriceCardProps> = ({
  price,
  currency = '₹',
  label,
  change,
  size = 'medium',
}) => {
  const getTrendIcon = () => {
    if (!change) return <Remove sx={{ fontSize: 16 }} />;
    return change > 0 ? <TrendingUp sx={{ fontSize: 16 }} /> : <TrendingDown sx={{ fontSize: 16 }} />;
  };

  const getTrendColor = () => {
    if (!change) return 'text.secondary';
    return change > 0 ? 'error.main' : 'success.main';
  };

  const fontSize = {
    small: '1.5rem',
    medium: '2.5rem',
    large: '3.5rem',
  };

  return (
    <GlassCard>
      <CardContent sx={{ p: 3 }}>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {label}
        </Typography>
        <Typography
          variant="h3"
          sx={{
            fontSize: fontSize[size],
            fontWeight: 800,
            background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            mb: 1,
          }}
        >
          {currency}{price.toLocaleString()}
        </Typography>
        {change !== undefined && (
          <Chip
            icon={getTrendIcon()}
            label={`${change > 0 ? '+' : ''}${change.toFixed(1)}%`}
            size="small"
            sx={{
              background: alpha(getTrendColor() as string, 0.1),
              color: getTrendColor(),
              fontWeight: 600,
              border: `1px solid ${alpha(getTrendColor() as string, 0.3)}`,
            }}
          />
        )}
      </CardContent>
    </GlassCard>
  );
};

// Stat Card
interface StatCardProps {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  gradient?: string;
}

export const StatCard: React.FC<StatCardProps> = ({ label, value, icon, gradient }) => (
  <GlassCard>
    <CardContent sx={{ p: 3, textAlign: 'center' }}>
      {icon && (
        <Box
          sx={{
            display: 'inline-flex',
            p: 2,
            borderRadius: 2,
            background: gradient || 'rgba(99, 102, 241, 0.1)',
            color: 'primary.main',
            mb: 2,
          }}
        >
          {icon}
        </Box>
      )}
      <Typography variant="h3" sx={{ fontWeight: 800, mb: 1 }}>
        {value}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
    </CardContent>
  </GlassCard>
);

// Gradient Button
export const GradientButton = ({ children, ...props }: any) => (
  <Box
    {...props}
    sx={{
      px: 4,
      py: 1.5,
      borderRadius: 2,
      background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
      color: 'white',
      fontWeight: 700,
      fontSize: '1rem',
      cursor: 'pointer',
      transition: 'all 0.3s ease',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 1,
      '&:hover': {
        transform: 'translateY(-2px)',
        boxShadow: '0 10px 30px rgba(99, 102, 241, 0.4)',
      },
      ...props.sx,
    }}
  >
    {children}
  </Box>
);

// Loading Spinner
export const LoadingSpinner = ({ message = 'Loading...' }: { message?: string }) => (
  <Box
    sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      py: 8,
      gap: 2,
    }}
  >
    <CircularProgress
      size={60}
      thickness={4}
      sx={{
        '& .MuiCircularProgress-circle': {
          stroke: 'url(#gradient)',
        },
      }}
    />
    <svg width="0" height="0">
      <defs>
        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#6366f1" />
          <stop offset="100%" stopColor="#ec4899" />
        </linearGradient>
      </defs>
    </svg>
    <Typography color="text.secondary">{message}</Typography>
  </Box>
);

// Section Header
interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}

export const SectionHeader: React.FC<SectionHeaderProps> = ({ title, subtitle, action }) => (
  <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
    <Box>
      <Typography variant="h4" sx={{ fontWeight: 800, mb: 1 }}>
        {title}
      </Typography>
      {subtitle && (
        <Typography variant="body2" color="text.secondary">
          {subtitle}
        </Typography>
      )}
    </Box>
    {action && <Box>{action}</Box>}
  </Box>
);

// Badge
interface BadgeProps {
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'error' | 'info';
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = 'info' }) => {
  const colors = {
    success: { bg: 'rgba(34, 197, 94, 0.1)', border: 'rgba(34, 197, 94, 0.3)', text: '#22c55e' },
    warning: { bg: 'rgba(251, 146, 60, 0.1)', border: 'rgba(251, 146, 60, 0.3)', text: '#fb923c' },
    error: { bg: 'rgba(239, 68, 68, 0.1)', border: 'rgba(239, 68, 68, 0.3)', text: '#ef4444' },
    info: { bg: 'rgba(99, 102, 241, 0.1)', border: 'rgba(99, 102, 241, 0.3)', text: '#6366f1' },
  };

  const color = colors[variant];

  return (
    <Box
      component="span"
      sx={{
        display: 'inline-flex',
        px: 2,
        py: 0.5,
        borderRadius: 1.5,
        background: color.bg,
        border: `1px solid ${color.border}`,
        color: color.text,
        fontSize: '0.875rem',
        fontWeight: 600,
      }}
    >
      {children}
    </Box>
  );
};

// Flight Card
interface FlightCardProps {
  airline: string;
  price: number;
  departure: string;
  arrival: string;
  duration: string;
  onClick?: () => void;
}

export const FlightCard: React.FC<FlightCardProps> = ({
  airline,
  price,
  departure,
  arrival,
  duration,
  onClick,
}) => (
  <GlassCard sx={{ cursor: onClick ? 'pointer' : 'default' }} onClick={onClick}>
    <CardContent sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
        <Box>
          <Typography variant="h6" sx={{ fontWeight: 700, mb: 0.5 }}>
            {airline}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {duration}
          </Typography>
        </Box>
        <Typography
          variant="h5"
          sx={{
            fontWeight: 800,
            background: 'linear-gradient(135deg, #6366f1 0%, #ec4899 100%)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}
        >
          ₹{price.toLocaleString()}
        </Typography>
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="body1" sx={{ fontWeight: 600 }}>
          {departure}
        </Typography>
        <Box
          sx={{
            flex: 1,
            height: 2,
            mx: 2,
            background: 'linear-gradient(90deg, rgba(99, 102, 241, 0.5) 0%, rgba(236, 72, 153, 0.5) 100%)',
            position: 'relative',
            '&::after': {
              content: '""',
              position: 'absolute',
              right: -5,
              top: '50%',
              transform: 'translateY(-50%)',
              width: 0,
              height: 0,
              borderLeft: '5px solid #ec4899',
              borderTop: '3px solid transparent',
              borderBottom: '3px solid transparent',
            },
          }}
        />
        <Typography variant="body1" sx={{ fontWeight: 600 }}>
          {arrival}
        </Typography>
      </Box>
    </CardContent>
  </GlassCard>
);
