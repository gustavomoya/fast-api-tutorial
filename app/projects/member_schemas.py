
from datetime import datetime

from sqlmodel import SQLModel


class ProjectMemberCreate(SQLModel):
    user_id: int


class ProjectMemberRead(SQLModel):
    project_id: int
    user_id: int
    created_at: datetime
