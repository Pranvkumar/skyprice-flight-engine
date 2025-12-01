"""
Price Alerts System
Allows users to set price alerts and get notifications
"""

from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
import logging

logger = logging.getLogger(__name__)


class PriceAlert(BaseModel):
    """Price alert configuration"""
    id: Optional[str] = None
    user_email: EmailStr
    origin: str
    destination: str
    target_price: float
    departure_date: str
    cabin_class: str = "ECONOMY"
    active: bool = True
    created_at: Optional[datetime] = None
    triggered_at: Optional[datetime] = None


class PriceAlertService:
    """
    Service to manage price alerts
    In production, this would use a database and background jobs
    """
    
    def __init__(self):
        # In-memory storage for demo (use database in production)
        self.alerts: Dict[str, PriceAlert] = {}
        self._alert_counter = 0
    
    def create_alert(
        self,
        user_email: str,
        origin: str,
        destination: str,
        target_price: float,
        departure_date: str,
        cabin_class: str = "ECONOMY"
    ) -> PriceAlert:
        """
        Create a new price alert
        
        Args:
            user_email: User's email for notifications
            origin: Origin airport IATA code
            destination: Destination airport IATA code
            target_price: Target price to trigger alert
            departure_date: Departure date
            cabin_class: Cabin class preference
            
        Returns:
            Created price alert
        """
        self._alert_counter += 1
        alert_id = f"alert_{self._alert_counter}"
        
        alert = PriceAlert(
            id=alert_id,
            user_email=user_email,
            origin=origin,
            destination=destination,
            target_price=target_price,
            departure_date=departure_date,
            cabin_class=cabin_class,
            active=True,
            created_at=datetime.utcnow()
        )
        
        self.alerts[alert_id] = alert
        logger.info(f"Created price alert {alert_id} for {origin}-{destination} at {target_price}")
        
        return alert
    
    def get_alert(self, alert_id: str) -> Optional[PriceAlert]:
        """Get alert by ID"""
        return self.alerts.get(alert_id)
    
    def get_user_alerts(self, user_email: str) -> List[PriceAlert]:
        """Get all alerts for a user"""
        return [
            alert for alert in self.alerts.values()
            if alert.user_email == user_email
        ]
    
    def get_active_alerts(self) -> List[PriceAlert]:
        """Get all active alerts"""
        return [
            alert for alert in self.alerts.values()
            if alert.active
        ]
    
    def deactivate_alert(self, alert_id: str) -> bool:
        """Deactivate an alert"""
        if alert_id in self.alerts:
            self.alerts[alert_id].active = False
            logger.info(f"Deactivated alert {alert_id}")
            return True
        return False
    
    def delete_alert(self, alert_id: str) -> bool:
        """Delete an alert"""
        if alert_id in self.alerts:
            del self.alerts[alert_id]
            logger.info(f"Deleted alert {alert_id}")
            return True
        return False
    
    async def check_alert(self, alert: PriceAlert, current_price: float) -> bool:
        """
        Check if alert should be triggered
        
        Args:
            alert: Price alert to check
            current_price: Current flight price
            
        Returns:
            True if alert should trigger
        """
        if not alert.active:
            return False
        
        if current_price <= alert.target_price:
            alert.triggered_at = datetime.utcnow()
            alert.active = False
            logger.info(f"Alert {alert.id} triggered: price {current_price} <= target {alert.target_price}")
            return True
        
        return False
    
    async def send_alert_notification(self, alert: PriceAlert, current_price: float):
        """
        Send notification to user (email/push)
        
        In production, this would:
        - Send email via SendGrid/AWS SES
        - Send push notification via Firebase
        - Store in notification database
        """
        logger.info(
            f"ALERT: {alert.user_email} - Flight {alert.origin}-{alert.destination} "
            f"on {alert.departure_date} is now {current_price} (target: {alert.target_price})"
        )
        
        # TODO: Implement actual email/push notification
        # For now, just log it
        return {
            "notification_sent": True,
            "user_email": alert.user_email,
            "message": f"Price alert! Flight {alert.origin}-{alert.destination} is now ${current_price}",
            "current_price": current_price,
            "target_price": alert.target_price,
            "savings": alert.target_price - current_price
        }


# Singleton instance
_alert_service = None

def get_alert_service() -> PriceAlertService:
    """Get or create alert service singleton"""
    global _alert_service
    if _alert_service is None:
        _alert_service = PriceAlertService()
    return _alert_service
