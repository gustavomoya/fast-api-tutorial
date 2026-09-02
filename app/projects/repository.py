from sqlmodel import Session, select
from sqlalchemy.orm import selectinload, joinedload

from app.projects.models import Project
from app.users.models import User
from app.projects.schemas import ProjectFilterParams

class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session
        
        
    def get_projects(self, filters: ProjectFilterParams) -> list[Project]:        
        # statement = (
        #     select(Project)
        #     .options(
        #         joinedload(Project.owner)
        #     )
        #     .offset(filters.offset)
        #     .limit(filters.limit)
        # )
        statement = select(Project).options(joinedload(Project.owner))
        
        if filters.name:
            statement = statement.where(Project.name == filters.name)
        
        statement = statement.offset(filters.offset).limit(filters.limit)

        return list(self.session.exec(statement).all())
    
    def get_project(self, id: int) -> Project:
        return self.session.get(Project, id)    
        
    def get_projects_by_user(self, user_id: int):
        statement = (
                    select(Project)
                    .options(
                        joinedload(Project.owner)
                    )
                    .where(Project.owner_id == user_id)
                    .offset(0)
                    
                    .limit(100)
                )
        return list(self.session.exec(statement).all())