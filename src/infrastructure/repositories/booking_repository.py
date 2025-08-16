from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.ibooking_repository import IBookingRepository
from domain.models.booking import Booking, BookingStatus
from infrastructure.models.booking_model import BookingModel
from infrastructure.repositories.base_repository import BaseRepository
from datetime import datetime
from decimal import Decimal

class BookingRepository(BaseRepository[BookingModel], IBookingRepository):
    """
    Booking Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(BookingModel, session)
    
    def _model_to_domain(self, model: BookingModel) -> Booking:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return Booking(
            id=model.id,
            student_id=model.student_id,
            tutor_id=model.tutor_id,
            service_id=model.service_id,
            subject_id=model.subject_id,
            start_at=model.start_at,
            end_at=model.end_at,
            hours=Decimal(str(model.hours)),
            status=BookingStatus(model.status.value),
            total_amount=Decimal(str(model.total_amount)),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: Booking) -> BookingModel:
        """Convert domain entity to SQLAlchemy model"""
        return BookingModel(
            id=domain.id,
            student_id=domain.student_id,
            tutor_id=domain.tutor_id,
            service_id=domain.service_id,
            subject_id=domain.subject_id,
            start_at=domain.start_at,
            end_at=domain.end_at,
            hours=domain.hours,
            status=domain.status.value,
            total_amount=domain.total_amount,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, booking: Booking) -> Booking:
        """Add a new booking"""
        model = self._domain_to_model(booking)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        """Get booking by ID"""
        model = super().get_by_id(booking_id)
        return self._model_to_domain(model)
    
    def get_by_student_id(self, student_id: int) -> List[Booking]:
        """Get all bookings for a student"""
        try:
            models = self.session.query(BookingModel).filter_by(student_id=student_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting bookings by student_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_tutor_id(self, tutor_id: int) -> List[Booking]:
        """Get all bookings for a tutor"""
        try:
            models = self.session.query(BookingModel).filter_by(tutor_id=tutor_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting bookings by tutor_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_status(self, status: BookingStatus) -> List[Booking]:
        """Get bookings by status"""
        try:
            models = self.session.query(BookingModel).filter_by(status=status.value).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting bookings by status: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Booking]:
        """Get bookings within a date range"""
        try:
            models = self.session.query(BookingModel).filter(
                BookingModel.start_at >= start_date,
                BookingModel.end_at <= end_date
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting bookings by date range: {str(e)}')
        finally:
            self.session.close()
    
    def get_upcoming_bookings(self, user_id: int) -> List[Booking]:
        """Get upcoming bookings for a user"""
        try:
            now = datetime.utcnow()
            models = self.session.query(BookingModel).filter(
                (BookingModel.student_id == user_id) | (BookingModel.tutor_id == user_id),
                BookingModel.start_at > now,
                BookingModel.status.in_(['Confirmed', 'Pending'])
            ).order_by(BookingModel.start_at).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting upcoming bookings: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, booking: Booking) -> Booking:
        """Update booking"""
        try:
            model = self.session.query(BookingModel).filter_by(id=booking.id).first()
            if not model:
                raise ValueError(f'Booking with id {booking.id} not found')
            
            model.start_at = booking.start_at
            model.end_at = booking.end_at
            model.hours = booking.hours
            model.status = booking.status.value
            model.total_amount = booking.total_amount
            model.updated_at = booking.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating booking: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, booking_id: int) -> bool:
        """Delete booking"""
        return super().delete(booking_id)
