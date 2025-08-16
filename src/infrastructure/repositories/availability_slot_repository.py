from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.iavailability_slot_repository import IAvailabilitySlotRepository
from domain.models.availability_slot import AvailabilitySlot, Weekday
from infrastructure.models.availability_slot_model import AvailabilitySlotModel
from infrastructure.repositories.base_repository import BaseRepository

class AvailabilitySlotRepository(BaseRepository[AvailabilitySlotModel], IAvailabilitySlotRepository):
    """
    Availability Slot Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(AvailabilitySlotModel, session)
    
    def _model_to_domain(self, model: AvailabilitySlotModel) -> AvailabilitySlot:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return AvailabilitySlot(
            id=model.id,
            tutor_id=model.tutor_id,
            weekday=Weekday(model.weekday.value) if hasattr(model.weekday, 'value') else Weekday(model.weekday),
            start_time=model.start_time,
            end_time=model.end_time,
            timezone=model.timezone,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: AvailabilitySlot) -> AvailabilitySlotModel:
        """Convert domain entity to SQLAlchemy model"""
        return AvailabilitySlotModel(
            id=domain.id,
            tutor_id=domain.tutor_id,
            weekday=domain.weekday.value,
            start_time=domain.start_time,
            end_time=domain.end_time,
            timezone=domain.timezone,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, availability_slot: AvailabilitySlot) -> AvailabilitySlot:
        """Add a new availability slot"""
        model = self._domain_to_model(availability_slot)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, slot_id: int) -> Optional[AvailabilitySlot]:
        """Get availability slot by ID"""
        model = super().get_by_id(slot_id)
        return self._model_to_domain(model)
    
    def get_by_tutor_id(self, tutor_id: int) -> List[AvailabilitySlot]:
        """Get all availability slots for a tutor"""
        try:
            models = self.session.query(AvailabilitySlotModel).filter_by(tutor_id=tutor_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting availability slots by tutor_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_tutor_and_weekday(self, tutor_id: int, weekday: Weekday) -> List[AvailabilitySlot]:
        """Get availability slots for a tutor on a specific weekday"""
        try:
            models = self.session.query(AvailabilitySlotModel).filter_by(
                tutor_id=tutor_id, weekday=weekday.value
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting availability slots by tutor and weekday: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, availability_slot: AvailabilitySlot) -> AvailabilitySlot:
        """Update availability slot"""
        try:
            model = self.session.query(AvailabilitySlotModel).filter_by(id=availability_slot.id).first()
            if not model:
                raise ValueError(f'Availability slot with id {availability_slot.id} not found')
            
            model.weekday = availability_slot.weekday.value
            model.start_time = availability_slot.start_time
            model.end_time = availability_slot.end_time
            model.timezone = availability_slot.timezone
            model.updated_at = availability_slot.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating availability slot: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, slot_id: int) -> bool:
        """Delete availability slot"""
        return super().delete(slot_id)
    
    def delete_by_tutor_id(self, tutor_id: int) -> bool:
        """Delete all availability slots for a tutor"""
        try:
            models = self.session.query(AvailabilitySlotModel).filter_by(tutor_id=tutor_id).all()
            for model in models:
                self.session.delete(model)
            
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting availability slots: {str(e)}')
        finally:
            self.session.close()
