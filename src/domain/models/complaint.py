from typing import Optional
from datetime import datetime
from enum import Enum

class ComplaintType(Enum):
    CONTENT = "Content"
    BEHAVIOR = "Behavior"
    PAYMENT = "Payment"
    OTHER = "Other"

class ComplaintStatus(Enum):
    OPEN = "Open"
    UNDER_REVIEW = "UnderReview"
    RESOLVED = "Resolved"
    REJECTED = "Rejected"

class Complaint:
    def __init__(
        self,
        id: Optional[int] = None,
        raised_by_user: int = 0,
        against_user: int = 0,
        booking_id: Optional[int] = None,
        type: ComplaintType = ComplaintType.OTHER,
        detail: str = "",
        status: ComplaintStatus = ComplaintStatus.OPEN,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.raised_by_user = raised_by_user
        self.against_user = against_user
        self.booking_id = booking_id
        self.type = type
        self.detail = detail
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_status(self, status: ComplaintStatus):
        """Update complaint status"""
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def resolve(self):
        """Resolve the complaint"""
        self.status = ComplaintStatus.RESOLVED
        self.updated_at = datetime.utcnow()
    
    def reject(self):
        """Reject the complaint"""
        self.status = ComplaintStatus.REJECTED
        self.updated_at = datetime.utcnow()
    
    def start_review(self):
        """Start reviewing the complaint"""
        self.status = ComplaintStatus.UNDER_REVIEW
        self.updated_at = datetime.utcnow()
    
    def is_open(self) -> bool:
        """Check if complaint is open"""
        return self.status == ComplaintStatus.OPEN
    
    def is_resolved(self) -> bool:
        """Check if complaint is resolved"""
        return self.status == ComplaintStatus.RESOLVED
