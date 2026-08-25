from sqlmodel import Session, select

from app.users.models import User
from app.users.schemas import UserFilterParams

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
        
        
    def get_users(self, filters: UserFilterParams) -> list[User]:
        statement = select(User)
        
        if filters.name:
            statement = statement.where(User.name == filters.name)
        if filters.email:
            statement = statement.where(User.email == filters.email)
        if filters.is_active is not None:
            statement = statement.where(User.is_active == filters.is_active)                        
        
        statement = statement.offset(filters.offset).limit(filters.limit)
        
        return list(self.session.exec(statement).all())

    def get_user(self, id : int) -> User:
        return self.session.get(User, id)       

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(
            User.email == email
        )

        return self.session.exec(statement).first() 