from abc import ABC, abstractmethod
from typing import List, Optional
from ..moderation_action import ModerationAction

class IModerationActionRepository(ABC):
    """
    Interface for Moderation Action Repository
    """
    
    @abstractmethod
    def add(self, moderation_action: ModerationAction) -> ModerationAction:
        """Add a new moderation action"""
        pass
    
    @abstractmethod
    def get_by_id(self, action_id: int) -> Optional[ModerationAction]:
        """Get moderation action by ID"""
        pass
    
    @abstractmethod
    def get_by_complaint_id(self, complaint_id: int) -> List[ModerationAction]:
        """Get all moderation actions for a complaint"""
        pass
    
    @abstractmethod
    def get_by_moderator_id(self, moderator_id: int) -> List[ModerationAction]:
        """Get all moderation actions by a moderator"""
        pass
    
    @abstractmethod
    def update(self, moderation_action: ModerationAction) -> ModerationAction:
        """Update moderation action"""
        pass
    
    @abstractmethod
    def delete(self, action_id: int) -> bool:
        """Delete moderation action"""
        pass
