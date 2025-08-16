from typing import Optional
from datetime import datetime
from enum import Enum
from decimal import Decimal

class PayoutStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    PAID = "Paid"
    FAILED = "Failed"

class Payout:
    def __init__(
        self,
        id: Optional[int] = None,
        tutor_id: int = 0,
        booking_id: int = 0,
        amount: Decimal = Decimal('0.00'),
        status: PayoutStatus = PayoutStatus.PENDING,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.tutor_id = tutor_id
        self.booking_id = booking_id
        self.amount = amount
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def process(self):
        """Mark payout as processing"""
        self.status = PayoutStatus.PROCESSING
        self.updated_at = datetime.utcnow()
    
    def mark_paid(self):
        """Mark payout as paid"""
        self.status = PayoutStatus.PAID
        self.updated_at = datetime.utcnow()
    
    def fail(self):
        """Mark payout as failed"""
        self.status = PayoutStatus.FAILED
        self.updated_at = datetime.utcnow()
    
    def is_pending(self) -> bool:
        """Check if payout is pending"""
        return self.status == PayoutStatus.PENDING
    
    def is_paid(self) -> bool:
        """Check if payout is paid"""
        return self.status == PayoutStatus.PAID
    
    def is_failed(self) -> bool:
        """Check if payout is failed"""
        return self.status == PayoutStatus.FAILED
