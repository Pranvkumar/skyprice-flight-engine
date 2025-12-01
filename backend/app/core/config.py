from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # App Configuration
    APP_NAME: str = "Flight Price Recommendation Engine"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://flightuser:flightpass123@localhost:5432/flight_pricing"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CACHE_TTL: int = 300  # 5 minutes
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000"
    ]
    
    # ML Models
    ML_MODEL_PATH: str = "./models"
    MODEL_RETRAIN_INTERVAL_HOURS: int = 24
    FORECASTING_HORIZON_DAYS: int = 90
    
    # Forecasting Parameters
    MIN_HISTORICAL_DATA_POINTS: int = 30
    SEGMENT_MIN_SIZE: int = 10
    CONFIDENCE_THRESHOLD: float = 0.75
    
    # Price Optimization
    MIN_PRICE_MARGIN: float = 0.05  # 5%
    MAX_PRICE_INCREASE: float = 0.30  # 30%
    DEMAND_ELASTICITY_FACTOR: float = 1.2
    
    # API Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_MAX_CONNECTIONS: int = 1000
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Monitoring
    ENABLE_METRICS: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Amadeus API
    AMADEUS_API_KEY: str = ""
    AMADEUS_API_SECRET: str = ""
    AMADEUS_ENVIRONMENT: str = "test"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
