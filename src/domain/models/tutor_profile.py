from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum

class VerificationStatus(Enum):
    UNVERIFIED = "Unverified"
    PENDING = "Pending"
    VERIFIED = "Verified"
    REJECTED = "Rejected"

class TutorProfile:
    def __init__(
        self,
        user_id: int,
        full_name: str,
        bio: str,
        years_experience: int = 0,
        hourly_rate: Decimal = Decimal('0.00'),
        verification_status: VerificationStatus = VerificationStatus.UNVERIFIED,
        rating_avg: Decimal = Decimal('0.00'),
        rating_count: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.full_name = full_name
        self.bio = bio
        self.years_experience = years_experience
        self.hourly_rate = hourly_rate
        self.verification_status = verification_status
        self.rating_avg = rating_avg
        self.rating_count = rating_count
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_rating(self, new_rating: int):
        """Update average rating when a new review is added"""
        total_points = self.rating_avg * self.rating_count + new_rating
        self.rating_count += 1
        self.rating_avg = Decimal(str(total_points / self.rating_count))
        self.updated_at = datetime.utcnow()
    
    def update_verification_status(self, status: VerificationStatus):
        self.verification_status = status
        self.updated_at = datetime.utcnow()
    
    def is_verified(self) -> bool:
        return self.verification_status == VerificationStatus.VERIFIED
    
    def can_accept_bookings(self) -> bool:
        return self.verification_status == VerificationStatus.VERIFIED
