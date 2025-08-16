from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.istudent_profile_repository import IStudentProfileRepository
from domain.models.student_profile import StudentProfile
from infrastructure.models.student_profile_model import StudentProfileModel
from infrastructure.repositories.base_repository import BaseRepository

class StudentProfileRepository(BaseRepository[StudentProfileModel], IStudentProfileRepository):
    """
    Student Profile Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(StudentProfileModel, session)
    
    def _model_to_domain(self, model: StudentProfileModel) -> StudentProfile:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return StudentProfile(
            user_id=model.user_id,
            full_name=model.full_name,
            dob=model.dob,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: StudentProfile) -> StudentProfileModel:
        """Convert domain entity to SQLAlchemy model"""
        return StudentProfileModel(
            user_id=domain.user_id,
            full_name=domain.full_name,
            dob=domain.dob,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, student_profile: StudentProfile) -> StudentProfile:
        """Add a new student profile"""
        model = self._domain_to_model(student_profile)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_user_id(self, user_id: int) -> Optional[StudentProfile]:
        """Get student profile by user ID"""
        try:
            model = self.session.query(StudentProfileModel).filter_by(user_id=user_id).first()
            return self._model_to_domain(model)
        except Exception as e:
            raise ValueError(f'Error getting student profile by user_id: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, student_profile: StudentProfile) -> StudentProfile:
        """Update student profile"""
        try:
            model = self.session.query(StudentProfileModel).filter_by(user_id=student_profile.user_id).first()
            if not model:
                raise ValueError(f'Student profile with user_id {student_profile.user_id} not found')
            
            model.full_name = student_profile.full_name
            model.dob = student_profile.dob
            model.updated_at = student_profile.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating student profile: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, user_id: int) -> bool:
        """Delete student profile"""
        try:
            model = self.session.query(StudentProfileModel).filter_by(user_id=user_id).first()
            if not model:
                return False
            
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting student profile: {str(e)}')
        finally:
            self.session.close()
    
    def search_by_name(self, name: str) -> List[StudentProfile]:
        """Search student profiles by name"""
        try:
            models = self.session.query(StudentProfileModel).filter(
                StudentProfileModel.full_name.like(f'%{name}%')
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error searching student profiles by name: {str(e)}')
        finally:
            self.session.close()
    
    def get_all(self) -> List[StudentProfile]:
        """Get all student profiles"""
        models = super().get_all()
        return [self._model_to_domain(model) for model in models]
