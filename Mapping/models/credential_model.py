from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class CredentialModel(Base):
    __tablename__ = 'credentials'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tutor_id = Column(Integer, ForeignKey('tutor_profiles.user_id'), nullable=False)
    type = Column(Enum('Degree', 'Certificate', 'ID', 'Transcript', 'Other', name='credential_type'),
                  nullable=False)
    issuer = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tutor = relationship("TutorProfileModel", back_populates="credentials")
    
    def __repr__(self):
        return f"<CredentialModel(id={self.id}, type='{self.type}', tutor_id={self.tutor_id})>"
