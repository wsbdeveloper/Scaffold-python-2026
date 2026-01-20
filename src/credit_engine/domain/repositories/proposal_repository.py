"""Proposal Repository Interface"""
from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.proposal import Proposal


class ProposalRepository(ABC):
    """Interface para repositório de propostas"""

    @abstractmethod
    async def save(self, proposal: Proposal) -> Proposal:
        """Salva uma proposta"""
        pass

    @abstractmethod
    async def get_by_id(self, proposal_id: UUID) -> Proposal | None:
        """Busca uma proposta por ID"""
        pass
