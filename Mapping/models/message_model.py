from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from infrastructure.databases.base import Base

class MessageModel(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_id = Column(Integer, ForeignKey('chat_threads.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    body = Column(Text, nullable=False)
    attachment_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    thread = relationship("ChatThreadModel", back_populates="messages")
    sender = relationship("UserModel", back_populates="messages")
    
    def __repr__(self):
        return f"<MessageModel(id={self.id}, sender_id={self.sender_id}, thread_id={self.thread_id})>"
