from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class ChatThreadModel(Base):
    __tablename__ = 'chat_threads'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student_profiles.user_id'), nullable=False)
    tutor_id = Column(Integer, ForeignKey('tutor_profiles.user_id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student = relationship("StudentProfileModel", back_populates="chat_threads")
    tutor = relationship("TutorProfileModel", back_populates="chat_threads")
    messages = relationship("MessageModel", back_populates="thread")
    
    def __repr__(self):
        return f"<ChatThreadModel(id={self.id}, student_id={self.student_id}, tutor_id={self.tutor_id})>"
