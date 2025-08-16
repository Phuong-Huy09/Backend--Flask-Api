from typing import Optional
from datetime import datetime
from decimal import Decimal

class ServiceListing:
    def __init__(
        self,
        id: Optional[int] = None,
        tutor_id: int = 0,
        title: str = "",
        description: str = "",
        price_per_hour: Decimal = Decimal('0.00'),
        active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.tutor_id = tutor_id
        self.title = title
        self.description = description
        self.price_per_hour = price_per_hour
        self.active = active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_title(self, title: str):
        """Update service listing title"""
        self.title = title
        self.updated_at = datetime.utcnow()
    
    def update_description(self, description: str):
        """Update service listing description"""
        self.description = description
        self.updated_at = datetime.utcnow()
    
    def update_price(self, price_per_hour: Decimal):
        """Update service listing price per hour"""
        if price_per_hour < 0:
            raise ValueError("Price per hour cannot be negative")
        self.price_per_hour = price_per_hour
        self.updated_at = datetime.utcnow()
    
    def activate(self):
        """Activate the service listing"""
        self.active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self):
        """Deactivate the service listing"""
        self.active = False
        self.updated_at = datetime.utcnow()
    
    def is_active(self) -> bool:
        """Check if service listing is active"""
        return self.active
