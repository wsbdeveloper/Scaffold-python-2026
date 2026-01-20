"""Decision Repository Interface"""
from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.decision import Decision


class DecisionRepository(ABC):
    """Interface para repositório de decisões"""

    @abstractmethod
    async def save(self, decision: Decision) -> Decision:
        """Salva uma decisão"""
        pass

    @abstractmethod
    async def get_by_proposal_id(self, proposal_id: UUID) -> Decision | None:
        """Busca uma decisão por ID da proposta"""
        pass

    @abstractmethod
    async def get_by_id(self, decision_id: UUID) -> Decision | None:
        """Busca uma decisão por ID"""
        pass
