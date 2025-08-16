from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from ..booking import Booking, BookingStatus

class IBookingRepository(ABC):
    """
    Interface for Booking Repository
    """
    
    @abstractmethod
    def add(self, booking: Booking) -> Booking:
        """Add a new booking"""
        pass
    
    @abstractmethod
    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        """Get booking by ID"""
        pass
    
    @abstractmethod
    def get_by_student_id(self, student_id: int) -> List[Booking]:
        """Get all bookings for a student"""
        pass
    
    @abstractmethod
    def get_by_tutor_id(self, tutor_id: int) -> List[Booking]:
        """Get all bookings for a tutor"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: BookingStatus) -> List[Booking]:
        """Get bookings by status"""
        pass
    
    @abstractmethod
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Booking]:
        """Get bookings within a date range"""
        pass
    
    @abstractmethod
    def get_upcoming_bookings(self, user_id: int) -> List[Booking]:
        """Get upcoming bookings for a user"""
        pass
    
    @abstractmethod
    def update(self, booking: Booking) -> Booking:
        """Update booking"""
        pass
    
    @abstractmethod
    def delete(self, booking_id: int) -> bool:
        """Delete booking"""
        pass
