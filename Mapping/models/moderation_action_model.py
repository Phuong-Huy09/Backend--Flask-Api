from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class ModerationActionModel(Base):
    __tablename__ = 'moderation_actions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    complaint_id = Column(Integer, ForeignKey('complaints.id'), nullable=False)
    moderator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(Enum('Warn', 'Ban', 'Suspend', 'RemoveContent', 'Refund', 'NoAction', 
                         name='moderation_action_type'),
                    nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    complaint = relationship("ComplaintModel", back_populates="moderation_actions")
    moderator = relationship("UserModel", back_populates="moderation_actions")
    
    def __repr__(self):
        return f"<ModerationActionModel(id={self.id}, action='{self.action}', moderator_id={self.moderator_id})>"
