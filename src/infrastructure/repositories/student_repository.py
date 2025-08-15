from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.repositories.base_repository import BaseRepository
from infrastructure.models.student_profile_model import StudentProfileModel
from infrastructure.databases.mssql import session

class StudentRepository(BaseRepository[StudentProfileModel]):
    """
    Student Repository implementation inheriting from BaseRepository
    Example of how to use BaseRepository for other entities
    """
    
    def __init__(self, session: Session = None):
        super().__init__(StudentProfileModel, session or session)
    
    def get_students_by_grade(self, grade: str) -> List[StudentProfileModel]:
        """Get students by grade level"""
        return self.find_by(grade=grade)
    
    def get_active_students(self) -> List[StudentProfileModel]:
        """Get all active students"""
        return self.find_by(is_active=True)
    
    def search_students_by_name(self, name: str) -> List[StudentProfileModel]:
        """Search students by name (contains search)"""
        try:
            return self.session.query(self.model_class).filter(
                self.model_class.name.contains(name)
            ).all()
        except Exception as e:
            raise ValueError(f'Error searching students by name: {str(e)}')
        finally:
            self.session.close()
    
    def get_students_by_subject_interest(self, subject_id: int) -> List[StudentProfileModel]:
        """Get students interested in a specific subject"""
        # This would require a more complex query with joins
        # Implementation depends on your data model structure
        pass
