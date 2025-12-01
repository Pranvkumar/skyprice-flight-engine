"""
Price Alerts API Endpoints
Create, manage, and trigger price alerts
"""

from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from pydantic import BaseModel, EmailStr

from app.services.alerts.price_alerts import get_alert_service, PriceAlert

router = APIRouter()


class CreateAlertRequest(BaseModel):
    user_email: EmailStr
    origin: str
    destination: str
    target_price: float
    departure_date: str
    cabin_class: str = "ECONOMY"


class AlertResponse(BaseModel):
    success: bool
    alert: PriceAlert
    message: str


@router.post("/create", response_model=AlertResponse)
async def create_price_alert(request: CreateAlertRequest):
    """
    Create a new price alert
    
    **User will be notified when price drops to or below target**
    """
    service = get_alert_service()
    
    try:
        alert = service.create_alert(
            user_email=request.user_email,
            origin=request.origin,
            destination=request.destination,
            target_price=request.target_price,
            departure_date=request.departure_date,
            cabin_class=request.cabin_class
        )
        
        return {
            "success": True,
            "alert": alert,
            "message": f"Price alert created! You'll be notified when {request.origin}-{request.destination} drops to ${request.target_price}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user/{email}")
async def get_user_alerts(email: str):
    """
    Get all alerts for a user
    """
    service = get_alert_service()
    
    try:
        alerts = service.get_user_alerts(email)
        
        return {
            "success": True,
            "email": email,
            "alerts": alerts,
            "count": len(alerts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alert/{alert_id}")
async def get_alert(alert_id: str):
    """
    Get specific alert by ID
    """
    service = get_alert_service()
    alert = service.get_alert(alert_id)
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    return {
        "success": True,
        "alert": alert
    }


@router.delete("/alert/{alert_id}")
async def delete_alert(alert_id: str):
    """
    Delete a price alert
    """
    service = get_alert_service()
    
    if service.delete_alert(alert_id):
        return {
            "success": True,
            "message": f"Alert {alert_id} deleted"
        }
    
    raise HTTPException(status_code=404, detail="Alert not found")


@router.post("/alert/{alert_id}/deactivate")
async def deactivate_alert(alert_id: str):
    """
    Deactivate an alert (don't delete, just stop monitoring)
    """
    service = get_alert_service()
    
    if service.deactivate_alert(alert_id):
        return {
            "success": True,
            "message": f"Alert {alert_id} deactivated"
        }
    
    raise HTTPException(status_code=404, detail="Alert not found")


@router.get("/active")
async def get_active_alerts():
    """
    Get all active alerts (admin endpoint)
    """
    service = get_alert_service()
    alerts = service.get_active_alerts()
    
    return {
        "success": True,
        "alerts": alerts,
        "count": len(alerts)
    }


@router.post("/check/{alert_id}")
async def check_alert_manually(
    alert_id: str,
    current_price: float = Body(..., embed=True)
):
    """
    Manually check if alert should trigger (for testing)
    """
    service = get_alert_service()
    alert = service.get_alert(alert_id)
    
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    should_trigger = await service.check_alert(alert, current_price)
    
    if should_trigger:
        notification = await service.send_alert_notification(alert, current_price)
        return {
            "success": True,
            "triggered": True,
            "message": "Alert triggered! Notification sent.",
            "notification": notification
        }
    
    return {
        "success": True,
        "triggered": False,
        "message": f"Current price ${current_price} is above target ${alert.target_price}"
    }
