from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class TutorSubjectModel(Base):
    __tablename__ = 'tutor_subjects'
    
    tutor_id = Column(Integer, ForeignKey('tutor_profiles.user_id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    tutor = relationship("TutorProfileModel", back_populates="tutor_subjects")
    subject = relationship("SubjectModel", back_populates="tutor_subjects")
    
    def __repr__(self):
        return f"<TutorSubjectModel(tutor_id={self.tutor_id}, subject_id={self.subject_id})>"
