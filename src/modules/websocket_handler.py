"""
WebSocket Handler Module
Provides real-time communication for live updates and notifications
"""

import json
import logging
from typing import Dict, Set, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from .utils import LoggingUtils

# Configure logging
logger = LoggingUtils.setup_logger(__name__)


@dataclass
class WebSocketMessage:
    """Structure for WebSocket messages"""
    type: str
    data: Any
    timestamp: str
    source: str = "server"
    
    def to_dict(self) -> dict:
        return asdict(self)


class WebSocketManager:
    """Manages WebSocket connections and message broadcasting"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set] = {}  # room_id -> set of connections
        self.user_connections: Dict[str, str] = {}  # connection_id -> user_id
        self.connection_rooms: Dict[str, Set[str]] = {}  # connection_id -> set of room_ids
        self.message_history: Dict[str, list] = {}  # room_id -> message history
        self.max_history = 100  # Max messages to keep per room
    
    def connect(self, connection_id: str, user_id: str = None):
        """Register a new connection"""
        logger.info(f"New connection: {connection_id} for user: {user_id}")
        self.connection_rooms[connection_id] = set()
        if user_id:
            self.user_connections[connection_id] = user_id
    
    def disconnect(self, connection_id: str):
        """Remove a connection"""
        logger.info(f"Disconnecting: {connection_id}")
        
        # Remove from all rooms
        if connection_id in self.connection_rooms:
            for room_id in self.connection_rooms[connection_id]:
                if room_id in self.active_connections:
                    self.active_connections[room_id].discard(connection_id)
            
            del self.connection_rooms[connection_id]
        
        # Remove user mapping
        if connection_id in self.user_connections:
            del self.user_connections[connection_id]
    
    def join_room(self, connection_id: str, room_id: str):
        """Add connection to a room"""
        logger.debug(f"Connection {connection_id} joining room {room_id}")
        
        if connection_id not in self.connection_rooms:
            self.connection_rooms[connection_id] = set()
        
        self.connection_rooms[connection_id].add(room_id)
        
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        
        self.active_connections[room_id].add(connection_id)
        
        # Initialize message history for room
        if room_id not in self.message_history:
            self.message_history[room_id] = []
    
    def leave_room(self, connection_id: str, room_id: str):
        """Remove connection from a room"""
        logger.debug(f"Connection {connection_id} leaving room {room_id}")
        
        if connection_id in self.connection_rooms:
            self.connection_rooms[connection_id].discard(room_id)
        
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(connection_id)
    
    def send_message(self, connection_id: str, message: WebSocketMessage):
        """Send message to specific connection"""
        # This would be implemented by the actual WebSocket library
        # For now, we'll just log it
        logger.debug(f"Sending to {connection_id}: {message.type}")
    
    def broadcast_to_room(self, room_id: str, message: WebSocketMessage):
        """Broadcast message to all connections in a room"""
        if room_id not in self.active_connections:
            logger.warning(f"Room {room_id} has no active connections")
            return
        
        connections = self.active_connections[room_id]
        logger.info(f"Broadcasting to room {room_id}: {len(connections)} connections")
        
        # Add to message history
        if room_id in self.message_history:
            self.message_history[room_id].append(message.to_dict())
            # Trim history if needed
            if len(self.message_history[room_id]) > self.max_history:
                self.message_history[room_id] = self.message_history[room_id][-self.max_history:]
        
        # Send to all connections (would be implemented by WebSocket library)
        for connection_id in connections:
            self.send_message(connection_id, message)
    
    def broadcast_to_user(self, user_id: str, message: WebSocketMessage):
        """Broadcast message to all connections for a specific user"""
        user_connections = [
            conn_id for conn_id, uid in self.user_connections.items() 
            if uid == user_id
        ]
        
        logger.info(f"Broadcasting to user {user_id}: {len(user_connections)} connections")
        
        for connection_id in user_connections:
            self.send_message(connection_id, message)
    
    def get_room_connections(self, room_id: str) -> Set[str]:
        """Get all connection IDs in a room"""
        return self.active_connections.get(room_id, set())
    
    def get_room_history(self, room_id: str, limit: int = 50) -> list:
        """Get message history for a room"""
        history = self.message_history.get(room_id, [])
        return history[-limit:] if history else []
    
    def get_connection_rooms(self, connection_id: str) -> Set[str]:
        """Get all rooms a connection is in"""
        return self.connection_rooms.get(connection_id, set())
    
    def get_stats(self) -> dict:
        """Get WebSocket manager statistics"""
        return {
            'total_connections': len(self.connection_rooms),
            'total_rooms': len(self.active_connections),
            'total_users': len(set(self.user_connections.values())),
            'connections_by_room': {
                room_id: len(connections) 
                for room_id, connections in self.active_connections.items()
            }
        }


class NotificationManager:
    """Manages real-time notifications"""
    
    def __init__(self, ws_manager: WebSocketManager):
        self.ws_manager = ws_manager
        self.notification_channels = {
            'financial': 'financial_updates',
            'souls': 'soul_updates',
            'analytics': 'analytics_updates',
            'system': 'system_notifications'
        }
    
    def send_financial_update(self, data: dict):
        """Send financial update notification"""
        message = WebSocketMessage(
            type='financial_update',
            data=data,
            timestamp=datetime.now().isoformat(),
            source='financial_system'
        )
        room = self.notification_channels['financial']
        self.ws_manager.broadcast_to_room(room, message)
    
    def send_soul_update(self, soul_id: str, data: dict):
        """Send soul update notification"""
        message = WebSocketMessage(
            type='soul_update',
            data={'soul_id': soul_id, 'update': data},
            timestamp=datetime.now().isoformat(),
            source='souls_manager'
        )
        room = self.notification_channels['souls']
        self.ws_manager.broadcast_to_room(room, message)
    
    def send_analytics_update(self, data: dict):
        """Send analytics update notification"""
        message = WebSocketMessage(
            type='analytics_update',
            data=data,
            timestamp=datetime.now().isoformat(),
            source='analytics_system'
        )
        room = self.notification_channels['analytics']
        self.ws_manager.broadcast_to_room(room, message)
    
    def send_system_notification(self, notification: dict):
        """Send system notification"""
        message = WebSocketMessage(
            type='system_notification',
            data=notification,
            timestamp=datetime.now().isoformat(),
            source='system'
        )
        room = self.notification_channels['system']
        self.ws_manager.broadcast_to_room(room, message)
    
    def send_user_notification(self, user_id: str, notification: dict):
        """Send notification to specific user"""
        message = WebSocketMessage(
            type='user_notification',
            data=notification,
            timestamp=datetime.now().isoformat(),
            source='system'
        )
        self.ws_manager.broadcast_to_user(user_id, message)


# Global WebSocket manager instance
ws_manager = WebSocketManager()
notification_manager = NotificationManager(ws_manager)


def get_websocket_manager() -> WebSocketManager:
    """Get the global WebSocket manager instance"""
    return ws_manager


def get_notification_manager() -> NotificationManager:
    """Get the global notification manager instance"""
    return notification_manager
