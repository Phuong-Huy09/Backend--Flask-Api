from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.icomplaint_repository import IComplaintRepository
from domain.models.complaint import Complaint, ComplaintType, ComplaintStatus
from infrastructure.models.complaint_model import ComplaintModel
from infrastructure.repositories.base_repository import BaseRepository

class ComplaintRepository(BaseRepository[ComplaintModel], IComplaintRepository):
    """
    Complaint Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(ComplaintModel, session)
    
    def _model_to_domain(self, model: ComplaintModel) -> Complaint:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return Complaint(
            id=model.id,
            raised_by_user=model.raised_by_user,
            against_user=model.against_user,
            booking_id=model.booking_id,
            type=ComplaintType(model.type.value) if hasattr(model.type, 'value') else ComplaintType(model.type),
            detail=model.detail,
            status=ComplaintStatus(model.status.value) if hasattr(model.status, 'value') else ComplaintStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: Complaint) -> ComplaintModel:
        """Convert domain entity to SQLAlchemy model"""
        return ComplaintModel(
            id=domain.id,
            raised_by_user=domain.raised_by_user,
            against_user=domain.against_user,
            booking_id=domain.booking_id,
            type=domain.type.value,
            detail=domain.detail,
            status=domain.status.value,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, complaint: Complaint) -> Complaint:
        """Add a new complaint"""
        model = self._domain_to_model(complaint)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, complaint_id: int) -> Optional[Complaint]:
        """Get complaint by ID"""
        model = super().get_by_id(complaint_id)
        return self._model_to_domain(model)
    
    def get_by_user_raised(self, user_id: int) -> List[Complaint]:
        """Get complaints raised by a user"""
        try:
            models = self.session.query(ComplaintModel).filter_by(raised_by_user=user_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting complaints by user_raised: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_user_against(self, user_id: int) -> List[Complaint]:
        """Get complaints against a user"""
        try:
            models = self.session.query(ComplaintModel).filter_by(against_user=user_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting complaints by user_against: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_status(self, status: ComplaintStatus) -> List[Complaint]:
        """Get complaints by status"""
        try:
            models = self.session.query(ComplaintModel).filter_by(status=status.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting complaints by status: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_booking_id(self, booking_id: int) -> List[Complaint]:
        """Get complaints for a booking"""
        try:
            models = self.session.query(ComplaintModel).filter_by(booking_id=booking_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting complaints by booking_id: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, complaint: Complaint) -> Complaint:
        """Update complaint"""
        try:
            model = self.session.query(ComplaintModel).filter_by(id=complaint.id).first()
            if not model:
                raise ValueError(f'Complaint with id {complaint.id} not found')
            
            model.type = complaint.type.value
            model.detail = complaint.detail
            model.status = complaint.status.value
            model.updated_at = complaint.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating complaint: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, complaint_id: int) -> bool:
        """Delete complaint"""
        return super().delete(complaint_id)
