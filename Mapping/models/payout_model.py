from sqlalchemy import Column, Integer, String, DateTime, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class PayoutModel(Base):
    __tablename__ = 'payouts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tutor_id = Column(Integer, ForeignKey('tutor_profiles.user_id'), nullable=False)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Enum('Pending', 'Processing', 'Paid', 'Failed', name='payout_status'),
                    default='Pending', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tutor = relationship("TutorProfileModel", back_populates="payouts")
    booking = relationship("BookingModel", back_populates="payouts")
    
    def __repr__(self):
        return f"<PayoutModel(id={self.id}, tutor_id={self.tutor_id}, status='{self.status}')>"
