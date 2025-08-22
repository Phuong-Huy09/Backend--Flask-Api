from abc import ABC, abstractmethod
from typing import List, Optional
from ..subject import Subject, SubjectLevel

class ISubjectRepository(ABC):
    """
    Interface for Subject Repository
    """
    
    @abstractmethod
    def add(self, subject: Subject) -> Subject:
        """Add a new subject"""
        pass
    
    @abstractmethod
    def get_by_id(self, subject_id: int) -> Optional[Subject]:
        """Get subject by ID"""
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Subject]:
        """Get subject by name"""
        pass
    
    @abstractmethod
    def get_by_level(self, level: SubjectLevel) -> List[Subject]:
        """Get subjects by level"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Subject]:
        """Get all subjects"""
        pass
    
    @abstractmethod
    def update(self, subject: Subject) -> Subject:
        """Update subject"""
        pass
    
    @abstractmethod
    def delete(self, subject_id: int) -> bool:
        """Delete subject"""
        pass
    
    @abstractmethod
    def search_by_name(self, name: str) -> List[Subject]:
        """Search subjects by name pattern"""
        pass

    # @abstractmethod
    # def check_contract(self, name: str) -> bool:
    #     """Check if subject exists by name"""
    #     pass