"""Minimum Income Rule"""
from ....domain.entities.proposal import Proposal
from ....domain.entities.rule_result import RuleResult
from ..rule import Rule


class MinIncomeRule(Rule):
    """Regra que verifica se a renda mínima foi atendida"""

    MIN_INCOME = 1000.0

    @property
    def code(self) -> str:
        return "MIN_INCOME_NOT_MET"

    @property
    def name(self) -> str:
        return "Minimum Income Rule"

    async def evaluate(self, proposal: Proposal) -> RuleResult:
        """Avalia se a renda mínima foi atendida"""
        passed = proposal.applicant.monthly_income >= self.MIN_INCOME
        message = (
            f"Minimum income not met. Required: {self.MIN_INCOME}, "
            f"Provided: {proposal.applicant.monthly_income}"
            if not passed
            else None
        )
        return RuleResult(
            rule_code=self.code,
            passed=passed,
            message=message,
            metadata={
                "min_income": self.MIN_INCOME,
                "applicant_income": proposal.applicant.monthly_income,
            },
        )
