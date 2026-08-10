from sqlmodel import Session

from app.users.models import User
from app.users.repository import get_users


def list_users(session: Session) -> list[User]:
    return get_users(session)
