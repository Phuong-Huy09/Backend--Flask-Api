from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.orm import Session
from infrastructure.databases.mssql import SessionLocal
from infrastructure.databases.base import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T], ABC):
    """
    Base repository class providing common CRUD operations
    """

    def __init__(self, model_class: Type[T], session: Optional[Session] = None):
        """
        Initialize repository with model class and optional session
        If no session provided, creates a new one
        """
        self.model_class = model_class
        if session is not None:
            self.session = session
            self._owns_session = False  # External session, don't close it
        else:
            self.session = SessionLocal()
            self._owns_session = True   # Own the session, should close it

    def add(self, entity: T) -> T:
        """Add a new entity to the database"""
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error adding {self.model_class.__name__}: {str(e)}')
        finally:
            if self._owns_session:
                self.session.close()

    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID"""
        try:
            return self.session.query(self.model_class).filter(
                self.model_class.id == id
            ).first()
        except Exception as e:
            raise ValueError(f'Error getting {self.model_class.__name__} by ID: {str(e)}')
        finally:
            if self._owns_session:
                self.session.close()

    def get_all(self) -> List[T]:
        """Get all entities"""
        try:
            return self.session.query(self.model_class).all()
        except Exception as e:
            raise ValueError(f'Error getting all {self.model_class.__name__}: {str(e)}')
        finally:
            if self._owns_session:
                self.session.close()

    def update(self, entity: T) -> T:
        """Update an existing entity"""
        try:
            self.session.merge(entity)
            self.session.commit()
            return entity
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating {self.model_class.__name__}: {str(e)}')
        finally:
            if self._owns_session:
                self.session.close()

    def delete(self, id: int) -> bool:
        """Delete an entity by ID"""
        try:
            entity = self.session.query(self.model_class).filter(
                self.model_class.id == id
            ).first()
            if entity:
                self.session.delete(entity)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting {self.model_class.__name__}: {str(e)}')
        finally:
            if self._owns_session:
                self.session.close()

    def exists(self, id: int) -> bool:
        """Check if entity exists by ID"""
        try:
            return self.session.query(self.model_class).filter(
                self.model_class.id == id
            ).first() is not None
        except Exception as e:
            raise ValueError(f'Error checking {self.model_class.__name__} existence: {str(e)}')
        finally:
            if self._owns_session:
                self.session.close()

    def count(self) -> int:
        """Count total entities"""
        try:
            return self.session.query(self.model_class).count()
        except Exception as e:
            raise ValueError(f'Error counting {self.model_class.__name__}: {str(e)}')
        finally:
            if self._owns_session:
                self.session.close()

    def find_by(self, **kwargs) -> List[T]:
        """Find entities by arbitrary criteria"""
        try:
            query = self.session.query(self.model_class)
            for key, value in kwargs.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)
            return query.all()
        except Exception as e:
            raise ValueError(f'Error finding {self.model_class.__name__}: {str(e)}')
        finally:
            if self._owns_session:
                self.session.close()

    def find_one_by(self, **kwargs) -> Optional[T]:
        """Find single entity by arbitrary criteria"""
        try:
            query = self.session.query(self.model_class)
            for key, value in kwargs.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)
            return query.first()
        except Exception as e:
            raise ValueError(f'Error finding {self.model_class.__name__}: {str(e)}')
        finally:
            if self._owns_session:
                self.session.close()

    @abstractmethod
    def _model_to_domain(self, model: T) -> object:
        """Convert infrastructure model to domain entity"""
        pass

    @abstractmethod
    def _domain_to_model(self, domain_entity: object) -> T:
        """Convert domain entity to infrastructure model"""
        pass
