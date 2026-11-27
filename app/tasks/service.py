import logging

from sqlmodel import Session

from app.tasks.models import Task
from app.tasks.repository import TaskRepository
from app.tasks.schemas import TaskCreate
from app.projects.service import ProjectService
from app.users.service import UserService

class TaskService:

    logger = logging.getLogger(__name__)

    def __init__(self, repository: TaskRepository, project_service: ProjectService, user_service: UserService,):
        self.repository = repository
        self.project_service = project_service
        self.user_service = user_service
        
    def create_task(self, task_data: TaskCreate, owner_id: int,) -> Task:
        project = self.project_service.get_project_by_id_and_owner(
            task_data.project_id,
            owner_id,
        )

        if project is None:
            return None
        
        if task_data.assigned_to is not None:
            user = self.user_service.find_user(task_data.assigned_to)

            if user is None:
                raise ValueError("Assigned user not found")

        return self.repository.create_task(task_data)