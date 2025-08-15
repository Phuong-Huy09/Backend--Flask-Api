from sqlalchemy import Column, Integer, String, DateTime, Enum, Time, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class AvailabilitySlotModel(Base):
    __tablename__ = 'availability_slots'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tutor_id = Column(Integer, ForeignKey('tutor_profiles.user_id'), nullable=False)
    weekday = Column(Enum('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', name='weekday'),
                     nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    timezone = Column(String(50), nullable=False, default='UTC')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tutor = relationship("TutorProfileModel", back_populates="availability_slots")
    
    def __repr__(self):
        return f"<AvailabilitySlotModel(id={self.id}, tutor_id={self.tutor_id}, weekday='{self.weekday}')>"
