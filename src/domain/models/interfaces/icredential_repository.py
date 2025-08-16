from abc import ABC, abstractmethod
from typing import List, Optional
from ..credential import Credential

class ICredentialRepository(ABC):
    """
    Interface for Credential Repository
    """
    
    @abstractmethod
    def add(self, credential: Credential) -> Credential:
        """Add a new credential"""
        pass
    
    @abstractmethod
    def get_by_id(self, credential_id: int) -> Optional[Credential]:
        """Get credential by ID"""
        pass
    
    @abstractmethod
    def get_by_tutor_id(self, tutor_id: int) -> List[Credential]:
        """Get all credentials for a tutor"""
        pass
    
    @abstractmethod
    def update(self, credential: Credential) -> Credential:
        """Update credential"""
        pass
    
    @abstractmethod
    def delete(self, credential_id: int) -> bool:
        """Delete credential"""
        pass
    
    @abstractmethod
    def get_verified_credentials(self, tutor_id: int) -> List[Credential]:
        """Get verified credentials for a tutor"""
        pass
    
    @abstractmethod
    def get_unverified_credentials(self) -> List[Credential]:
        """Get all unverified credentials"""
        pass
