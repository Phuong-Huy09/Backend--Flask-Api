from typing import Optional
from datetime import datetime
from enum import Enum

class SubjectLevel(Enum):
    K12 = "K12"
    UNDERGRAD = "Undergrad"
    GRADUATE = "Graduate"
    OTHER = "Other"

class Subject:
    def __init__(
        self,
        id: Optional[int] = None,
        name: str = "",
        level: SubjectLevel = SubjectLevel.OTHER,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.level = level
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_name(self, name: str):
        self.name = name
        self.updated_at = datetime.utcnow()
    
    def update_level(self, level: SubjectLevel):
        self.level = level
        self.updated_at = datetime.utcnow()
