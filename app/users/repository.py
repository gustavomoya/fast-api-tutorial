from sqlmodel import Session, select

from app.users.models import User


def get_users(session: Session) -> list[User]:
    statement = select(User)

    return list(session.exec(statement).all())
