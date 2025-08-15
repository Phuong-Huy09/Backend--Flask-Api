from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Type
from sqlalchemy.orm import Session
from infrastructure.databases.mssql import session, SessionLocal
from infrastructure.databases.base import Base

T = TypeVar('T', bound=Base)

class BaseRepository(Generic[T], ABC):
    """
    Base repository class providing common CRUD operations
    """
    
    def __init__(self, model_class: Type[T], session: Session = None):
        self.model_class = model_class
        self.session = session or SessionLocal()
    
    def add(self, entity: T) -> T:
        """
        Add a new entity to the database
        """
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error adding {self.model_class.__name__}: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """
        Get entity by ID
        """
        try:
            return self.session.query(self.model_class).filter_by(id=entity_id).first()
        except Exception as e:
            raise ValueError(f'Error getting {self.model_class.__name__} by id: {str(e)}')
        finally:
            self.session.close()
    
    def get_all(self) -> List[T]:
        """
        Get all entities
        """
        try:
            return self.session.query(self.model_class).all()
        except Exception as e:
            raise ValueError(f'Error getting all {self.model_class.__name__}: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, entity: T) -> T:
        """
        Update an existing entity
        """
        try:
            self.session.merge(entity)
            self.session.commit()
            return entity
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating {self.model_class.__name__}: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, entity_id: int) -> bool:
        """
        Delete an entity by ID
        """
        try:
            entity = self.session.query(self.model_class).filter_by(id=entity_id).first()
            if entity:
                self.session.delete(entity)
                self.session.commit()
                return True
            else:
                raise ValueError(f'{self.model_class.__name__} not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting {self.model_class.__name__}: {str(e)}')
        finally:
            self.session.close()
    
    def exists(self, entity_id: int) -> bool:
        """
        Check if entity exists by ID
        """
        try:
            return self.session.query(self.model_class).filter_by(id=entity_id).first() is not None
        except Exception as e:
            raise ValueError(f'Error checking if {self.model_class.__name__} exists: {str(e)}')
        finally:
            self.session.close()
    
    def count(self) -> int:
        """
        Count total number of entities
        """
        try:
            return self.session.query(self.model_class).count()
        except Exception as e:
            raise ValueError(f'Error counting {self.model_class.__name__}: {str(e)}')
        finally:
            self.session.close()
    
    def find_by(self, **kwargs) -> List[T]:
        """
        Find entities by specified criteria
        """
        try:
            query = self.session.query(self.model_class)
            for key, value in kwargs.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)
            return query.all()
        except Exception as e:
            raise ValueError(f'Error finding {self.model_class.__name__} by criteria: {str(e)}')
        finally:
            self.session.close()
    
    def find_one_by(self, **kwargs) -> Optional[T]:
        """
        Find one entity by specified criteria
        """
        try:
            query = self.session.query(self.model_class)
            for key, value in kwargs.items():
                if hasattr(self.model_class, key):
                    query = query.filter(getattr(self.model_class, key) == value)
            return query.first()
        except Exception as e:
            raise ValueError(f'Error finding {self.model_class.__name__} by criteria: {str(e)}')
        finally:
            self.session.close()
