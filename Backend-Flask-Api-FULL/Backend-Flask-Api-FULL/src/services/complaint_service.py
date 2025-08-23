from typing import List, Optional
from src.infrastructure.databases.db import db
from src.infrastructure.models.complaint import Complaint

class ComplaintService:
    def list_complaints(self, status: Optional[str]=None) -> List[Complaint]:
        q = Complaint.query
        if status:
            q = q.filter_by(status=status)
        return q.order_by(Complaint.created_at.desc()).all()

    def create_complaint(self, reporter_id: int, title: str, content: str, target_user_id: Optional[int]=None) -> Complaint:
        c = Complaint(reporter_id=reporter_id, target_user_id=target_user_id, title=title, content=content)
        db.session.add(c)
        db.session.commit()
        return c

    def update_status(self, complaint_id: int, status: str) -> Optional[Complaint]:
        c = Complaint.query.get(complaint_id)
        if not c:
            return None
        c.status = status
        db.session.commit()
        return c

    def delete(self, complaint_id: int) -> bool:
        c = Complaint.query.get(C)

        if not c:
            return False
        db.session.delete(c)
        db.session.commit()
        return True
