"""Rule Interface"""
from abc import ABC, abstractmethod

from ...domain.entities.proposal import Proposal
from ...domain.entities.rule_result import RuleResult


class Rule(ABC):
    """Interface base para regras de crédito"""

    @property
    @abstractmethod
    def code(self) -> str:
        """Código único da regra"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Nome da regra"""
        pass

    @abstractmethod
    async def evaluate(self, proposal: Proposal) -> RuleResult:
        """Avalia a proposta e retorna o resultado"""
        pass

