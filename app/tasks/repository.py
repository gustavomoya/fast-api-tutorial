from typing import Any

from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from app.tasks.schemas import TaskCreate
from app.tasks.models import Task
from app.tasks.models import Task


class TaskRepository:

    def __init__(self, session: Session):
        """Initialize the repository with a database session."""
        self.session = session

    def create_task(
        self,
        task_data: TaskCreate,
    ) -> Task | None:
        """Create a task."""

        task = Task(**task_data.model_dump())

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task
