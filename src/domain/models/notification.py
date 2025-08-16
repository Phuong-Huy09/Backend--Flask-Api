from typing import Optional
from datetime import datetime
from enum import Enum

class NotificationType(Enum):
    OTP = "OTP"
    BOOKING_UPDATE = "BookingUpdate"
    PAYMENT = "Payment"
    MESSAGE = "Message"
    SYSTEM = "System"

class NotificationChannel(Enum):
    EMAIL = "Email"
    SMS = "SMS"
    PUSH = "Push"
    IN_APP = "InApp"

class Notification:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        type: NotificationType = NotificationType.SYSTEM,
        channel: NotificationChannel = NotificationChannel.IN_APP,
        payload: str = "",
        sent_at: Optional[datetime] = None,
        read_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.type = type
        self.channel = channel
        self.payload = payload
        self.sent_at = sent_at
        self.read_at = read_at
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def mark_sent(self):
        """Mark notification as sent"""
        self.sent_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def mark_read(self):
        """Mark notification as read"""
        self.read_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def is_sent(self) -> bool:
        """Check if notification is sent"""
        return self.sent_at is not None
    
    def is_read(self) -> bool:
        """Check if notification is read"""
        return self.read_at is not None
    
    def is_unread(self) -> bool:
        """Check if notification is unread"""
        return self.sent_at is not None and self.read_at is None
