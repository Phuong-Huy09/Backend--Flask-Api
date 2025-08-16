from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.imoderation_action_repository import IModerationActionRepository
from domain.models.moderation_action import ModerationAction, ModerationActionType
from infrastructure.models.moderation_action_model import ModerationActionModel
from infrastructure.repositories.base_repository import BaseRepository

class ModerationActionRepository(BaseRepository[ModerationActionModel], IModerationActionRepository):
    """
    Moderation Action Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(ModerationActionModel, session)
    
    def _model_to_domain(self, model: ModerationActionModel) -> ModerationAction:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return ModerationAction(
            id=model.id,
            complaint_id=model.complaint_id,
            moderator_id=model.moderator_id,
            action=ModerationActionType(model.action.value) if hasattr(model.action, 'value') else ModerationActionType(model.action),
            note=model.note,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: ModerationAction) -> ModerationActionModel:
        """Convert domain entity to SQLAlchemy model"""
        return ModerationActionModel(
            id=domain.id,
            complaint_id=domain.complaint_id,
            moderator_id=domain.moderator_id,
            action=domain.action.value,
            note=domain.note,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, moderation_action: ModerationAction) -> ModerationAction:
        """Add a new moderation action"""
        model = self._domain_to_model(moderation_action)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, action_id: int) -> Optional[ModerationAction]:
        """Get moderation action by ID"""
        model = super().get_by_id(action_id)
        return self._model_to_domain(model)
    
    def get_by_complaint_id(self, complaint_id: int) -> List[ModerationAction]:
        """Get all moderation actions for a complaint"""
        try:
            models = self.session.query(ModerationActionModel).filter_by(complaint_id=complaint_id).order_by(
                ModerationActionModel.created_at
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting moderation actions by complaint_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_moderator_id(self, moderator_id: int) -> List[ModerationAction]:
        """Get all moderation actions by a moderator"""
        try:
            models = self.session.query(ModerationActionModel).filter_by(moderator_id=moderator_id).order_by(
                ModerationActionModel.created_at.desc()
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting moderation actions by moderator_id: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, moderation_action: ModerationAction) -> ModerationAction:
        """Update moderation action"""
        try:
            model = self.session.query(ModerationActionModel).filter_by(id=moderation_action.id).first()
            if not model:
                raise ValueError(f'Moderation action with id {moderation_action.id} not found')
            
            model.action = moderation_action.action.value
            model.note = moderation_action.note
            model.updated_at = moderation_action.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating moderation action: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, action_id: int) -> bool:
        """Delete moderation action"""
        return super().delete(action_id)
