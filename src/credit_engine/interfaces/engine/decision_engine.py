"""Decision Engine"""
from typing import List

from ...domain.entities.decision import Decision
from ...domain.entities.policy import Policy
from ...domain.entities.proposal import Proposal
from ...domain.entities.rule_result import RuleResult
from ...domain.value_objects.decision_status import DecisionStatus
from .rule import Rule


class DecisionEngine:
    """Motor de decisão de crédito"""

    def __init__(self, rules: List[Rule]):
        """Inicializa o engine com uma lista de regras"""
        self.rules = rules

    async def evaluate(self, proposal: Proposal, policy: Policy) -> Decision:
        """
        Avalia uma proposta usando as regras configuradas e retorna uma decisão
        """
        rule_results: List[RuleResult] = []

        # Executa todas as regras
        for rule in self.rules:
            result = await rule.evaluate(proposal)
            rule_results.append(result)

        # Determina o status baseado nos resultados
        all_passed = all(result.passed for result in rule_results)

        # Tenary operator aqui eu poderia ter usado um if/else, mas preferi usar o tenary operator para ser mais pythonico
        # fica mais limpo e legivel o código.
        status = DecisionStatus.APPROVED if all_passed else DecisionStatus.REJECTED

        # Cria a decisão
        decision = Decision(
            proposal_id=proposal.id,
            status=status,
            policy_name=policy.name,
            policy_version=policy.version,
            rule_results=rule_results
        )

        return decision

