from typing import Optional
from datetime import datetime

class ChatThread:
    def __init__(
        self,
        id: Optional[int] = None,
        student_id: int = 0,
        tutor_id: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.student_id = student_id
        self.tutor_id = tutor_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_timestamp(self):
        """Update the last activity timestamp"""
        self.updated_at = datetime.utcnow()
    
    def get_participants(self) -> tuple[int, int]:
        """Get chat participants (student_id, tutor_id)"""
        return (self.student_id, self.tutor_id)
    
    def involves_user(self, user_id: int) -> bool:
        """Check if user is part of this chat thread"""
        return user_id in [self.student_id, self.tutor_id]
