from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.interfaces.icredential_repository import ICredentialRepository
from domain.models.credential import Credential, CredentialType
from infrastructure.models.credential_model import CredentialModel
from infrastructure.repositories.base_repository import BaseRepository

class CredentialRepository(BaseRepository[CredentialModel], ICredentialRepository):
    """
    Credential Repository Implementation
    """
    
    def __init__(self, session: Session = None):
        super().__init__(CredentialModel, session)
    
    def _model_to_domain(self, model: CredentialModel) -> Credential:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        
        return Credential(
            id=model.id,
            tutor_id=model.tutor_id,
            type=CredentialType(model.type.value),
            issuer=model.issuer,
            file_url=model.file_url,
            verified=model.verified,
            verified_at=model.verified_at,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _domain_to_model(self, domain: Credential) -> CredentialModel:
        """Convert domain entity to SQLAlchemy model"""
        return CredentialModel(
            id=domain.id,
            tutor_id=domain.tutor_id,
            type=domain.type.value,
            issuer=domain.issuer,
            file_url=domain.file_url,
            verified=domain.verified,
            verified_at=domain.verified_at,
            created_at=domain.created_at,
            updated_at=domain.updated_at
        )
    
    def add(self, credential: Credential) -> Credential:
        """Add a new credential"""
        model = self._domain_to_model(credential)
        saved_model = super().add(model)
        return self._model_to_domain(saved_model)
    
    def get_by_id(self, credential_id: int) -> Optional[Credential]:
        """Get credential by ID"""
        model = super().get_by_id(credential_id)
        return self._model_to_domain(model)
    
    def get_by_tutor_id(self, tutor_id: int) -> List[Credential]:
        """Get all credentials for a tutor"""
        try:
            models = self.session.query(CredentialModel).filter_by(tutor_id=tutor_id).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting credentials by tutor_id: {str(e)}')
        finally:
            self.session.close()
    
    def update(self, credential: Credential) -> Credential:
        """Update credential"""
        try:
            model = self.session.query(CredentialModel).filter_by(id=credential.id).first()
            if not model:
                raise ValueError(f'Credential with id {credential.id} not found')
            
            model.type = credential.type.value
            model.issuer = credential.issuer
            model.file_url = credential.file_url
            model.verified = credential.verified
            model.verified_at = credential.verified_at
            model.updated_at = credential.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_domain(model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating credential: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, credential_id: int) -> bool:
        """Delete credential"""
        return super().delete(credential_id)
    
    def get_verified_credentials(self, tutor_id: int) -> List[Credential]:
        """Get verified credentials for a tutor"""
        try:
            models = self.session.query(CredentialModel).filter_by(
                tutor_id=tutor_id, verified=True
            ).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting verified credentials: {str(e)}')
        finally:
            self.session.close()
    
    def get_unverified_credentials(self) -> List[Credential]:
        """Get all unverified credentials"""
        try:
            models = self.session.query(CredentialModel).filter_by(verified=False).all()
            return [self._model_to_domain(model) for model in models]
        except Exception as e:
            raise ValueError(f'Error getting unverified credentials: {str(e)}')
        finally:
            self.session.close()
