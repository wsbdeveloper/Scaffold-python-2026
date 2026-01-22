"""Credit Decision Service"""

from ...domain.repositories.user_repository import UserRepository
from ..dto.user_dto import UserDTO


class UserService:
    """Serviço de gerenciamento do usuário e suas operações"""

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def analyze_proposal(self, request: UserDTO):
        """
        Analisa uma proposta de crédito e retorna a decisão
        """
        # Converte DTO para entidade de domínio
        pass
