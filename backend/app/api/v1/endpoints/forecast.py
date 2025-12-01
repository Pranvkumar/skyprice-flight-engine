from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.schemas.schemas import (
    PricePredictionRequest,
    PricePredictionResponse,
    OptimalPriceRecommendation
)
from app.services.forecasting.price_predictor import PricePredictor
from app.services.forecasting.optimizer import PriceOptimizer

router = APIRouter()


@router.post("/predict", response_model=PricePredictionResponse)
async def predict_price(
    request: PricePredictionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Predict flight prices using divide-and-conquer forecasting
    
    This endpoint implements the core DAA project algorithm:
    1. Segments historical data by route, airline, seasonality
    2. Applies multiple forecasting models to each segment
    3. Merges segment predictions into global forecast
    4. Provides optimal booking recommendations
    """
    predictor = PricePredictor(db)
    
    try:
        prediction = await predictor.predict_price(
            origin=request.origin,
            destination=request.destination,
            departure_date=request.departure_date,
            airline=request.airline,
            cabin_class=request.cabin_class,
            horizon_days=request.days_ahead
        )
        
        return prediction
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/batch")
async def batch_predict(
    requests: List[PricePredictionRequest],
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Batch price predictions for multiple routes
    Uses parallel processing for efficiency
    """
    predictor = PricePredictor(db)
    
    results = []
    for req in requests:
        try:
            prediction = await predictor.predict_price(
                origin=req.origin,
                destination=req.destination,
                departure_date=req.departure_date,
                airline=req.airline,
                cabin_class=req.cabin_class,
                horizon_days=req.days_ahead
            )
            results.append({"status": "success", "prediction": prediction})
        except Exception as e:
            results.append({"status": "error", "error": str(e)})
    
    return {"results": results, "total": len(requests), "successful": sum(1 for r in results if r["status"] == "success")}


@router.get("/routes/{route}")
async def get_route_forecast(
    route: str,
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """
    Get price forecast for a specific route
    Route format: ORIGIN-DESTINATION (e.g., BOM-DEL)
    """
    try:
        origin, destination = route.split('-')
    except:
        raise HTTPException(status_code=400, detail="Invalid route format. Use ORIGIN-DESTINATION")
    
    predictor = PricePredictor(db)
    
    forecast = await predictor.get_route_forecast(
        origin=origin,
        destination=destination,
        horizon_days=days
    )
    
    return forecast


@router.post("/optimize", response_model=OptimalPriceRecommendation)
async def optimize_price(
    flight_id: int,
    objective: str = "revenue",  # revenue, conversion, profit
    db: AsyncSession = Depends(get_db)
):
    """
    Get optimal price recommendation for a flight
    
    Uses price optimization algorithms considering:
    - Demand elasticity
    - Competitor pricing
    - Historical performance
    - Current occupancy
    """
    optimizer = PriceOptimizer(db)
    
    recommendation = await optimizer.optimize_flight_price(
        flight_id=flight_id,
        objective=objective
    )
    
    return recommendation


@router.get("/confidence/{flight_id}")
async def get_prediction_confidence(
    flight_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get confidence metrics for price predictions
    """
    predictor = PricePredictor(db)
    
    confidence_metrics = await predictor.get_confidence_metrics(flight_id)
    
    return confidence_metrics
