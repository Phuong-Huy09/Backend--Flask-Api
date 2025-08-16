from domain.models.interfaces.iuser_repository import IUserRepository
from domain.models.user import User, UserRole, UserStatus
from infrastructure.models.user_model import UserModel
from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[UserModel], IUserRepository):
    """
    User Repository implementation inheriting from BaseRepository
    """
    
    def __init__(self, session: Session = None):
        super().__init__(UserModel, session)
    
    def _model_to_domain(self, model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            role=UserRole(model.role.value),
            status=UserStatus(model.status.value),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: User) -> UserModel:
        """Convert domain entity to SQLAlchemy model"""
        return UserModel(
            id=domain.id,
            email=domain.email,
            password_hash=domain.password_hash,
            role=domain.role.value,
            status=domain.status.value,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, user: User) -> User:
        """Add a new user"""
        model = self._domain_to_model(user)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        model = super().get_by_id(user_id)
        return self._model_to_domain(model)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username - legacy method, now uses email"""
        return self.get_by_email(username)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            model = self.session.query(UserModel).filter_by(email=email).first()
            return self._model_to_domain(model)
        except Exception as e:
            raise ValueError(f'Error getting user by email: {str(e)}')
        finally:
            self.session.close()
    
    def get_all(self) -> List[User]:
        """Get all users"""
        models = super().get_all()
        return [self._model_to_domain(model) for model in models]
    
    def update(self, user: User) -> User:
        """Update user"""
        try:
            model = self.session.query(UserModel).filter_by(id=user.id).first()
            if not model:
                raise ValueError(f'User with id {user.id} not found')
            
            model.email = user.email
            model.password_hash = user.password_hash
            model.role = user.role.value
            model.status = user.status.value
            model.updated_at = user.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating user: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, user_id: int) -> bool:
        """Delete user"""
        return super().delete(user_id)
    
    def exists_by_username(self, username: str) -> bool:
        """Check if user exists by username"""
        return self.get_by_email(username) is not None
    
    def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        return self.get_by_email(email) is not None
    
    def get_by_role(self, role: UserRole) -> List[User]:
        """Get users by role"""
        try:
            models = self.session.query(UserModel).filter_by(role=role.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting users by role: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_status(self, status: UserStatus) -> List[User]:
        """Get users by status"""
        try:
            models = self.session.query(UserModel).filter_by(status=status.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting users by status: {str(e)}')
        finally:
            self.session.close()
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