from abc import ABC, abstractmethod
from typing import List, Optional
from ..payout import Payout, PayoutStatus

class IPayoutRepository(ABC):
    """
    Interface for Payout Repository
    """
    
    @abstractmethod
    def add(self, payout: Payout) -> Payout:
        """Add a new payout"""
        pass
    
    @abstractmethod
    def get_by_id(self, payout_id: int) -> Optional[Payout]:
        """Get payout by ID"""
        pass
    
    @abstractmethod
    def get_by_tutor_id(self, tutor_id: int) -> List[Payout]:
        """Get all payouts for a tutor"""
        pass
    
    @abstractmethod
    def get_by_booking_id(self, booking_id: int) -> List[Payout]:
        """Get payouts for a booking"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: PayoutStatus) -> List[Payout]:
        """Get payouts by status"""
        pass
    
    @abstractmethod
    def update(self, payout: Payout) -> Payout:
        """Update payout"""
        pass
    
    @abstractmethod
    def delete(self, payout_id: int) -> bool:
        """Delete payout"""
        pass
    
    @abstractmethod
    def get_pending_payouts(self) -> List[Payout]:
        """Get all pending payouts"""
        pass
