from abc import ABC, abstractmethod
from typing import List, Optional
from ..notification import Notification, NotificationType, NotificationChannel

class INotificationRepository(ABC):
    """
    Interface for Notification Repository
    """
    
    @abstractmethod
    def add(self, notification: Notification) -> Notification:
        """Add a new notification"""
        pass
    
    @abstractmethod
    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """Get notification by ID"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[Notification]:
        """Get all notifications for a user"""
        pass
    
    @abstractmethod
    def get_unread_by_user_id(self, user_id: int) -> List[Notification]:
        """Get unread notifications for a user"""
        pass
    
    @abstractmethod
    def get_by_type(self, notification_type: NotificationType) -> List[Notification]:
        """Get notifications by type"""
        pass
    
    @abstractmethod
    def get_by_channel(self, channel: NotificationChannel) -> List[Notification]:
        """Get notifications by channel"""
        pass
    
    @abstractmethod
    def update(self, notification: Notification) -> Notification:
        """Update notification"""
        pass
    
    @abstractmethod
    def delete(self, notification_id: int) -> bool:
        """Delete notification"""
        pass
    
    @abstractmethod
    def mark_all_read_for_user(self, user_id: int) -> bool:
        """Mark all notifications as read for a user"""
        pass
