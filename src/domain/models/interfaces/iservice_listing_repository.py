from abc import ABC, abstractmethod
from typing import List, Optional
from ..service_listing import ServiceListing

class IServiceListingRepository(ABC):
    """
    Interface for Service Listing Repository
    """
    
    @abstractmethod
    def add(self, service_listing: ServiceListing) -> ServiceListing:
        """Add a new service listing"""
        pass
    
    @abstractmethod
    def get_by_id(self, service_id: int) -> Optional[ServiceListing]:
        """Get service listing by ID"""
        pass
    
    @abstractmethod
    def get_by_tutor_id(self, tutor_id: int) -> List[ServiceListing]:
        """Get all service listings for a tutor"""
        pass
    
    @abstractmethod
    def get_active_listings(self) -> List[ServiceListing]:
        """Get all active service listings"""
        pass
    
    @abstractmethod
    def get_active_listings_by_tutor(self, tutor_id: int) -> List[ServiceListing]:
        """Get active service listings for a tutor"""
        pass
    
    @abstractmethod
    def update(self, service_listing: ServiceListing) -> ServiceListing:
        """Update service listing"""
        pass
    
    @abstractmethod
    def delete(self, service_id: int) -> bool:
        """Delete service listing"""
        pass
    
    @abstractmethod
    def search_by_title(self, title: str) -> List[ServiceListing]:
        """Search service listings by title"""
        pass
