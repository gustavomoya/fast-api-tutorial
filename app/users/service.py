from sqlmodel import Session

from app.users.models import User
from app.users.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    def list_users(self, offset: int = 0, limit: int = 100) -> list[User]:
        return self.repository.get_users(offset, limit)

    def find_user(self, id: int) -> User:
        return self.repository.get_user(id)  