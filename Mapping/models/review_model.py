from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class ReviewModel(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('student_profiles.user_id'), nullable=False)
    tutor_id = Column(Integer, ForeignKey('tutor_profiles.user_id'), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 scale
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    booking = relationship("BookingModel", back_populates="review")
    student = relationship("StudentProfileModel", back_populates="reviews")
    tutor = relationship("TutorProfileModel", back_populates="reviews")
    
    def __repr__(self):
        return f"<ReviewModel(id={self.id}, rating={self.rating}, booking_id={self.booking_id})>"
