from abc import ABC, abstractmethod
from typing import List, Optional
from ..message import Message

class IMessageRepository(ABC):
    """
    Interface for Message Repository
    """
    
    @abstractmethod
    def add(self, message: Message) -> Message:
        """Add a new message"""
        pass
    
    @abstractmethod
    def get_by_id(self, message_id: int) -> Optional[Message]:
        """Get message by ID"""
        pass
    
    @abstractmethod
    def get_by_thread_id(self, thread_id: int) -> List[Message]:
        """Get all messages in a thread"""
        pass
    
    @abstractmethod
    def get_by_sender_id(self, sender_id: int) -> List[Message]:
        """Get all messages by a sender"""
        pass
    
    @abstractmethod
    def get_latest_messages_in_thread(self, thread_id: int, limit: int = 50) -> List[Message]:
        """Get latest messages in a thread"""
        pass
    
    @abstractmethod
    def update(self, message: Message) -> Message:
        """Update message"""
        pass
    
    @abstractmethod
    def delete(self, message_id: int) -> bool:
        """Delete message"""
        pass
    
    @abstractmethod
    def count_messages_in_thread(self, thread_id: int) -> int:
        """Count messages in a thread"""
        pass
