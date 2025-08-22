from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from domain.models.payment import Payment, PaymentMethod, PaymentStatus
from domain.models.interfaces.ipayment_repository import IPaymentRepository


class PaymentService:
    """
    Service class for Payment business logic
    Handles payment processing, authorization, capture, and refund operations
    """
    
    def __init__(self, repository: IPaymentRepository):
        self.repository = repository

    def create_payment(
        self, 
        booking_id: int, 
        amount: Decimal, 
        method: PaymentMethod,
        provider_txn_id: str = "",
        currency: str = "USD"
    ) -> Payment:
        """
        Create a new payment for a booking
        
        Args:
            booking_id: ID of the booking this payment is for
            amount: Payment amount
            method: Payment method (Card, Wallet, Bank)
            provider_txn_id: Transaction ID from payment provider
            currency: Currency code (default: USD)
            
        Returns:
            Created Payment object
        """
        payment = Payment(
            booking_id=booking_id,
            method=method,
            provider_txn_id=provider_txn_id,
            amount=amount,
            currency=currency,
            status=PaymentStatus.AUTHORIZED,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return self.repository.add(payment)

    def get_payment(self, payment_id: int) -> Optional[Payment]:
        """
        Get payment by ID
        
        Args:
            payment_id: Payment ID
            
        Returns:
            Payment object if found, None otherwise
        """
        return self.repository.get_by_id(payment_id)

    def get_payment_by_booking(self, booking_id: int) -> Optional[Payment]:
        """
        Get payment for a specific booking
        
        Args:
            booking_id: Booking ID
            
        Returns:
            Payment object if found, None otherwise
        """
        return self.repository.get_by_booking_id(booking_id)

    def capture_payment(self, payment_id: int) -> Optional[Payment]:
        """
        Capture an authorized payment
        
        Args:
            payment_id: Payment ID to capture
            
        Returns:
            Updated Payment object if successful, None if payment not found
        """
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
            
        if payment.status != PaymentStatus.AUTHORIZED:
            raise ValueError(f"Cannot capture payment with status: {payment.status.value}")
            
        payment.capture()
        return self.repository.update(payment)

    def refund_payment(self, payment_id: int) -> Optional[Payment]:
        """
        Refund a captured payment
        
        Args:
            payment_id: Payment ID to refund
            
        Returns:
            Updated Payment object if successful, None if payment not found
        """
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
            
        if payment.status != PaymentStatus.CAPTURED:
            raise ValueError(f"Cannot refund payment with status: {payment.status.value}")
            
        payment.refund()
        return self.repository.update(payment)

    def fail_payment(self, payment_id: int) -> Optional[Payment]:
        """
        Mark a payment as failed
        
        Args:
            payment_id: Payment ID to mark as failed
            
        Returns:
            Updated Payment object if successful, None if payment not found
        """
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
            
        payment.fail()
        return self.repository.update(payment)

    def list_payments_by_status(self, status: PaymentStatus) -> List[Payment]:
        """
        Get all payments with a specific status
        
        Args:
            status: Payment status to filter by
            
        Returns:
            List of Payment objects
        """
        return self.repository.get_by_status(status)

    def update_payment_status(self, payment_id: int, new_status: PaymentStatus) -> Optional[Payment]:
        """
        Update payment status
        
        Args:
            payment_id: Payment ID
            new_status: New payment status
            
        Returns:
            Updated Payment object if successful, None if payment not found
        """
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
            
        payment.status = new_status
        payment.updated_at = datetime.utcnow()
        return self.repository.update(payment)

    def is_payment_successful(self, payment_id: int) -> bool:
        """
        Check if a payment was successful (captured)
        
        Args:
            payment_id: Payment ID to check
            
        Returns:
            True if payment is captured, False otherwise
        """
        payment = self.repository.get_by_id(payment_id)
        return payment is not None and payment.status == PaymentStatus.CAPTURED
