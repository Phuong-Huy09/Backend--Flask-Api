from sqlalchemy import Column, Integer, String, DateTime, Enum, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class BookingModel(Base):
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student_profiles.user_id'), nullable=False)
    tutor_id = Column(Integer, ForeignKey('tutor_profiles.user_id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service_listings.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    hours = Column(DECIMAL(4, 2), nullable=False)
    status = Column(Enum('Pending', 'Confirmed', 'InProgress', 'Completed', 'Canceled', 'Refunded',
                         name='booking_status'), 
                    default='Pending', nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student = relationship("StudentProfileModel", back_populates="bookings")
    tutor = relationship("TutorProfileModel", back_populates="bookings")
    service = relationship("ServiceListingModel", back_populates="bookings")
    subject = relationship("SubjectModel", back_populates="bookings")
    payment = relationship("PaymentModel", back_populates="booking", uselist=False)
    payouts = relationship("PayoutModel", back_populates="booking")
    review = relationship("ReviewModel", back_populates="booking", uselist=False)
    complaints = relationship("ComplaintModel", back_populates="booking")
    
    def __repr__(self):
        return f"<BookingModel(id={self.id}, student_id={self.student_id}, tutor_id={self.tutor_id}, status='{self.status}')>"
