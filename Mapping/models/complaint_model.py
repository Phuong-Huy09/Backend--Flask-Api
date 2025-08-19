from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class ComplaintModel(Base):
    __tablename__ = 'complaints'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    raised_by_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    against_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=True)
    type = Column(Enum('Content', 'Behavior', 'Payment', 'Other', name='complaint_type'),
                  nullable=False)
    detail = Column(Text, nullable=False)
    status = Column(Enum('Open', 'UnderReview', 'Resolved', 'Rejected', name='complaint_status'),
                    default='Open', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    raised_by = relationship("UserModel", foreign_keys=[raised_by_user], back_populates="complaints_raised")
    against = relationship("UserModel", foreign_keys=[against_user], back_populates="complaints_against")
    booking = relationship("BookingModel", back_populates="complaints")
    moderation_actions = relationship("ModerationActionModel", back_populates="complaint")
    
    def __repr__(self):
        return f"<ComplaintModel(id={self.id}, type='{self.type}', status='{self.status}')>"
