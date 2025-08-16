from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.ipayout_repository import IPayoutRepository
from domain.models.payout import Payout, PayoutStatus
from infrastructure.models.payout_model import PayoutModel
from infrastructure.repositories.base_repository import BaseRepository
from decimal import Decimal

class PayoutRepository(BaseRepository[PayoutModel], IPayoutRepository):
    """
    Payout Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(PayoutModel, session)
    
    def _model_to_domain(self, model: PayoutModel) -> Payout:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return Payout(
            id=model.id,
            tutor_id=model.tutor_id,
            booking_id=model.booking_id,
            amount=Decimal(str(model.amount)),
            status=PayoutStatus(model.status.value) if hasattr(model.status, 'value') else PayoutStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: Payout) -> PayoutModel:
        """Convert domain entity to SQLAlchemy model"""
        return PayoutModel(
            id=domain.id,
            tutor_id=domain.tutor_id,
            booking_id=domain.booking_id,
            amount=domain.amount,
            status=domain.status.value,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, payout: Payout) -> Payout:
        """Add a new payout"""
        model = self._domain_to_model(payout)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, payout_id: int) -> Optional[Payout]:
        """Get payout by ID"""
        model = super().get_by_id(payout_id)
        return self._model_to_domain(model)
    
    def get_by_tutor_id(self, tutor_id: int) -> List[Payout]:
        """Get all payouts for a tutor"""
        try:
            models = self.session.query(PayoutModel).filter_by(tutor_id=tutor_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting payouts by tutor_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_booking_id(self, booking_id: int) -> List[Payout]:
        """Get payouts for a booking"""
        try:
            models = self.session.query(PayoutModel).filter_by(booking_id=booking_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting payouts by booking_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_status(self, status: PayoutStatus) -> List[Payout]:
        """Get payouts by status"""
        try:
            models = self.session.query(PayoutModel).filter_by(status=status.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting payouts by status: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, payout: Payout) -> Payout:
        """Update payout"""
        try:
            model = self.session.query(PayoutModel).filter_by(id=payout.id).first()
            if not model:
                raise ValueError(f'Payout with id {payout.id} not found')
            
            model.amount = payout.amount
            model.status = payout.status.value
            model.updated_at = payout.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating payout: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, payout_id: int) -> bool:
        """Delete payout"""
        return super().delete(payout_id)
    
    def get_pending_payouts(self) -> List[Payout]:
        """Get all pending payouts"""
        return self.get_by_status(PayoutStatus.PENDING)
