from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.itutor_subject_repository import ITutorSubjectRepository
from domain.models.tutor_subject import TutorSubject
from infrastructure.models.tutor_subject_model import TutorSubjectModel
from infrastructure.repositories.base_repository import BaseRepository

class TutorSubjectRepository(BaseRepository[TutorSubjectModel], ITutorSubjectRepository):
    """
    Tutor Subject Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(TutorSubjectModel, session)
    
    def _model_to_domain(self, model: TutorSubjectModel) -> TutorSubject:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return TutorSubject(
            tutor_id=model.tutor_id,
            subject_id=model.subject_id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: TutorSubject) -> TutorSubjectModel:
        """Convert domain entity to SQLAlchemy model"""
        return TutorSubjectModel(
            tutor_id=domain.tutor_id,
            subject_id=domain.subject_id,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, tutor_subject: TutorSubject) -> TutorSubject:
        """Add a new tutor subject"""
        model = self._domain_to_model(tutor_subject)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_tutor_id(self, tutor_id: int) -> List[TutorSubject]:
        """Get all subjects for a tutor"""
        try:
            models = self.session.query(TutorSubjectModel).filter_by(tutor_id=tutor_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting tutor subjects by tutor_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_subject_id(self, subject_id: int) -> List[TutorSubject]:
        """Get all tutors for a subject"""
        try:
            models = self.session.query(TutorSubjectModel).filter_by(subject_id=subject_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting tutor subjects by subject_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_tutor_and_subject(self, tutor_id: int, subject_id: int) -> Optional[TutorSubject]:
        """Get tutor subject by tutor and subject ID"""
        try:
            model = self.session.query(TutorSubjectModel).filter_by(
                tutor_id=tutor_id, subject_id=subject_id
            ).first()
            return self._model_to_domain(model)
        except Exception as e:
            raise ValueError(f'Error getting tutor subject by tutor and subject: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, tutor_subject: TutorSubject) -> TutorSubject:
        """Update tutor subject"""
        try:
            model = self.session.query(TutorSubjectModel).filter_by(
                tutor_id=tutor_subject.tutor_id, 
                subject_id=tutor_subject.subject_id
            ).first()
            if not model:
                raise ValueError(f'Tutor subject not found')
            
            model.updated_at = tutor_subject.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating tutor subject: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, tutor_id: int, subject_id: int) -> bool:
        """Delete tutor subject"""
        try:
            model = self.session.query(TutorSubjectModel).filter_by(
                tutor_id=tutor_id, subject_id=subject_id
            ).first()
            if not model:
                return False
            
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting tutor subject: {str(e)}')
        finally:
            self.session.close()
    
    def delete_by_tutor_id(self, tutor_id: int) -> bool:
        """Delete all subjects for a tutor"""
        try:
            models = self.session.query(TutorSubjectModel).filter_by(tutor_id=tutor_id).all()
            for model in models:
                self.session.delete(model)
            
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting tutor subjects: {str(e)}')
        finally:
            self.session.close()
