from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class StudentProfileModel(Base):
    __tablename__ = 'student_profiles'
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    full_name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("UserModel", back_populates="student_profile")
    bookings = relationship("BookingModel", back_populates="student")
    reviews = relationship("ReviewModel", back_populates="student")
    chat_threads = relationship("ChatThreadModel", back_populates="student")
    
    def __repr__(self):
        return f"<StudentProfileModel(user_id={self.user_id}, full_name='{self.full_name}')>"
