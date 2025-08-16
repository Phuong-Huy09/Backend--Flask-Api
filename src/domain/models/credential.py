from typing import Optional
from datetime import datetime
from enum import Enum

class CredentialType(Enum):
    DEGREE = "Degree"
    CERTIFICATE = "Certificate"
    ID = "ID"
    TRANSCRIPT = "Transcript"
    OTHER = "Other"

class Credential:
    def __init__(
        self,
        id: Optional[int] = None,
        tutor_id: int = 0,
        type: CredentialType = CredentialType.OTHER,
        issuer: str = "",
        file_url: str = "",
        verified: bool = False,
        verified_at: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.tutor_id = tutor_id
        self.type = type
        self.issuer = issuer
        self.file_url = file_url
        self.verified = verified
        self.verified_at = verified_at
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def verify(self):
        """Mark credential as verified"""
        self.verified = True
        self.verified_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def update_file_url(self, file_url: str):
        """Update credential file URL"""
        self.file_url = file_url
        self.updated_at = datetime.utcnow()
    
    def update_issuer(self, issuer: str):
        """Update credential issuer"""
        self.issuer = issuer
        self.updated_at = datetime.utcnow()
    
    def is_verified(self) -> bool:
        """Check if credential is verified"""
        return self.verified
