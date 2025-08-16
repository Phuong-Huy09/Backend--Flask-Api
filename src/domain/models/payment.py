from typing import Optional
from datetime import datetime
from enum import Enum
from decimal import Decimal

class PaymentMethod(Enum):
    CARD = "Card"
    WALLET = "Wallet"
    BANK = "Bank"

class PaymentStatus(Enum):
    AUTHORIZED = "Authorized"
    CAPTURED = "Captured"
    FAILED = "Failed"
    REFUNDED = "Refunded"

class Payment:
    def __init__(
        self,
        id: Optional[int] = None,
        booking_id: int = 0,
        method: PaymentMethod = PaymentMethod.CARD,
        provider_txn_id: str = "",
        amount: Decimal = Decimal('0.00'),
        currency: str = "USD",
        status: PaymentStatus = PaymentStatus.AUTHORIZED,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.booking_id = booking_id
        self.method = method
        self.provider_txn_id = provider_txn_id
        self.amount = amount
        self.currency = currency
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def capture(self):
        """Capture the payment"""
        self.status = PaymentStatus.CAPTURED
        self.updated_at = datetime.utcnow()
    
    def refund(self):
        """Refund the payment"""
        self.status = PaymentStatus.REFUNDED
        self.updated_at = datetime.utcnow()
    
    def fail(self):
        """Mark payment as failed"""
        self.status = PaymentStatus.FAILED
        self.updated_at = datetime.utcnow()
    
    def is_successful(self) -> bool:
        """Check if payment is successful"""
        return self.status in [PaymentStatus.AUTHORIZED, PaymentStatus.CAPTURED]
    
    def is_refunded(self) -> bool:
        """Check if payment is refunded"""
        return self.status == PaymentStatus.REFUNDED
