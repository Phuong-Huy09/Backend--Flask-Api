from typing import Optional
from datetime import datetime
from enum import Enum

class ModerationActionType(Enum):
    WARN = "Warn"
    BAN = "Ban"
    SUSPEND = "Suspend"
    REMOVE_CONTENT = "RemoveContent"
    REFUND = "Refund"
    NO_ACTION = "NoAction"

class ModerationAction:
    def __init__(
        self,
        id: Optional[int] = None,
        complaint_id: int = 0,
        moderator_id: int = 0,
        action: ModerationActionType = ModerationActionType.NO_ACTION,
        note: str = "",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.complaint_id = complaint_id
        self.moderator_id = moderator_id
        self.action = action
        self.note = note
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_note(self, note: str):
        """Update moderation action note"""
        self.note = note
        self.updated_at = datetime.utcnow()
    
    def is_punitive(self) -> bool:
        """Check if action is punitive"""
        return self.action in [
            ModerationActionType.WARN,
            ModerationActionType.BAN,
            ModerationActionType.SUSPEND,
            ModerationActionType.REMOVE_CONTENT
        ]
    
    def is_no_action(self) -> bool:
        """Check if no action was taken"""
        return self.action == ModerationActionType.NO_ACTION
