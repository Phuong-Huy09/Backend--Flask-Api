from typing import Optional
from datetime import datetime

class Review:
    def __init__(
        self,
        id: Optional[int] = None,
        booking_id: int = 0,
        student_id: int = 0,
        tutor_id: int = 0,
        rating: int = 1,
        comment: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.booking_id = booking_id
        self.student_id = student_id
        self.tutor_id = tutor_id
        self.rating = self._validate_rating(rating)
        self.comment = comment
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def _validate_rating(self, rating: int) -> int:
        """Validate rating is between 1 and 5"""
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    def update_rating(self, rating: int):
        """Update review rating"""
        self.rating = self._validate_rating(rating)
        self.updated_at = datetime.utcnow()
    
    def update_comment(self, comment: str):
        """Update review comment"""
        self.comment = comment
        self.updated_at = datetime.utcnow()
    
    def is_positive(self) -> bool:
        """Check if review is positive (rating >= 4)"""
        return self.rating >= 4
    
    def is_negative(self) -> bool:
        """Check if review is negative (rating <= 2)"""
        return self.rating <= 2
