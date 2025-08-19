from sqlalchemy import Column, Integer, String, DateTime, Text, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class TutorProfileModel(Base):
    __tablename__ = 'tutor_profiles'
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    full_name = Column(String(255), nullable=False)
    bio = Column(Text, nullable=False)
    years_experience = Column(Integer, default=0, nullable=False)
    hourly_rate = Column(DECIMAL(10, 2), default=0.00, nullable=False)
    verification_status = Column(Enum('Unverified', 'Pending', 'Verified', 'Rejected', 
                                     name='verification_status'), 
                                default='Unverified', nullable=False)
    rating_avg = Column(DECIMAL(3, 2), default=0.00, nullable=False)
    rating_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("UserModel", back_populates="tutor_profile")
    credentials = relationship("CredentialModel", back_populates="tutor")
    tutor_subjects = relationship("TutorSubjectModel", back_populates="tutor")
    service_listings = relationship("ServiceListingModel", back_populates="tutor")
    availability_slots = relationship("AvailabilitySlotModel", back_populates="tutor")
    bookings = relationship("BookingModel", back_populates="tutor")
    payouts = relationship("PayoutModel", back_populates="tutor")
    reviews = relationship("ReviewModel", back_populates="tutor")
    chat_threads = relationship("ChatThreadModel", back_populates="tutor")
    
    def __repr__(self):
        return f"<TutorProfileModel(user_id={self.user_id}, full_name='{self.full_name}', verification_status='{self.verification_status}')>"
