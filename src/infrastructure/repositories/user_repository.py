from domain.models.iuser_repository import IUserRepository
from domain.models.user import User
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config import Config
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from infrastructure.databases.base import Base
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.databases.mssql import session

load_dotenv()

class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    username = Column(String(18), nullable=False)
    password = Column(String(18), nullable=False)
    email = Column(String(255), nullable=True)
    status = Column(Boolean, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class UserRepository(BaseRepository[UserModel], IUserRepository):
    """
    User Repository implementation inheriting from BaseRepository
    """
    
    def __init__(self, session: Session = None):
        super().__init__(UserModel, session or session)
    
    def get_by_username(self, username: str) -> Optional[UserModel]:
        """Get user by username"""
        return self.find_one_by(username=username)
    
    def get_by_email(self, email: str) -> Optional[UserModel]:
        """Get user by email"""  
        return self.find_one_by(email=email)
    
    def exists_by_username(self, username: str) -> bool:
        """Check if user exists by username"""
        return self.find_one_by(username=username) is not None
    
    def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        return self.find_one_by(email=email) is not None
    
    def get_active_users(self) -> List[UserModel]:
        """Get all active users"""
        return self.find_by(status=True)
    
    def get_inactive_users(self) -> List[UserModel]:
        """Get all inactive users"""
        return self.find_by(status=False)
    
    def activate_user(self, user_id: int) -> bool:
        """Activate a user"""
        try:
            user = self.get_by_id(user_id)
            if user:
                user.status = True
                self.update(user)
                return True
            return False
        except Exception as e:
            raise ValueError(f'Error activating user: {str(e)}')
    
    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user"""
        try:
            user = self.get_by_id(user_id)
            if user:
                user.status = False
                self.update(user)
                return True
            return False
        except Exception as e:
            raise ValueError(f'Error deactivating user: {str(e)}')