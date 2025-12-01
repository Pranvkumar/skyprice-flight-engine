from fastapi import WebSocket
from typing import List
import json
import asyncio
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time price updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.subscriptions: dict = {}  # {websocket: [routes]}
        
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]
        logger.info(f"WebSocket disconnected. Remaining: {len(self.active_connections)}")
        
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific client"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
            
    async def broadcast(self, message: str):
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
            
    async def broadcast_price_update(self, route: str, price_data: dict):
        """
        Broadcast price update to subscribed clients
        
        Args:
            route: Flight route (e.g., "BOM-DEL")
            price_data: Dictionary with price information
        """
        message = json.dumps({
            "type": "price_update",
            "route": route,
            "data": price_data,
            "timestamp": str(datetime.utcnow())
        })
        
        # Send to all subscribed clients
        for websocket, routes in self.subscriptions.items():
            if route in routes or "all" in routes:
                try:
                    await websocket.send_text(message)
                except Exception as e:
                    logger.error(f"Error sending price update: {e}")
                    
    async def subscribe_route(self, websocket: WebSocket, route: str):
        """Subscribe client to route updates"""
        if websocket not in self.subscriptions:
            self.subscriptions[websocket] = []
        if route not in self.subscriptions[websocket]:
            self.subscriptions[websocket].append(route)
            logger.info(f"Client subscribed to route: {route}")
            
    async def unsubscribe_route(self, websocket: WebSocket, route: str):
        """Unsubscribe client from route updates"""
        if websocket in self.subscriptions and route in self.subscriptions[websocket]:
            self.subscriptions[websocket].remove(route)
            logger.info(f"Client unsubscribed from route: {route}")


# Global manager instance
manager = ConnectionManager()
