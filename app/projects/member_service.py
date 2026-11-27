
from app.projects.member_model import ProjectMember
from app.projects.member_repository import ProjectMemberRepository
from app.projects.service import ProjectService
from app.users.service import UserService


class ProjectNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class NotProjectOwnerError(Exception):
    pass


class NotProjectMemberError(Exception):
    pass


class UserAlreadyMemberError(Exception):
    pass


class OwnerCannotBeMemberError(Exception):
    pass


class InactiveUserError(Exception):
    pass


class ProjectMemberService:

    def __init__(
        self,
        repository: ProjectMemberRepository,
        project_service: ProjectService,
        user_service: UserService,
    ):
        self.repository = repository
        self.project_service = project_service
        self.user_service = user_service

    def add_member(
        self,
        project_id: int,
        owner_id: int,
        user_id: int,
    ) -> ProjectMember:

        project = self.project_service.get_project(project_id)

        if project is None:
            raise ProjectNotFoundError

        if project.owner_id != owner_id:
            raise NotProjectOwnerError

        user = self.user_service.find_user(user_id)

        if user is None:
            raise UserNotFoundError

        if not user.is_active:
            raise InactiveUserError

        if user_id == project.owner_id:
            raise OwnerCannotBeMemberError

        membership = self.repository.get_membership(
            project_id,
            user_id,
        )

        if membership is not None:
            raise UserAlreadyMemberError

        return self.repository.add_member(project_id, user_id)

    def get_members(
        self,
        project_id: int,
        user_id: int,
    ) -> list[ProjectMember]:

        project = self.project_service.get_project(project_id)

        if project is None:
            raise ProjectNotFoundError

        is_owner = project.owner_id == user_id

        if not is_owner:
            membership = self.repository.get_membership(
                project_id,
                user_id,
            )

            if membership is None:
                raise NotProjectMemberError

        return self.repository.get_members(project_id)

    def remove_member(
        self,
        project_id: int,
        owner_id: int,
        user_id: int,
    ) -> bool:

        project = self.project_service.get_project(project_id)

        if project is None:
            raise ProjectNotFoundError

        if project.owner_id != owner_id:
            raise NotProjectOwnerError

        if user_id == project.owner_id:
            raise OwnerCannotBeMemberError

        membership = self.repository.get_membership(
            project_id,
            user_id,
        )

        if membership is None:
            return False

        self.repository.remove_member(membership)

        return True
