from abc import ABC, abstractmethod
from typing import List, Optional
from ..user import User

class IUserRepository(ABC):
    """
    Interface for User Repository
    """
    
    @abstractmethod
    def add(self, user: User) -> User:
        """Add a new user"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[User]:
        """Get all users"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Update user"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user by ID"""
        pass
    
    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        """Check if user exists by username"""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        pass
