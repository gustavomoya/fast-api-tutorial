
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_active_user
from app.projects.member_dependencies import get_project_member_service
from app.projects.member_schemas import (
    ProjectMemberCreate,
    ProjectMemberRead,
)
from app.projects.member_service import (
    ProjectMemberService,
    ProjectNotFoundError,
    UserNotFoundError,
    NotProjectOwnerError,
    NotProjectMemberError,
    UserAlreadyMemberError,
    OwnerCannotBeMemberError,
    InactiveUserError,
)
from app.users.models import User


router = APIRouter(
    prefix="/projects/{project_id}/members",
    tags=["Project Members"],
)


@router.post(
    "/",
    response_model=ProjectMemberRead,
    status_code=status.HTTP_201_CREATED,
)
def add_member(
    project_id: int,
    member_data: ProjectMemberCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: Annotated[
        ProjectMemberService,
        Depends(get_project_member_service),
    ],
):
    try:
        return service.add_member(
            project_id,
            current_user.id,
            member_data.user_id,
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    except NotProjectOwnerError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the project owner can manage members",
        )
    except UserAlreadyMemberError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a project member",
        )
    except OwnerCannotBeMemberError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project owner cannot be added as a member",
        )
    except InactiveUserError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add an inactive user",
        )


@router.get(
    "/",
    response_model=list[ProjectMemberRead],
)
def get_members(
    project_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: Annotated[
        ProjectMemberService,
        Depends(get_project_member_service),
    ],
):
    try:
        return service.get_members(project_id, current_user.id)
    except ProjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    except NotProjectMemberError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this project",
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_member(
    project_id: int,
    user_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    service: Annotated[
        ProjectMemberService,
        Depends(get_project_member_service),
    ],
):
    try:
        removed = service.remove_member(
            project_id,
            current_user.id,
            user_id,
        )

        if not removed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project membership not found",
            )

    except ProjectNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    except NotProjectOwnerError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the project owner can manage members",
        )
    except OwnerCannotBeMemberError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project owner is not a project member",
        )
