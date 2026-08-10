from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.tasks.models import Task


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    name: str = Field(
        max_length=50,
        unique=True,
    )

    task_tags: list["TaskTag"] = Relationship(
        back_populates="tag",
        cascade_delete=True,
    )


class TaskTag(SQLModel, table=True):
    __tablename__ = "task_tags"

    task_id: int = Field(
        foreign_key="tasks.id",
        primary_key=True,
    )

    tag_id: int = Field(
        foreign_key="tags.id",
        primary_key=True,
    )

    task: "Task" = Relationship(
        back_populates="task_tags",
    )

    tag: "Tag" = Relationship(
        back_populates="task_tags",
    )