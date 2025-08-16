from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.itutor_profile_repository import ITutorProfileRepository
from domain.models.tutor_profile import TutorProfile, VerificationStatus
from infrastructure.models.tutor_profile_model import TutorProfileModel
from infrastructure.repositories.base_repository import BaseRepository
from decimal import Decimal

class TutorProfileRepository(BaseRepository[TutorProfileModel], ITutorProfileRepository):
    """
    Tutor Profile Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(TutorProfileModel, session)
    
    def _model_to_domain(self, model: TutorProfileModel) -> TutorProfile:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return TutorProfile(
            user_id=model.user_id,
            full_name=model.full_name,
            bio=model.bio,
            years_experience=model.years_experience,
            hourly_rate=Decimal(str(model.hourly_rate)),
            verification_status=VerificationStatus(model.verification_status.value) if hasattr(model.verification_status, 'value') else VerificationStatus(model.verification_status),
            rating_avg=float(model.rating_avg),
            rating_count=model.rating_count,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: TutorProfile) -> TutorProfileModel:
        """Convert domain entity to SQLAlchemy model"""
        return TutorProfileModel(
            user_id=domain.user_id,
            full_name=domain.full_name,
            bio=domain.bio,
            years_experience=domain.years_experience,
            hourly_rate=domain.hourly_rate,
            verification_status=domain.verification_status.value,
            rating_avg=domain.rating_avg,
            rating_count=domain.rating_count,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, tutor_profile: TutorProfile) -> TutorProfile:
        """Add a new tutor profile"""
        model = self._domain_to_model(tutor_profile)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_user_id(self, user_id: int) -> Optional[TutorProfile]:
        """Get tutor profile by user ID"""
        try:
            model = self.session.query(TutorProfileModel).filter_by(user_id=user_id).first()
            return self._model_to_domain(model)
        except Exception as e:
            raise ValueError(f'Error getting tutor profile by user_id: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, tutor_profile: TutorProfile) -> TutorProfile:
        """Update tutor profile"""
        try:
            model = self.session.query(TutorProfileModel).filter_by(user_id=tutor_profile.user_id).first()
            if not model:
                raise ValueError(f'Tutor profile with user_id {tutor_profile.user_id} not found')
            
            model.full_name = tutor_profile.full_name
            model.bio = tutor_profile.bio
            model.years_experience = tutor_profile.years_experience
            model.hourly_rate = tutor_profile.hourly_rate
            model.verification_status = tutor_profile.verification_status.value
            model.rating_avg = tutor_profile.rating_avg
            model.rating_count = tutor_profile.rating_count
            model.updated_at = tutor_profile.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating tutor profile: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, user_id: int) -> bool:
        """Delete tutor profile"""
        try:
            model = self.session.query(TutorProfileModel).filter_by(user_id=user_id).first()
            if not model:
                return False
            
            self.session.delete(model)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting tutor profile: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_verification_status(self, status: VerificationStatus) -> List[TutorProfile]:
        """Get tutor profiles by verification status"""
        try:
            models = self.session.query(TutorProfileModel).filter_by(verification_status=status.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting tutor profiles by verification status: {str(e)}')
        finally:
            self.session.close()
    
    def search_by_name(self, name: str) -> List[TutorProfile]:
        """Search tutor profiles by name"""
        try:
            models = self.session.query(TutorProfileModel).filter(
                TutorProfileModel.full_name.like(f'%{name}%')
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error searching tutor profiles by name: {str(e)}')
        finally:
            self.session.close()
    
    def get_verified_tutors(self) -> List[TutorProfile]:
        """Get all verified tutors"""
        return self.get_by_verification_status(VerificationStatus.VERIFIED)
    
    def get_by_rating_range(self, min_rating: float, max_rating: float) -> List[TutorProfile]:
        """Get tutors by rating range"""
        try:
            models = self.session.query(TutorProfileModel).filter(
                TutorProfileModel.rating_avg >= min_rating,
                TutorProfileModel.rating_avg <= max_rating
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting tutors by rating range: {str(e)}')
        finally:
            self.session.close()
