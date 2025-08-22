from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from domain.models.payout import Payout, PayoutStatus
from domain.models.interfaces.ipayout_repository import IPayoutRepository


class PayoutService:
    """
    Service class for Payout business logic
    Handles payout creation, processing, and management for tutors
    """
    
    def __init__(self, repository: IPayoutRepository):
        self.repository = repository

    def create_payout(
        self, 
        tutor_id: int, 
        booking_id: int,
        amount: Decimal
    ) -> Payout:
        """
        Create a new payout for a tutor
        
        Args:
            tutor_id: ID of the tutor receiving the payout
            booking_id: ID of the booking this payout is for
            amount: Payout amount
            
        Returns:
            Created Payout object
        """
        payout = Payout(
            tutor_id=tutor_id,
            booking_id=booking_id,
            amount=amount,
            status=PayoutStatus.PENDING,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return self.repository.add(payout)

    def get_payout(self, payout_id: int) -> Optional[Payout]:
        """
        Get payout by ID
        
        Args:
            payout_id: Payout ID
            
        Returns:
            Payout object if found, None otherwise
        """
        return self.repository.get_by_id(payout_id)

    def get_tutor_payouts(self, tutor_id: int) -> List[Payout]:
        """
        Get all payouts for a specific tutor
        
        Args:
            tutor_id: Tutor ID
            
        Returns:
            List of Payout objects
        """
        return self.repository.get_by_tutor_id(tutor_id)

    def get_booking_payouts(self, booking_id: int) -> List[Payout]:
        """
        Get all payouts for a specific booking
        
        Args:
            booking_id: Booking ID
            
        Returns:
            List of Payout objects
        """
        return self.repository.get_by_booking_id(booking_id)

    def process_payout(self, payout_id: int) -> Optional[Payout]:
        """
        Mark a payout as processing
        
        Args:
            payout_id: Payout ID to process
            
        Returns:
            Updated Payout object if successful, None if payout not found
        """
        payout = self.repository.get_by_id(payout_id)
        if not payout:
            return None
            
        if payout.status != PayoutStatus.PENDING:
            raise ValueError(f"Cannot process payout with status: {payout.status.value}")
            
        payout.process()
        return self.repository.update(payout)

    def complete_payout(self, payout_id: int) -> Optional[Payout]:
        """
        Mark a payout as paid/completed
        
        Args:
            payout_id: Payout ID to complete
            
        Returns:
            Updated Payout object if successful, None if payout not found
        """
        payout = self.repository.get_by_id(payout_id)
        if not payout:
            return None
            
        if payout.status not in [PayoutStatus.PENDING, PayoutStatus.PROCESSING]:
            raise ValueError(f"Cannot complete payout with status: {payout.status.value}")
            
        payout.mark_paid()
        return self.repository.update(payout)

    def fail_payout(self, payout_id: int) -> Optional[Payout]:
        """
        Mark a payout as failed
        
        Args:
            payout_id: Payout ID to mark as failed
            
        Returns:
            Updated Payout object if successful, None if payout not found
        """
        payout = self.repository.get_by_id(payout_id)
        if not payout:
            return None
            
        payout.fail()
        return self.repository.update(payout)

    def get_pending_payouts(self) -> List[Payout]:
        """
        Get all pending payouts for processing
        
        Returns:
            List of pending Payout objects
        """
        return self.repository.get_by_status(PayoutStatus.PENDING)

    def get_payouts_by_status(self, status: PayoutStatus) -> List[Payout]:
        """
        Get all payouts with a specific status
        
        Args:
            status: Payout status to filter by
            
        Returns:
            List of Payout objects
        """
        return self.repository.get_by_status(status)

    def calculate_tutor_earnings(self, tutor_id: int) -> Decimal:
        """
        Calculate total earnings for a tutor (completed payouts)
        
        Args:
            tutor_id: Tutor ID
            
        Returns:
            Total earnings amount
        """
        payouts = self.get_tutor_payouts(tutor_id)
        total = Decimal('0.00')
        
        for payout in payouts:
            if payout.status == PayoutStatus.PAID:
                total += payout.amount
                
        return total

    def calculate_pending_earnings(self, tutor_id: int) -> Decimal:
        """
        Calculate pending earnings for a tutor (pending and processing payouts)
        
        Args:
            tutor_id: Tutor ID
            
        Returns:
            Pending earnings amount
        """
        payouts = self.get_tutor_payouts(tutor_id)
        total = Decimal('0.00')
        
        for payout in payouts:
            if payout.status in [PayoutStatus.PENDING, PayoutStatus.PROCESSING]:
                total += payout.amount
                
        return total

    def update_payout_status(self, payout_id: int, new_status: PayoutStatus) -> Optional[Payout]:
        """
        Update payout status
        
        Args:
            payout_id: Payout ID
            new_status: New payout status
            
        Returns:
            Updated Payout object if successful, None if payout not found
        """
        payout = self.repository.get_by_id(payout_id)
        if not payout:
            return None
            
        payout.status = new_status
        payout.updated_at = datetime.utcnow()
        return self.repository.update(payout)

    def is_payout_completed(self, payout_id: int) -> bool:
        """
        Check if a payout is completed
        
        Args:
            payout_id: Payout ID to check
            
        Returns:
            True if payout is paid, False otherwise
        """
        payout = self.repository.get_by_id(payout_id)
        return payout is not None and payout.is_paid()
