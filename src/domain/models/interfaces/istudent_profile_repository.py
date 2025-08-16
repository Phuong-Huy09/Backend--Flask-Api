from abc import ABC, abstractmethod
from typing import List, Optional
from ..student_profile import StudentProfile

class IStudentProfileRepository(ABC):
    """
    Interface for Student Profile Repository
    """
    
    @abstractmethod
    def add(self, student_profile: StudentProfile) -> StudentProfile:
        """Add a new student profile"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[StudentProfile]:
        """Get student profile by user ID"""
        pass
    
    @abstractmethod
    def update(self, student_profile: StudentProfile) -> StudentProfile:
        """Update student profile"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete student profile"""
        pass
    
    @abstractmethod
    def search_by_name(self, name: str) -> List[StudentProfile]:
        """Search student profiles by name"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[StudentProfile]:
        """Get all student profiles"""
        pass
