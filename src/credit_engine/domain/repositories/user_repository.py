"""Decision Repository Interface"""
from abc import ABC, abstractmethod

from ..entities.user import User


class UserRepository(ABC):
    """Interface para repositório de usuários"""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Salva um usuário no banco"""
        pass
