"""Maximum Income Commitment Rule"""
from ....domain.entities.proposal import Proposal
from ....domain.entities.rule_result import RuleResult
from ..rule import Rule


class MaxIncomeCommitmentRule(Rule):
    """Regra que verifica se o comprometimento máximo de renda foi respeitado"""

    MAX_COMMITMENT_PERCENTAGE = 0.30  # 30% da renda

    @property
    def code(self) -> str:
        return "MAX_INCOME_COMMITMENT_EXCEEDED"

    @property
    def name(self) -> str:
        return "Maximum Income Commitment Rule"

    async def evaluate(self, proposal: Proposal) -> RuleResult:
        """Avalia se o comprometimento de renda está dentro do limite"""
        monthly_payment = proposal.requested_amount / proposal.installments
        commitment_percentage = monthly_payment / proposal.applicant.monthly_income
        passed = commitment_percentage <= self.MAX_COMMITMENT_PERCENTAGE

        message = (
            f"Income commitment exceeded. Max: {self.MAX_COMMITMENT_PERCENTAGE * 100}%, "
            f"Calculated: {commitment_percentage * 100:.2f}%"
            if not passed
            else None
        )

        return RuleResult(
            rule_code=self.code,
            passed=passed,
            message=message,
            metadata={
                "max_commitment": self.MAX_COMMITMENT_PERCENTAGE,
                "calculated_commitment": commitment_percentage,
                "monthly_payment": monthly_payment,
            },
        )
