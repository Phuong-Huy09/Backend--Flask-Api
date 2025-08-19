from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class UserModel(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('Guest', 'Student', 'Tutor', 'Moderator', 'Admin', name='user_role'), 
                  nullable=False, default='Guest')
    status = Column(Enum('Active', 'Suspended', 'Pending', name='user_status'), 
                    nullable=False, default='Pending')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student_profile = relationship("StudentProfileModel", back_populates="user", uselist=False)
    tutor_profile = relationship("TutorProfileModel", back_populates="user", uselist=False)
    
    # Messages sent by this user
    messages = relationship("MessageModel", back_populates="sender")
    
    # Notifications for this user
    notifications = relationship("NotificationModel", back_populates="user")
    
    # Complaints raised by this user
    complaints_raised = relationship("ComplaintModel", 
                                   foreign_keys="[ComplaintModel.raised_by_user]",
                                   back_populates="raised_by")
    
    # Complaints against this user
    complaints_against = relationship("ComplaintModel", 
                                    foreign_keys="[ComplaintModel.against_user]",
                                    back_populates="against")
    
    # Moderation actions performed by this user (if moderator)
    moderation_actions = relationship("ModerationActionModel", back_populates="moderator")
    
    def __repr__(self):
        return f"<UserModel(id={self.id}, email='{self.email}', role='{self.role}', status='{self.status}')>" 