from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.inotification_repository import INotificationRepository
from domain.models.notification import Notification, NotificationType, NotificationChannel
from infrastructure.models.notification_model import NotificationModel
from infrastructure.repositories.base_repository import BaseRepository

class NotificationRepository(BaseRepository[NotificationModel], INotificationRepository):
    """
    Notification Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(NotificationModel, session)
    
    def _model_to_domain(self, model: NotificationModel) -> Notification:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return Notification(
            id=model.id,
            user_id=model.user_id,
            type=NotificationType(model.type.value) if hasattr(model.type, 'value') else NotificationType(model.type),
            channel=NotificationChannel(model.channel.value) if hasattr(model.channel, 'value') else NotificationChannel(model.channel),
            payload=model.payload,
            sent_at=model.sent_at,
            read_at=model.read_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: Notification) -> NotificationModel:
        """Convert domain entity to SQLAlchemy model"""
        return NotificationModel(
            id=domain.id,
            user_id=domain.user_id,
            type=domain.type.value,
            channel=domain.channel.value,
            payload=domain.payload,
            sent_at=domain.sent_at,
            read_at=domain.read_at,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, notification: Notification) -> Notification:
        """Add a new notification"""
        model = self._domain_to_model(notification)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, notification_id: int) -> Optional[Notification]:
        """Get notification by ID"""
        model = super().get_by_id(notification_id)
        return self._model_to_domain(model)
    
    def get_by_user_id(self, user_id: int) -> List[Notification]:
        """Get all notifications for a user"""
        try:
            models = self.session.query(NotificationModel).filter_by(user_id=user_id).order_by(
                NotificationModel.created_at.desc()
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting notifications by user_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_unread_by_user_id(self, user_id: int) -> List[Notification]:
        """Get unread notifications for a user"""
        try:
            models = self.session.query(NotificationModel).filter_by(
                user_id=user_id, read_at=None
            ).filter(NotificationModel.sent_at.isnot(None)).order_by(
                NotificationModel.created_at.desc()
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting unread notifications: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_type(self, notification_type: NotificationType) -> List[Notification]:
        """Get notifications by type"""
        try:
            models = self.session.query(NotificationModel).filter_by(type=notification_type.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting notifications by type: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_channel(self, channel: NotificationChannel) -> List[Notification]:
        """Get notifications by channel"""
        try:
            models = self.session.query(NotificationModel).filter_by(channel=channel.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting notifications by channel: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, notification: Notification) -> Notification:
        """Update notification"""
        try:
            model = self.session.query(NotificationModel).filter_by(id=notification.id).first()
            if not model:
                raise ValueError(f'Notification with id {notification.id} not found')
            
            model.type = notification.type.value
            model.channel = notification.channel.value
            model.payload = notification.payload
            model.sent_at = notification.sent_at
            model.read_at = notification.read_at
            model.updated_at = notification.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating notification: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, notification_id: int) -> bool:
        """Delete notification"""
        return super().delete(notification_id)
    
    def mark_all_read_for_user(self, user_id: int) -> bool:
        """Mark all notifications as read for a user"""
        try:
            from datetime import datetime
            models = self.session.query(NotificationModel).filter_by(
                user_id=user_id, read_at=None
            ).all()
            
            for model in models:
                model.read_at = datetime.utcnow()
                model.updated_at = datetime.utcnow()
            
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error marking notifications as read: {str(e)}')
        finally:
            self.session.close()
