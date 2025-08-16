from abc import ABC, abstractmethod
from typing import List, Optional
from ..availability_slot import AvailabilitySlot, Weekday

class IAvailabilitySlotRepository(ABC):
    """
    Interface for Availability Slot Repository
    """
    
    @abstractmethod
    def add(self, availability_slot: AvailabilitySlot) -> AvailabilitySlot:
        """Add a new availability slot"""
        pass
    
    @abstractmethod
    def get_by_id(self, slot_id: int) -> Optional[AvailabilitySlot]:
        """Get availability slot by ID"""
        pass
    
    @abstractmethod
    def get_by_tutor_id(self, tutor_id: int) -> List[AvailabilitySlot]:
        """Get all availability slots for a tutor"""
        pass
    
    @abstractmethod
    def get_by_tutor_and_weekday(self, tutor_id: int, weekday: Weekday) -> List[AvailabilitySlot]:
        """Get availability slots for a tutor on a specific weekday"""
        pass
    
    @abstractmethod
    def update(self, availability_slot: AvailabilitySlot) -> AvailabilitySlot:
        """Update availability slot"""
        pass
    
    @abstractmethod
    def delete(self, slot_id: int) -> bool:
        """Delete availability slot"""
        pass
    
    @abstractmethod
    def delete_by_tutor_id(self, tutor_id: int) -> bool:
        """Delete all availability slots for a tutor"""
        pass
