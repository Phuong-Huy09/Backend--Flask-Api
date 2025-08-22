from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.ipayment_repository import IPaymentRepository
from domain.models.payment import Payment, PaymentMethod, PaymentStatus
from infrastructure.models.payment_model import PaymentModel
from infrastructure.repositories.base_repository import BaseRepository
from decimal import Decimal

class PaymentRepository(BaseRepository[PaymentModel], IPaymentRepository):
    """
    Payment Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(PaymentModel, session)
    
    def _model_to_domain(self, model: PaymentModel) -> Payment:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return Payment(
            id=model.id,
            booking_id=model.booking_id,
            method=PaymentMethod(model.method),
            provider_txn_id=model.provider_txn_id,
            amount=Decimal(str(model.amount)),
            currency=model.currency,
            status=PaymentStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: Payment) -> PaymentModel:
        """Convert domain entity to SQLAlchemy model"""
        return PaymentModel(
            id=domain.id,
            booking_id=domain.booking_id,
            method=domain.method.value,
            provider_txn_id=domain.provider_txn_id,
            amount=domain.amount,
            currency=domain.currency,
            status=domain.status.value,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, payment: Payment) -> Payment:
        """Add a new payment"""
        model = self._domain_to_model(payment)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """Get payment by ID"""
        model = super().get_by_id(payment_id)
        return self._model_to_domain(model)
    
    def get_by_booking_id(self, booking_id: int) -> Optional[Payment]:
        """Get payment by booking ID"""
        try:
            model = self.session.query(PaymentModel).filter_by(booking_id=booking_id).first()
            return self._model_to_domain(model)
        except Exception as e:
            raise ValueError(f'Error getting payment by booking_id: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, payment: Payment) -> Payment:
        """Update payment"""
        try:
            model = self.session.query(PaymentModel).filter_by(id=payment.id).first()
            if not model:
                raise ValueError(f'Payment with id {payment.id} not found')
            
            model.method = payment.method.value
            model.provider_txn_id = payment.provider_txn_id
            model.amount = payment.amount
            model.currency = payment.currency
            model.status = payment.status.value
            model.updated_at = payment.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating payment: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, payment_id: int) -> bool:
        """Delete payment"""
        return super().delete(payment_id)
    
    def get_by_status(self, status: PaymentStatus) -> List[Payment]:
        """Get payments by status"""
        try:
            models = self.session.query(PaymentModel).filter_by(status=status.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting payments by status: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_provider_txn_id(self, provider_txn_id: str) -> Optional[Payment]:
        """Get payment by provider transaction ID"""
        try:
            model = self.session.query(PaymentModel).filter_by(provider_txn_id=provider_txn_id).first()
            return self._model_to_domain(model)
        except Exception as e:
            raise ValueError(f'Error getting payment by provider_txn_id: {str(e)}')
        finally:
            self.session.close()
