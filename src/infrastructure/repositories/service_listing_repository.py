from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.iservice_listing_repository import IServiceListingRepository
from domain.models.service_listing import ServiceListing
from infrastructure.models.service_listing_model import ServiceListingModel
from infrastructure.repositories.base_repository import BaseRepository
from decimal import Decimal

class ServiceListingRepository(BaseRepository[ServiceListingModel], IServiceListingRepository):
    """
    Service Listing Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(ServiceListingModel, session)
    
    def _model_to_domain(self, model: ServiceListingModel) -> ServiceListing:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return ServiceListing(
            id=model.id,
            tutor_id=model.tutor_id,
            title=model.title,
            description=model.description,
            price_per_hour=Decimal(str(model.price_per_hour)),
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: ServiceListing) -> ServiceListingModel:
        """Convert domain entity to SQLAlchemy model"""
        return ServiceListingModel(
            id=domain.id,
            tutor_id=domain.tutor_id,
            title=domain.title,
            description=domain.description,
            price_per_hour=domain.price_per_hour,
            active=domain.active,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, service_listing: ServiceListing) -> ServiceListing:
        """Add a new service listing"""
        model = self._domain_to_model(service_listing)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, service_id: int) -> Optional[ServiceListing]:
        """Get service listing by ID"""
        model = super().get_by_id(service_id)
        return self._model_to_domain(model)
    
    def get_by_tutor_id(self, tutor_id: int) -> List[ServiceListing]:
        """Get all service listings for a tutor"""
        try:
            models = self.session.query(ServiceListingModel).filter_by(tutor_id=tutor_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting service listings by tutor_id: {str(e)}')
        finally:
            self.session.close()
    
    def get_active_listings(self) -> List[ServiceListing]:
        """Get all active service listings"""
        try:
            models = self.session.query(ServiceListingModel).filter_by(active=True).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting active service listings: {str(e)}')
        finally:
            self.session.close()
    
    def get_active_listings_by_tutor(self, tutor_id: int) -> List[ServiceListing]:
        """Get active service listings for a tutor"""
        try:
            models = self.session.query(ServiceListingModel).filter_by(
                tutor_id=tutor_id, active=True
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting active listings by tutor: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, service_listing: ServiceListing) -> ServiceListing:
        """Update service listing"""
        try:
            model = self.session.query(ServiceListingModel).filter_by(id=service_listing.id).first()
            if not model:
                raise ValueError(f'Service listing with id {service_listing.id} not found')
            
            model.title = service_listing.title
            model.description = service_listing.description
            model.price_per_hour = service_listing.price_per_hour
            model.active = service_listing.active
            model.updated_at = service_listing.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating service listing: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, service_id: int) -> bool:
        """Delete service listing"""
        return super().delete(service_id)
    
    def search_by_title(self, title: str) -> List[ServiceListing]:
        """Search service listings by title"""
        try:
            models = self.session.query(ServiceListingModel).filter(
                ServiceListingModel.title.like(f'%{title}%')
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error searching service listings by title: {str(e)}')
        finally:
            self.session.close()
