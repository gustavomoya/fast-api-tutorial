from sqlmodel import Session, select

from app.users.models import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
        
        
    def get_users(self, offset: int = 0, limit: int = 100) -> list[User]:
        statement = select(User).offset(offset).limit(limit)
        session = self.session
        return list(session.exec(statement).all())

    def get_user(self, id : int) -> User:
        return self.session.get(User, id)        