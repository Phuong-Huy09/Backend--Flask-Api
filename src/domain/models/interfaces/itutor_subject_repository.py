from abc import ABC, abstractmethod
from typing import List, Optional
from ..tutor_subject import TutorSubject

class ITutorSubjectRepository(ABC):
    """
    Interface for Tutor Subject Repository
    """
    
    @abstractmethod
    def add(self, tutor_subject: TutorSubject) -> TutorSubject:
        """Add a new tutor subject"""
        pass
    
    @abstractmethod
    def get_by_tutor_id(self, tutor_id: int) -> List[TutorSubject]:
        """Get all subjects for a tutor"""
        pass
    
    @abstractmethod
    def get_by_subject_id(self, subject_id: int) -> List[TutorSubject]:
        """Get all tutors for a subject"""
        pass
    
    @abstractmethod
    def get_by_tutor_and_subject(self, tutor_id: int, subject_id: int) -> Optional[TutorSubject]:
        """Get tutor subject by tutor and subject ID"""
        pass
    
    @abstractmethod
    def update(self, tutor_subject: TutorSubject) -> TutorSubject:
        """Update tutor subject"""
        pass
    
    @abstractmethod
    def delete(self, tutor_id: int, subject_id: int) -> bool:
        """Delete tutor subject"""
        pass
    
    @abstractmethod
    def delete_by_tutor_id(self, tutor_id: int) -> bool:
        """Delete all subjects for a tutor"""
        pass
