
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Index,
    Text,
    text,
)
from sqlalchemy.dialects.mysql import BIGINT
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.users.models import User
    from app.tasks.models import Task
    from app.projects.member_model import ProjectMember


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    __table_args__ = (
        Index("idx_projects_owner", "owner_id"),
    )

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_type=BIGINT(unsigned=True),
    )

    name: str = Field(max_length=150)

    description: str | None = Field(
        default=None,
        sa_type=Text,
    )

    owner_id: int = Field(
        sa_column=Column(
            BIGINT(unsigned=True),
            ForeignKey(
                "users.id",
                name="fk_projects_owner",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
    )

    created_at: datetime = Field(
        sa_type=TIMESTAMP,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
        },
    )

    updated_at: datetime = Field(
        sa_type=TIMESTAMP,
        nullable=False,
        sa_column_kwargs={
            "server_default": text(
                "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
            ),
        },
    )

    owner: "User" = Relationship(
        back_populates="projects",
    )

    tasks: list["Task"] = Relationship(
        back_populates="project",
        cascade_delete=True,
    )

    members: list["ProjectMember"] = Relationship(
        back_populates="project",
    )
