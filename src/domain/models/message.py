from typing import Optional
from datetime import datetime

class Message:
    def __init__(
        self,
        id: Optional[int] = None,
        thread_id: int = 0,
        sender_id: int = 0,
        body: str = "",
        attachment_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.thread_id = thread_id
        self.sender_id = sender_id
        self.body = body
        self.attachment_url = attachment_url
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_body(self, body: str):
        """Update message body"""
        self.body = body
        self.updated_at = datetime.utcnow()
    
    def add_attachment(self, attachment_url: str):
        """Add attachment to message"""
        self.attachment_url = attachment_url
        self.updated_at = datetime.utcnow()
    
    def remove_attachment(self):
        """Remove attachment from message"""
        self.attachment_url = None
        self.updated_at = datetime.utcnow()
    
    def has_attachment(self) -> bool:
        """Check if message has attachment"""
        return self.attachment_url is not None and self.attachment_url.strip() != ""
