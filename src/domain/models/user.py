from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(Enum):
    GUEST = "Guest"
    STUDENT = "Student"
    TUTOR = "Tutor"
    MODERATOR = "Moderator"
    ADMIN = "Admin"

class UserStatus(Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    PENDING = "Pending"

class User:
    def __init__(
        self, 
        id: Optional[int] = None,
        email: str = "", 
        password_hash: str = "", 
        role: UserRole = UserRole.GUEST,
        status: UserStatus = UserStatus.PENDING,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_status(self, status: UserStatus):
        self.status = status
        self.updated_at = datetime.utcnow()
    
    def update_role(self, role: UserRole):
        self.role = role
        self.updated_at = datetime.utcnow()
    
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE
    
    def can_tutor(self) -> bool:
        return self.role in [UserRole.TUTOR, UserRole.ADMIN]
    
    def can_moderate(self) -> bool:
        return self.role in [UserRole.MODERATOR, UserRole.ADMIN]