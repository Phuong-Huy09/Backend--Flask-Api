from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class SubjectModel(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    level = Column(Enum('K12', 'Undergrad', 'Graduate', 'Other', name='subject_level'), 
                   nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tutor_subjects = relationship("TutorSubjectModel", back_populates="subject")
    bookings = relationship("BookingModel", back_populates="subject")
    
    def __repr__(self):
        return f"<SubjectModel(id={self.id}, name='{self.name}', level='{self.level}')>"
