from typing import List, Optional
from src.infrastructure.databases.db import db
from src.infrastructure.models.notification import Notification

class NotificationService:
    def list_notifications(self, user_id: int, is_read: Optional[bool]=None) -> List[Notification]:
        query = Notification.query.filter_by(user_id=user_id)
        if is_read is not None:
            query = query.filter_by(is_read=is_read)
        return query.order_by(Notification.created_at.desc()).all()

    def create_notification(self, user_id: int, title: str, message: str) -> Notification:
        n = Notification(user_id=user_id, title=title, message=message)
        db.session.add(n)
        db.session.commit()
        return n

    def mark_as_read(self, notif_id: int) -> Optional[Notification]:
        n = Notification.query.get(notif_id)
        if not n:
            return None
        n.is_read = True
        db.session.commit()
        return n

    def delete(self, notif_id: int) -> bool:
        n = Notification.query.get(notif_id)
        if not n:
            return False
        db.session.delete(n)
        db.session.commit()
        return True
