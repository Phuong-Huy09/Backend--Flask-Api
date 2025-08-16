from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.ireview_repository import IReviewRepository
from domain.models.review import Review
from infrastructure.models.review_model import ReviewModel
from infrastructure.repositories.base_repository import BaseRepository
from sqlalchemy import func

class ReviewRepository(BaseRepository[ReviewModel], IReviewRepository):
    """
    Review Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(ReviewModel, session)
    
    def _model_to_domain(self, model: ReviewModel) -> Review:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return Review(
            id=model.id,
            booking_id=model.booking_id,
            student_id=model.student_id,
            tutor_id=model.tutor_id,
            rating=model.rating,
            comment=model.comment,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: Review) -> ReviewModel:
        """Convert domain entity to SQLAlchemy model"""
        return ReviewModel(
            id=domain.id,
            booking_id=domain.booking_id,
            student_id=domain.student_id,
            tutor_id=domain.tutor_id,
            rating=domain.rating,
            comment=domain.comment,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, review: Review) -> Review:
        """Add a new review"""
        model = self._domain_to_model(review)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, review_id: int) -> Optional[Review]:
        """Get review by ID"""
        model = super().get_by_id(review_id)
        return self._model_to_domain(model)
    
    def get_by_booking_id(self, booking_id: int) -> Optional[Review]:
        """Get review by booking ID"""
        try:
            model = self.session.query(ReviewModel).filter_by(booking_id=booking_id).first()
            return self._model_to_domain(model)
        except Exception as e:
            raise ValueError(f'Error getting review by booking_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_tutor_id(self, tutor_id: int) -> List[Review]:
        """Get all reviews for a tutor"""
        try:
            models = self.session.query(ReviewModel).filter_by(tutor_id=tutor_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting reviews by tutor_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_student_id(self, student_id: int) -> List[Review]:
        """Get all reviews by a student"""
        try:
            models = self.session.query(ReviewModel).filter_by(student_id=student_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting reviews by student_id: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, review: Review) -> Review:
        """Update review"""
        try:
            model = self.session.query(ReviewModel).filter_by(id=review.id).first()
            if not model:
                raise ValueError(f'Review with id {review.id} not found')
            
            model.rating = review.rating
            model.comment = review.comment
            model.updated_at = review.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating review: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, review_id: int) -> bool:
        """Delete review"""
        return super().delete(review_id)
    
    def get_average_rating_for_tutor(self, tutor_id: int) -> float:
        """Get average rating for a tutor"""
        try:
            result = self.session.query(func.avg(ReviewModel.rating)).filter_by(tutor_id=tutor_id).scalar()
            return float(result) if result else 0.0
        except Exception as e:
            raise ValueError(f'Error getting average rating: {str(e)}')
        finally:
            self.session.close()
