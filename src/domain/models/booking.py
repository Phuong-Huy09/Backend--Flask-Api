from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

class BookingStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    CANCELED = "Canceled"
    REFUNDED = "Refunded"

class Booking:
    def __init__(
        self,
        id: Optional[int] = None,
        student_id: int = 0,
        tutor_id: int = 0,
        service_id: int = 0,
        subject_id: int = 0,
        start_at: Optional[datetime] = None,
        end_at: Optional[datetime] = None,
        hours: Decimal = Decimal('0.0'),
        total_amount: Decimal = Decimal('0.0'),
        status: BookingStatus = BookingStatus.PENDING,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.student_id = student_id
        self.tutor_id = tutor_id
        self.service_id = service_id
        self.subject_id = subject_id
        self.start_at = start_at
        self.end_at = end_at
        self.hours = hours
        self.status = status
        self.total_amount = total_amount
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_status(self, status: BookingStatus):
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def can_be_canceled(self) -> bool:
        return self.status in [BookingStatus.PENDING, BookingStatus.CONFIRMED]
    
    def is_completed(self) -> bool:
        return self.status == BookingStatus.COMPLETED
    
    def calculate_duration_hours(self) -> Decimal:
        duration = self.end_at - self.start_at
        return Decimal(str(duration.total_seconds() / 3600))
