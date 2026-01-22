"""Decision Repository Implementation"""

from sqlalchemy.orm import Session

from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    """Implementação do repositório de usuários"""

    def __init__(self, db: Session):
        self.db = db

    async def save(self, user: User) -> User:
        """Salva um usuário no banco"""
        return user
