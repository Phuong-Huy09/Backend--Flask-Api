from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class NotificationModel(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(Enum('OTP', 'BookingUpdate', 'Payment', 'Message', 'System', name='notification_type'),
                  nullable=False)
    channel = Column(Enum('Email', 'SMS', 'Push', 'InApp', name='notification_channel'),
                     nullable=False)
    payload = Column(Text, nullable=False)  # JSON stored as text
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("UserModel", back_populates="notifications")
    
    def __repr__(self):
        return f"<NotificationModel(id={self.id}, user_id={self.user_id}, type='{self.type}')>"
