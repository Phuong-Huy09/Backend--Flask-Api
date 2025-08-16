from typing import Optional
from datetime import datetime, time
from enum import Enum

class Weekday(Enum):
    MON = "Mon"
    TUE = "Tue" 
    WED = "Wed"
    THU = "Thu"
    FRI = "Fri"
    SAT = "Sat"
    SUN = "Sun"

class AvailabilitySlot:
    def __init__(
        self,
        id: Optional[int] = None,
        tutor_id: int = 0,
        weekday: Weekday = Weekday.MON,
        start_time: time = time(9, 0),
        end_time: time = time(17, 0),
        timezone: str = "UTC",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.tutor_id = tutor_id
        self.weekday = weekday
        self.start_time = start_time
        self.end_time = end_time
        self.timezone = timezone
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def update_time_slot(self, start_time: time, end_time: time):
        """Update availability time slot"""
        if start_time >= end_time:
            raise ValueError("Start time must be before end time")
        self.start_time = start_time
        self.end_time = end_time
        self.updated_at = datetime.utcnow()
    
    def update_timezone(self, timezone: str):
        """Update timezone"""
        self.timezone = timezone
        self.updated_at = datetime.utcnow()
    
    def get_duration_hours(self) -> float:
        """Get duration in hours"""
        start_minutes = self.start_time.hour * 60 + self.start_time.minute
        end_minutes = self.end_time.hour * 60 + self.end_time.minute
        return (end_minutes - start_minutes) / 60.0
    
    def overlaps_with(self, other_start: time, other_end: time) -> bool:
        """Check if this slot overlaps with another time range"""
        return not (self.end_time <= other_start or self.start_time >= other_end)
