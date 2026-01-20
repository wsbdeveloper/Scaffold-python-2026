"""Decision Entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.decision_status import DecisionStatus
from .rule_result import RuleResult


@dataclass
class Decision:
    """Entidade que representa uma decisão de crédito"""

    proposal_id: UUID
    status: DecisionStatus
    policy_name: str
    policy_version: str
    rule_results: list[RuleResult]
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Validações e inicializações"""
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if not self.policy_name or not self.policy_name.strip():
            raise ValueError("Policy name is required")
        if not self.policy_version or not self.policy_version.strip():
            raise ValueError("Policy version is required")

    @property
    def rejected_reasons(self) -> list[str]:
        """Retorna os códigos das regras que falharam"""
        return [result.rule_code for result in self.rule_results if not result.passed]
