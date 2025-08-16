from abc import ABC, abstractmethod
from typing import List, Optional
from ..chat_thread import ChatThread

class IChatThreadRepository(ABC):
    """
    Interface for Chat Thread Repository
    """
    
    @abstractmethod
    def add(self, chat_thread: ChatThread) -> ChatThread:
        """Add a new chat thread"""
        pass
    
    @abstractmethod
    def get_by_id(self, thread_id: int) -> Optional[ChatThread]:
        """Get chat thread by ID"""
        pass
    
    @abstractmethod
    def get_by_participants(self, student_id: int, tutor_id: int) -> Optional[ChatThread]:
        """Get chat thread by participants"""
        pass
    
    @abstractmethod
    def get_by_student_id(self, student_id: int) -> List[ChatThread]:
        """Get all chat threads for a student"""
        pass
    
    @abstractmethod
    def get_by_tutor_id(self, tutor_id: int) -> List[ChatThread]:
        """Get all chat threads for a tutor"""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> List[ChatThread]:
        """Get all chat threads for a user (student or tutor)"""
        pass
    
    @abstractmethod
    def update(self, chat_thread: ChatThread) -> ChatThread:
        """Update chat thread"""
        pass
    
    @abstractmethod
    def delete(self, thread_id: int) -> bool:
        """Delete chat thread"""
        pass
