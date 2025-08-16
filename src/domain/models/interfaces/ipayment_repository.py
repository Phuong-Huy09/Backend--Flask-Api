from abc import ABC, abstractmethod
from typing import List, Optional
from ..payment import Payment, PaymentStatus

class IPaymentRepository(ABC):
    """
    Interface for Payment Repository
    """
    
    @abstractmethod
    def add(self, payment: Payment) -> Payment:
        """Add a new payment"""
        pass
    
    @abstractmethod
    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """Get payment by ID"""
        pass
    
    @abstractmethod
    def get_by_booking_id(self, booking_id: int) -> Optional[Payment]:
        """Get payment by booking ID"""
        pass
    
    @abstractmethod
    def update(self, payment: Payment) -> Payment:
        """Update payment"""
        pass
    
    @abstractmethod
    def delete(self, payment_id: int) -> bool:
        """Delete payment"""
        pass
    
    @abstractmethod
    def get_by_status(self, status: PaymentStatus) -> List[Payment]:
        """Get payments by status"""
        pass
    
    @abstractmethod
    def get_by_provider_txn_id(self, provider_txn_id: str) -> Optional[Payment]:
        """Get payment by provider transaction ID"""
        pass
