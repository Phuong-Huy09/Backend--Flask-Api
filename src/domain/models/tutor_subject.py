from typing import Optional
from datetime import datetime

class TutorSubject:
    def __init__(
        self,
        tutor_id: int,
        subject_id: int,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.tutor_id = tutor_id
        self.subject_id = subject_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
