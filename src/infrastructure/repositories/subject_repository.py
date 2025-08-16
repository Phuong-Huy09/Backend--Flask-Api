from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.isubject_repository import ISubjectRepository
from domain.models.subject import Subject, SubjectLevel
from infrastructure.models.subject_model import SubjectModel
from infrastructure.repositories.base_repository import BaseRepository

class SubjectRepository(BaseRepository[SubjectModel], ISubjectRepository):
    """
    Subject Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(SubjectModel, session)
    
    def _model_to_domain(self, model: SubjectModel) -> Subject:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        # Handle enum conversion - model.level might already be SubjectLevel enum
        level = model.level if isinstance(model.level, SubjectLevel) else SubjectLevel(model.level)
        
        return Subject(
            id=model.id,
            name=model.name,
            level=level,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: Subject) -> SubjectModel:
        """Convert domain entity to SQLAlchemy model"""
        return SubjectModel(
            id=domain.id,
            name=domain.name,
            level=domain.level.value,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, subject: Subject) -> Subject:
        """Add a new subject"""
        model = self._domain_to_model(subject)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, subject_id: int) -> Optional[Subject]:
        """Get subject by ID"""
        model = super().get_by_id(subject_id)
        return self._model_to_domain(model)
    
    def get_by_name(self, name: str) -> Optional[Subject]:
        """Get subject by name"""
        try:
            model = self.session.query(SubjectModel).filter_by(name=name).first()
            return self._model_to_domain(model)
        except Exception as e:
            raise ValueError(f'Error getting subject by name: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_level(self, level: SubjectLevel) -> List[Subject]:
        """Get subjects by level"""
        try:
            models = self.session.query(SubjectModel).filter_by(level=level.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting subjects by level: {str(e)}')
        finally:
            self.session.close()
    
    def get_all(self) -> List[Subject]:
        """Get all subjects"""
        models = super().get_all()
        return [self._model_to_domain(model) for model in models]
    
    def update(self, subject: Subject) -> Subject:
        """Update subject"""
        try:
            model = self.session.query(SubjectModel).filter_by(id=subject.id).first()
            if not model:
                raise ValueError(f'Subject with id {subject.id} not found')
            
            model.name = subject.name
            model.level = subject.level.value
            model.updated_at = subject.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating subject: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, subject_id: int) -> bool:
        """Delete subject"""
        return super().delete(subject_id)
    
    def search_by_name(self, name: str) -> List[Subject]:
        """Search subjects by name pattern"""
        try:
            models = self.session.query(SubjectModel).filter(
                SubjectModel.name.like(f'%{name}%')
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error searching subjects by name: {str(e)}')
        finally:
            self.session.close()
