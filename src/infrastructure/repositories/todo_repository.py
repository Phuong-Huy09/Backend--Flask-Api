from domain.models.interfaces.itodo_repository import ITodoRepository
from domain.models.todo import Todo
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from config import Config
from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.base import Base
from infrastructure.models.todo_model import TodoModel
from infrastructure.databases.mssql import session
from infrastructure.repositories.base_repository import BaseRepository

load_dotenv()

class TodoRepository(BaseRepository[TodoModel], ITodoRepository):
    """
    Todo Repository implementation inheriting from BaseRepository
    """
    
    def __init__(self, session: Session = None):
        super().__init__(TodoModel, session or session)
        self._todos = []
        self._id_counter = 1

    def add(self, todo: Todo) -> TodoModel:
        """Add a new todo using inherited base repository method"""
        try:
            # Manual mapping from Todo to TodoModel
            todo_model = TodoModel(
                title=todo.title,
                description=todo.description,
                status=todo.status,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
            return super().add(todo_model)
        except Exception as e:
            raise ValueError(f'Error adding todo: {str(e)}')

    def list(self) -> List[TodoModel]:
        """Get all todos using inherited base repository method"""
        return self.get_all()

    def update(self, todo: TodoModel) -> TodoModel:
        """Update todo using inherited base repository method"""
        return super().update(todo)

    def delete(self, todo_id: int) -> None:
        """Delete todo using inherited base repository method"""
        super().delete(todo_id)
    
    def get_todos_by_status(self, status: bool) -> List[TodoModel]:
        """Get todos by status"""
        return self.find_by(status=status)
    
    def get_completed_todos(self) -> List[TodoModel]:
        """Get all completed todos"""
        return self.get_todos_by_status(True)
    
    def get_pending_todos(self) -> List[TodoModel]:
        """Get all pending todos"""
        return self.get_todos_by_status(False)

