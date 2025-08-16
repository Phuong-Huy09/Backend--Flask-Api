from abc import ABC, abstractmethod
from typing import List, Optional
from ..review import Review

class IReviewRepository(ABC):
    """
    Interface for Review Repository
    """
    
    @abstractmethod
    def add(self, review: Review) -> Review:
        """Add a new review"""
        pass
    
    @abstractmethod
    def get_by_id(self, review_id: int) -> Optional[Review]:
        """Get review by ID"""
        pass
    
    @abstractmethod
    def get_by_booking_id(self, booking_id: int) -> Optional[Review]:
        """Get review by booking ID"""
        pass
    
    @abstractmethod
    def get_by_tutor_id(self, tutor_id: int) -> List[Review]:
        """Get all reviews for a tutor"""
        pass
    
    @abstractmethod
    def get_by_student_id(self, student_id: int) -> List[Review]:
        """Get all reviews by a student"""
        pass
    
    @abstractmethod
    def update(self, review: Review) -> Review:
        """Update review"""
        pass
    
    @abstractmethod
    def delete(self, review_id: int) -> bool:
        """Delete review"""
        pass
    
    @abstractmethod
    def get_average_rating_for_tutor(self, tutor_id: int) -> float:
        """Get average rating for a tutor"""
        pass
