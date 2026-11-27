
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.projects.models import Project
    from app.users.models import User


class ProjectMember(SQLModel, table=True):
    __tablename__ = "project_members"

    project_id: int = Field(
        foreign_key="projects.id",
        primary_key=True,
        sa_type=BIGINT(unsigned=True),
    )

    user_id: int = Field(
        foreign_key="users.id",
        primary_key=True,
        sa_type=BIGINT(unsigned=True),
    )

    created_at: datetime = Field(
        sa_type=TIMESTAMP,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        },
    )

    project: "Project" = Relationship(
        back_populates="members",
    )

    user: "User" = Relationship(
        back_populates="project_memberships",
    )
