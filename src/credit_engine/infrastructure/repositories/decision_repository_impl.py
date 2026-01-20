"""Decision Repository Implementation"""
from uuid import UUID

from sqlalchemy.orm import Session

from ...domain.entities.decision import Decision
from ...domain.entities.rule_result import RuleResult
from ...domain.repositories.decision_repository import DecisionRepository
from ...domain.value_objects.decision_status import DecisionStatus
from ..database.models import DecisionModel


class DecisionRepositoryImpl(DecisionRepository):
    """Implementação do repositório de decisões"""

    def __init__(self, db: Session):
        self.db = db

    async def save(self, decision: Decision) -> Decision:
        """Salva uma decisão no banco"""
        # Converte rule_results para JSON
        rule_results_json = [
            {
                "rule_code": r.rule_code,
                "passed": r.passed,
                "message": r.message,
                "metadata": r.metadata,
            }
            for r in decision.rule_results
        ]

        decision_model = self.db.query(DecisionModel).filter_by(id=decision.id).first()
        if not decision_model:
            decision_model = DecisionModel(
                id=decision.id,
                proposal_id=decision.proposal_id,
                status=decision.status,
                policy_name=decision.policy_name,
                policy_version=decision.policy_version,
                rule_results=rule_results_json,
                created_at=decision.created_at,
            )
            self.db.add(decision_model)
        else:
            decision_model.status = decision.status
            decision_model.policy_name = decision.policy_name
            decision_model.policy_version = decision.policy_version
            decision_model.rule_results = rule_results_json

        self.db.commit()
        self.db.refresh(decision_model)

        return self._to_entity(decision_model)

    async def get_by_proposal_id(self, proposal_id: UUID) -> Decision | None:
        """Busca uma decisão por ID da proposta"""
        decision_model = self.db.query(DecisionModel).filter_by(proposal_id=proposal_id).first()
        if not decision_model:
            return None

        return self._to_entity(decision_model)

    async def get_by_id(self, decision_id: UUID) -> Decision | None:
        """Busca uma decisão por ID"""
        decision_model = self.db.query(DecisionModel).filter_by(id=decision_id).first()
        if not decision_model:
            return None

        return self._to_entity(decision_model)

    def _to_entity(self, decision_model: DecisionModel) -> Decision:
        """Converte modelo para entidade"""
        rule_results = [
            RuleResult(
                rule_code=r["rule_code"],
                passed=r["passed"],
                message=r.get("message"),
                metadata=r.get("metadata"),
            )
            for r in decision_model.rule_results
        ]

        return Decision(
            id=decision_model.id,
            proposal_id=decision_model.proposal_id,
            status=DecisionStatus(decision_model.status.value),
            policy_name=decision_model.policy_name,
            policy_version=decision_model.policy_version,
            rule_results=rule_results,
            created_at=decision_model.created_at,
        )
