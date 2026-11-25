from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy import TIMESTAMP, text
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.users.models import User
    from app.tasks.models import Task


class Project(SQLModel, table=True):
    __tablename__ = "projects"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_type=BIGINT(unsigned=True),
    )

    name: str = Field(max_length=150)

    description: str | None = None

    owner_id: int = Field(
        foreign_key="users.id",
        index=True,
        sa_type=BIGINT(unsigned=True),
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