from sqlmodel import Session

from app.users.models import User
from app.users.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        
    def list_users(self, filters) -> list[User]:
        return self.repository.get_users(filters)

    def find_user(self, id: int) -> User:
        return self.repository.get_user(id)  