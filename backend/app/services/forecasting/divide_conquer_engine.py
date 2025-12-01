"""
Divide-and-Conquer Forecasting Engine
Core implementation of the segmentation and forecasting strategy
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class DataSegment:
    """Represents a data segment for divide-and-conquer"""
    segment_id: str
    data: pd.DataFrame
    metadata: Dict
    segment_type: str  # 'route', 'temporal', 'airline', 'demand_pattern'


class DataSegmenter:
    """
    Divides large datasets into manageable segments
    Implements the 'Divide' phase of divide-and-conquer
    """
    
    def __init__(self, min_segment_size: int = 10):
        self.min_segment_size = min_segment_size
        
    def segment_by_route(self, df: pd.DataFrame) -> List[DataSegment]:
        """Segment data by origin-destination pairs"""
        segments = []
        
        for (origin, dest), group in df.groupby(['origin', 'destination']):
            if len(group) >= self.min_segment_size:
                segment = DataSegment(
                    segment_id=f"route_{origin}_{dest}",
                    data=group.copy(),
                    metadata={
                        'origin': origin,
                        'destination': dest,
                        'size': len(group)
                    },
                    segment_type='route'
                )
                segments.append(segment)
                logger.info(f"Created route segment: {origin}-{dest} with {len(group)} records")
        
        return segments
    
    def segment_by_temporal(self, df: pd.DataFrame, freq: str = 'M') -> List[DataSegment]:
        """
        Segment data by time periods
        freq: 'D' (daily), 'W' (weekly), 'M' (monthly)
        """
        segments = []
        df['period'] = pd.to_datetime(df['date']).dt.to_period(freq)
        
        for period, group in df.groupby('period'):
            if len(group) >= self.min_segment_size:
                segment = DataSegment(
                    segment_id=f"temporal_{period}",
                    data=group.copy(),
                    metadata={
                        'period': str(period),
                        'size': len(group),
                        'date_range': (group['date'].min(), group['date'].max())
                    },
                    segment_type='temporal'
                )
                segments.append(segment)
        
        return segments
    
    def segment_by_airline(self, df: pd.DataFrame) -> List[DataSegment]:
        """Segment data by airline"""
        segments = []
        
        for airline, group in df.groupby('airline'):
            if len(group) >= self.min_segment_size:
                segment = DataSegment(
                    segment_id=f"airline_{airline}",
                    data=group.copy(),
                    metadata={
                        'airline': airline,
                        'size': len(group)
                    },
                    segment_type='airline'
                )
                segments.append(segment)
        
        return segments
    
    def segment_by_demand_pattern(self, df: pd.DataFrame) -> List[DataSegment]:
        """
        Segment by demand patterns using clustering
        Groups flights with similar booking patterns
        """
        from sklearn.cluster import KMeans
        
        # Extract demand features
        features = df[['days_to_departure', 'occupancy_rate', 'price']].values
        
        # Determine optimal clusters (3-5 typical demand patterns)
        n_clusters = min(5, len(df) // self.min_segment_size)
        if n_clusters < 2:
            return []
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['demand_cluster'] = kmeans.fit_predict(features)
        
        segments = []
        for cluster_id, group in df.groupby('demand_cluster'):
            if len(group) >= self.min_segment_size:
                segment = DataSegment(
                    segment_id=f"demand_{cluster_id}",
                    data=group.copy(),
                    metadata={
                        'cluster_id': int(cluster_id),
                        'size': len(group),
                        'avg_occupancy': float(group['occupancy_rate'].mean())
                    },
                    segment_type='demand_pattern'
                )
                segments.append(segment)
        
        return segments
    
    def hierarchical_segmentation(self, df: pd.DataFrame) -> List[DataSegment]:
        """
        Multi-level segmentation: First by route, then by temporal patterns
        Creates finer-grained segments for better forecasting
        """
        all_segments = []
        
        # Level 1: Route-based segmentation
        route_segments = self.segment_by_route(df)
        
        # Level 2: Further segment each route by time
        for route_segment in route_segments:
            temporal_segments = self.segment_by_temporal(
                route_segment.data, 
                freq='W'  # Weekly granularity
            )
            
            # Update segment IDs to reflect hierarchy
            for temp_seg in temporal_segments:
                temp_seg.segment_id = f"{route_segment.segment_id}_{temp_seg.segment_id}"
                temp_seg.metadata.update(route_segment.metadata)
                all_segments.append(temp_seg)
        
        logger.info(f"Hierarchical segmentation created {len(all_segments)} segments")
        return all_segments


class SegmentForecaster:
    """
    Forecasts prices for individual segments
    Implements the 'Conquer' phase
    """
    
    def __init__(self):
        self.models = {}
        
    def forecast_arima(self, segment: DataSegment, horizon: int) -> np.ndarray:
        """ARIMA forecasting for time series"""
        from statsmodels.tsa.arima.model import ARIMA
        
        try:
            prices = segment.data['price'].values
            model = ARIMA(prices, order=(1, 1, 1))
            fitted = model.fit()
            forecast = fitted.forecast(steps=horizon)
            return forecast
        except Exception as e:
            logger.warning(f"ARIMA failed for {segment.segment_id}: {e}")
            # Fallback to moving average
            return self.forecast_moving_average(segment, horizon)
    
    def forecast_moving_average(self, segment: DataSegment, horizon: int, window: int = 7) -> np.ndarray:
        """Simple moving average forecast"""
        prices = segment.data['price'].values
        ma = np.convolve(prices, np.ones(window)/window, mode='valid')
        last_ma = ma[-1] if len(ma) > 0 else np.mean(prices)
        return np.full(horizon, last_ma)
    
    def forecast_exponential_smoothing(self, segment: DataSegment, horizon: int) -> np.ndarray:
        """Exponential smoothing forecast"""
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        
        try:
            prices = segment.data['price'].values
            model = ExponentialSmoothing(prices, seasonal_periods=7, trend='add', seasonal='add')
            fitted = model.fit()
            forecast = fitted.forecast(steps=horizon)
            return forecast
        except Exception as e:
            logger.warning(f"Exponential smoothing failed: {e}")
            return self.forecast_moving_average(segment, horizon)
    
    def forecast_regression(self, segment: DataSegment, horizon: int, features: List[str]) -> np.ndarray:
        """Regression-based forecast using external features"""
        from sklearn.linear_model import LinearRegression
        
        X = segment.data[features].values
        y = segment.data['price'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate future feature values (simplified - would be more complex in production)
        future_X = np.tile(X[-1], (horizon, 1))
        forecast = model.predict(future_X)
        
        return forecast
    
    def ensemble_forecast(self, segment: DataSegment, horizon: int) -> Tuple[np.ndarray, float]:
        """
        Ensemble of multiple forecasting methods
        Returns: (forecast, confidence)
        """
        forecasts = []
        weights = []
        
        # Try ARIMA
        try:
            arima_forecast = self.forecast_arima(segment, horizon)
            forecasts.append(arima_forecast)
            weights.append(0.4)
        except:
            pass
        
        # Try Exponential Smoothing
        try:
            es_forecast = self.forecast_exponential_smoothing(segment, horizon)
            forecasts.append(es_forecast)
            weights.append(0.3)
        except:
            pass
        
        # Moving Average (always available)
        ma_forecast = self.forecast_moving_average(segment, horizon)
        forecasts.append(ma_forecast)
        weights.append(0.3)
        
        # Weighted average
        weights = np.array(weights) / sum(weights)
        ensemble = np.average(forecasts, axis=0, weights=weights)
        
        # Confidence based on forecast agreement
        if len(forecasts) > 1:
            std = np.std(forecasts, axis=0).mean()
            mean = np.mean(ensemble)
            confidence = max(0, 1 - (std / mean)) if mean > 0 else 0.5
        else:
            confidence = 0.6  # Lower confidence for single model
        
        return ensemble, confidence


class ForecastMerger:
    """
    Combines forecasts from multiple segments
    Implements the 'Combine' phase
    """
    
    def __init__(self):
        self.merge_strategies = {
            'weighted_average': self._weighted_average,
            'confidence_based': self._confidence_based,
            'hierarchical': self._hierarchical_merge
        }
    
    def merge(self, segment_forecasts: List[Dict], strategy: str = 'confidence_based') -> Dict:
        """
        Merge multiple segment forecasts into global forecast
        
        Args:
            segment_forecasts: List of dicts with keys: segment_id, forecast, confidence, metadata
            strategy: Merging strategy to use
        """
        if strategy not in self.merge_strategies:
            raise ValueError(f"Unknown merge strategy: {strategy}")
        
        return self.merge_strategies[strategy](segment_forecasts)
    
    def _weighted_average(self, segment_forecasts: List[Dict]) -> Dict:
        """Simple weighted average based on segment size"""
        total_weight = sum(sf['metadata'].get('size', 1) for sf in segment_forecasts)
        
        forecasts = []
        weights = []
        
        for sf in segment_forecasts:
            forecasts.append(sf['forecast'])
            weight = sf['metadata'].get('size', 1) / total_weight
            weights.append(weight)
        
        merged_forecast = np.average(forecasts, axis=0, weights=weights)
        avg_confidence = np.average([sf['confidence'] for sf in segment_forecasts], weights=weights)
        
        return {
            'forecast': merged_forecast,
            'confidence': float(avg_confidence),
            'num_segments': len(segment_forecasts),
            'strategy': 'weighted_average'
        }
    
    def _confidence_based(self, segment_forecasts: List[Dict]) -> Dict:
        """Merge based on forecast confidence scores"""
        confidences = np.array([sf['confidence'] for sf in segment_forecasts])
        weights = confidences / confidences.sum()
        
        forecasts = [sf['forecast'] for sf in segment_forecasts]
        merged_forecast = np.average(forecasts, axis=0, weights=weights)
        
        return {
            'forecast': merged_forecast,
            'confidence': float(np.max(confidences)),
            'num_segments': len(segment_forecasts),
            'strategy': 'confidence_based',
            'segment_contributions': weights.tolist()
        }
    
    def _hierarchical_merge(self, segment_forecasts: List[Dict]) -> Dict:
        """Hierarchical merge preserving segment structure"""
        # Group by segment hierarchy
        hierarchy = {}
        for sf in segment_forecasts:
            parts = sf['segment_id'].split('_')
            key = '_'.join(parts[:2])  # Group by first two levels
            
            if key not in hierarchy:
                hierarchy[key] = []
            hierarchy[key].append(sf)
        
        # Merge within each group first
        group_forecasts = []
        for group_name, group_segments in hierarchy.items():
            group_result = self._confidence_based(group_segments)
            group_forecasts.append(group_result)
        
        # Then merge across groups
        final_forecasts = [gf['forecast'] for gf in group_forecasts]
        final_confidences = [gf['confidence'] for gf in group_forecasts]
        
        weights = np.array(final_confidences) / sum(final_confidences)
        merged_forecast = np.average(final_forecasts, axis=0, weights=weights)
        
        return {
            'forecast': merged_forecast,
            'confidence': float(np.mean(final_confidences)),
            'num_segments': len(segment_forecasts),
            'num_groups': len(hierarchy),
            'strategy': 'hierarchical'
        }


class DivideAndConquerForecaster:
    """
    Main orchestrator for divide-and-conquer forecasting
    """
    
    def __init__(self, min_segment_size: int = 10):
        self.segmenter = DataSegmenter(min_segment_size)
        self.forecaster = SegmentForecaster()
        self.merger = ForecastMerger()
        
    def predict(self, df: pd.DataFrame, horizon: int, segmentation_strategy: str = 'route') -> Dict:
        """
        Complete divide-and-conquer forecasting pipeline
        
        Args:
            df: Historical data DataFrame
            horizon: Forecast horizon (number of steps)
            segmentation_strategy: 'route', 'temporal', 'hierarchical', 'demand_pattern'
        
        Returns:
            Dictionary with forecast, confidence, and metadata
        """
        logger.info(f"Starting divide-and-conquer forecast with {len(df)} records")
        
        # Phase 1: DIVIDE - Segment the data
        if segmentation_strategy == 'route':
            segments = self.segmenter.segment_by_route(df)
        elif segmentation_strategy == 'temporal':
            segments = self.segmenter.segment_by_temporal(df)
        elif segmentation_strategy == 'hierarchical':
            segments = self.segmenter.hierarchical_segmentation(df)
        elif segmentation_strategy == 'demand_pattern':
            segments = self.segmenter.segment_by_demand_pattern(df)
        else:
            raise ValueError(f"Unknown segmentation strategy: {segmentation_strategy}")
        
        logger.info(f"Created {len(segments)} segments")
        
        if not segments:
            logger.warning("No segments created, using global forecast")
            forecast, confidence = self.forecaster.ensemble_forecast(
                DataSegment('global', df, {}, 'global'), 
                horizon
            )
            return {
                'forecast': forecast.tolist(),
                'confidence': confidence,
                'strategy': 'global',
                'num_segments': 0
            }
        
        # Phase 2: CONQUER - Forecast each segment independently
        segment_forecasts = []
        for segment in segments:
            try:
                forecast, confidence = self.forecaster.ensemble_forecast(segment, horizon)
                segment_forecasts.append({
                    'segment_id': segment.segment_id,
                    'forecast': forecast,
                    'confidence': confidence,
                    'metadata': segment.metadata
                })
            except Exception as e:
                logger.error(f"Forecast failed for segment {segment.segment_id}: {e}")
        
        logger.info(f"Successfully forecasted {len(segment_forecasts)} segments")
        
        # Phase 3: COMBINE - Merge segment forecasts
        merged_result = self.merger.merge(segment_forecasts, strategy='confidence_based')
        merged_result['segmentation_strategy'] = segmentation_strategy
        merged_result['forecast'] = merged_result['forecast'].tolist()
        
        logger.info(f"Forecast complete with confidence: {merged_result['confidence']:.2f}")
        
        return merged_result
