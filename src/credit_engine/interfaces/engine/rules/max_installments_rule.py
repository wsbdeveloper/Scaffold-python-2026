"""Maximum Installments Rule"""
from ..rule import Rule
from ....domain.entities.proposal import Proposal
from ....domain.entities.rule_result import RuleResult


class MaxInstallmentsRule(Rule):
    """Regra que verifica se o número de parcelas não excede o máximo"""

    MAX_INSTALLMENTS = 84  # 7 anos

    @property
    def code(self) -> str:
        return "MAX_INSTALLMENTS_EXCEEDED"

    @property
    def name(self) -> str:
        return "Maximum Installments Rule"

    async def evaluate(self, proposal: Proposal) -> RuleResult:
        """Avalia se o número de parcelas está dentro do limite"""
        passed = proposal.installments <= self.MAX_INSTALLMENTS

        message = (
            f"Maximum installments exceeded. Max: {self.MAX_INSTALLMENTS}, "
            f"Provided: {proposal.installments}"
            if not passed
            else None
        )

        return RuleResult(
            rule_code=self.code,
            passed=passed,
            message=message,
            metadata={
                "max_installments": self.MAX_INSTALLMENTS,
                "requested_installments": proposal.installments
            }
        )

