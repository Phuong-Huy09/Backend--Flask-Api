from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.ichat_thread_repository import IChatThreadRepository
from domain.models.chat_thread import ChatThread
from infrastructure.models.chat_thread_model import ChatThreadModel
from infrastructure.repositories.base_repository import BaseRepository

class ChatThreadRepository(BaseRepository[ChatThreadModel], IChatThreadRepository):
    """
    Chat Thread Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(ChatThreadModel, session)
    
    def _model_to_domain(self, model: ChatThreadModel) -> ChatThread:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return ChatThread(
            id=model.id,
            student_id=model.student_id,
            tutor_id=model.tutor_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: ChatThread) -> ChatThreadModel:
        """Convert domain entity to SQLAlchemy model"""
        return ChatThreadModel(
            id=domain.id,
            student_id=domain.student_id,
            tutor_id=domain.tutor_id,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, chat_thread: ChatThread) -> ChatThread:
        """Add a new chat thread"""
        model = self._domain_to_model(chat_thread)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, thread_id: int) -> Optional[ChatThread]:
        """Get chat thread by ID"""
        model = super().get_by_id(thread_id)
        return self._model_to_domain(model)
    
    def get_by_participants(self, student_id: int, tutor_id: int) -> Optional[ChatThread]:
        """Get chat thread by participants"""
        try:
            model = self.session.query(ChatThreadModel).filter_by(
                student_id=student_id, tutor_id=tutor_id
            ).first()
            return self._model_to_domain(model)
        except Exception as e:
            raise ValueError(f'Error getting chat thread by participants: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_student_id(self, student_id: int) -> List[ChatThread]:
        """Get all chat threads for a student"""
        try:
            models = self.session.query(ChatThreadModel).filter_by(student_id=student_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting chat threads by student_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_tutor_id(self, tutor_id: int) -> List[ChatThread]:
        """Get all chat threads for a tutor"""
        try:
            models = self.session.query(ChatThreadModel).filter_by(tutor_id=tutor_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting chat threads by tutor_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_user_id(self, user_id: int) -> List[ChatThread]:
        """Get all chat threads for a user (student or tutor)"""
        try:
            models = self.session.query(ChatThreadModel).filter(
                (ChatThreadModel.student_id == user_id) | (ChatThreadModel.tutor_id == user_id)
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting chat threads by user_id: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, chat_thread: ChatThread) -> ChatThread:
        """Update chat thread"""
        try:
            model = self.session.query(ChatThreadModel).filter_by(id=chat_thread.id).first()
            if not model:
                raise ValueError(f'Chat thread with id {chat_thread.id} not found')
            
            model.updated_at = chat_thread.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating chat thread: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, thread_id: int) -> bool:
        """Delete chat thread"""
        return super().delete(thread_id)
