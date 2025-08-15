from sqlalchemy import Column, Integer, String, DateTime, Text, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class ServiceListingModel(Base):
    __tablename__ = 'service_listings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tutor_id = Column(Integer, ForeignKey('tutor_profiles.user_id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    price_per_hour = Column(DECIMAL(10, 2), nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tutor = relationship("TutorProfileModel", back_populates="service_listings")
    bookings = relationship("BookingModel", back_populates="service")
    
    def __repr__(self):
        return f"<ServiceListingModel(id={self.id}, title='{self.title}', tutor_id={self.tutor_id})>"
