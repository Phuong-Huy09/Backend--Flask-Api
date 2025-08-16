from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.imessage_repository import IMessageRepository
from domain.models.message import Message
from infrastructure.models.message_model import MessageModel
from infrastructure.repositories.base_repository import BaseRepository

class MessageRepository(BaseRepository[MessageModel], IMessageRepository):
    """
    Message Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(MessageModel, session)
    
    def _model_to_domain(self, model: MessageModel) -> Message:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return Message(
            id=model.id,
            thread_id=model.thread_id,
            sender_id=model.sender_id,
            body=model.body,
            attachment_url=model.attachment_url,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: Message) -> MessageModel:
        """Convert domain entity to SQLAlchemy model"""
        return MessageModel(
            id=domain.id,
            thread_id=domain.thread_id,
            sender_id=domain.sender_id,
            body=domain.body,
            attachment_url=domain.attachment_url,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, message: Message) -> Message:
        """Add a new message"""
        model = self._domain_to_model(message)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, message_id: int) -> Optional[Message]:
        """Get message by ID"""
        model = super().get_by_id(message_id)
        return self._model_to_domain(model)
    
    def get_by_thread_id(self, thread_id: int) -> List[Message]:
        """Get all messages in a thread"""
        try:
            models = self.session.query(MessageModel).filter_by(thread_id=thread_id).order_by(MessageModel.created_at).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting messages by thread_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_sender_id(self, sender_id: int) -> List[Message]:
        """Get all messages by a sender"""
        try:
            models = self.session.query(MessageModel).filter_by(sender_id=sender_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting messages by sender_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_latest_messages_in_thread(self, thread_id: int, limit: int = 50) -> List[Message]:
        """Get latest messages in a thread"""
        try:
            models = self.session.query(MessageModel).filter_by(thread_id=thread_id).order_by(
                MessageModel.created_at.desc()
            ).limit(limit).all()
            # Reverse to get chronological order
            models.reverse()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting latest messages: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, message: Message) -> Message:
        """Update message"""
        try:
            model = self.session.query(MessageModel).filter_by(id=message.id).first()
            if not model:
                raise ValueError(f'Message with id {message.id} not found')
            
            model.body = message.body
            model.attachment_url = message.attachment_url
            model.updated_at = message.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating message: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, message_id: int) -> bool:
        """Delete message"""
        return super().delete(message_id)
    
    def count_messages_in_thread(self, thread_id: int) -> int:
        """Count messages in a thread"""
        try:
            count = self.session.query(MessageModel).filter_by(thread_id=thread_id).count()
            return count
        except Exception as e:
            raise ValueError(f'Error counting messages in thread: {str(e)}')
        finally:
            self.session.close()
