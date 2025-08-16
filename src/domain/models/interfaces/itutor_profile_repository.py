from abc import ABC, abstractmethod
from typing import List, Optional
from ..tutor_profile import TutorProfile, VerificationStatus

class ITutorProfileRepository(ABC):
    """
    Interface for Tutor Profile Repository
    """
    
    @abstractmethod
    def add(self, tutor_profile: TutorProfile) -> TutorProfile:
        """Add a new tutor profile"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[TutorProfile]:
        """Get tutor profile by user ID"""
        pass
    
    @abstractmethod
    def update(self, tutor_profile: TutorProfile) -> TutorProfile:
        """Update tutor profile"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete tutor profile"""
        pass
    
    @abstractmethod
    def get_by_verification_status(self, status: VerificationStatus) -> List[TutorProfile]:
        """Get tutor profiles by verification status"""
        pass
    
    @abstractmethod
    def search_by_name(self, name: str) -> List[TutorProfile]:
        """Search tutor profiles by name"""
        pass
    
    @abstractmethod
    def get_verified_tutors(self) -> List[TutorProfile]:
        """Get all verified tutors"""
        pass
    
    @abstractmethod
    def get_by_rating_range(self, min_rating: float, max_rating: float) -> List[TutorProfile]:
        """Get tutors by rating range"""
        pass
