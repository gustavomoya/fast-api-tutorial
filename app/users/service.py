import logging

from sqlmodel import Session

from app.users.models import User
from app.users.repository import UserRepository
from app.core.security import Security

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, repository: UserRepository
                 #, security: Security
                 ):
        self.repository = repository
        #self.security = security
        
    def list_users(self, filters) -> list[User]:
        return self.repository.get_users(filters)

    def find_user(self, id: int) -> User:
        return self.repository.get_user(id)  