
from sqlmodel import Session, select

from app.projects.member_model import ProjectMember


class ProjectMemberRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_members(
        self,
        project_id: int,
    ) -> list[ProjectMember]:
        statement = select(ProjectMember).where(
            ProjectMember.project_id == project_id
        )

        return list(self.session.exec(statement).all())

    def get_membership(
        self,
        project_id: int,
        user_id: int,
    ) -> ProjectMember | None:
        statement = select(ProjectMember).where(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )

        return self.session.exec(statement).first()

    def add_member(
        self,
        project_id: int,
        user_id: int,
    ) -> ProjectMember:
        membership = ProjectMember(
            project_id=project_id,
            user_id=user_id,
        )

        self.session.add(membership)
        self.session.commit()
        self.session.refresh(membership)

        return membership

    def remove_member(self, membership: ProjectMember) -> None:
        self.session.delete(membership)
        self.session.commit()
