from typing import Optional
from datetime import datetime, date

class StudentProfile:
    def __init__(
        self,
        user_id: int,
        full_name: str,
        dob: Optional[date] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.full_name = full_name
        self.dob = dob
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_profile(self, full_name: Optional[str] = None, dob: Optional[date] = None):
        if full_name is not None:
            self.full_name = full_name
        if dob is not None:
            self.dob = dob
        self.updated_at = datetime.utcnow()
