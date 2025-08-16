from abc import ABC, abstractmethod
from typing import List, Optional
from ..complaint import Complaint, ComplaintStatus

class IComplaintRepository(ABC):
    """
    Interface for Complaint Repository
    """
    
    @abstractmethod
    def add(self, complaint: Complaint) -> Complaint:
        """Add a new complaint"""
        pass
    
    @abstractmethod
    def get_by_id(self, complaint_id: int) -> Optional[Complaint]:
        """Get complaint by ID"""
        pass
    
    @abstractmethod
    def get_by_user_raised(self, user_id: int) -> List[Complaint]:
        """Get complaints raised by a user"""
        pass
    
    @abstractmethod
    def get_by_user_against(self, user_id: int) -> List[Complaint]:
        """Get complaints against a user"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: ComplaintStatus) -> List[Complaint]:
        """Get complaints by status"""
        pass
    
    @abstractmethod
    def get_by_booking_id(self, booking_id: int) -> List[Complaint]:
        """Get complaints for a booking"""
        pass
    
    @abstractmethod
    def update(self, complaint: Complaint) -> Complaint:
        """Update complaint"""
        pass
    
    @abstractmethod
    def delete(self, complaint_id: int) -> bool:
        """Delete complaint"""
        pass
