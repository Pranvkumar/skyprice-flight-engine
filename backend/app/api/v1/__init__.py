from fastapi import APIRouter
from app.api.v1.endpoints import forecast, flights, analytics, travel, realtime, alerts

api_router = APIRouter()

api_router.include_router(forecast.router, prefix="/forecast", tags=["forecasting"])
api_router.include_router(flights.router, prefix="/flights", tags=["flights"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(travel.router, prefix="/travel", tags=["multi-modal travel"])
api_router.include_router(realtime.router, prefix="/realtime", tags=["real-time data"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["price alerts"])

