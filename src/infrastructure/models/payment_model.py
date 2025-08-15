from sqlalchemy import Column, Integer, String, DateTime, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class PaymentModel(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    method = Column(Enum('Card', 'Wallet', 'Bank', name='payment_method'), nullable=False)
    provider_txn_id = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default='USD')
    status = Column(Enum('Authorized', 'Captured', 'Failed', 'Refunded', name='payment_status'),
                    nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    booking = relationship("BookingModel", back_populates="payment")
    
    def __repr__(self):
        return f"<PaymentModel(id={self.id}, booking_id={self.booking_id}, status='{self.status}')>"
