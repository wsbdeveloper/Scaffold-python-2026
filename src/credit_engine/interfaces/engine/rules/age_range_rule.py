"""Age Range Rule"""
from ..rule import Rule
from ....domain.entities.proposal import Proposal
from ....domain.entities.rule_result import RuleResult


class AgeRangeRule(Rule):
    """Regra que verifica se a idade está dentro da faixa permitida"""

    MIN_AGE = 18
    MAX_AGE = 65

    @property
    def code(self) -> str:
        return "AGE_OUT_OF_RANGE"

    @property
    def name(self) -> str:
        return "Age Range Rule"

    async def evaluate(self, proposal: Proposal) -> RuleResult:
        """Avalia se a idade está dentro da faixa permitida"""
        age = proposal.applicant.age
        passed = self.MIN_AGE <= age <= self.MAX_AGE

        message = (
            f"Age out of range. Required: {self.MIN_AGE}-{self.MAX_AGE}, Provided: {age}"
            if not passed
            else None
        )

        return RuleResult(
            rule_code=self.code,
            passed=passed,
            message=message,
            metadata={"min_age": self.MIN_AGE, "max_age": self.MAX_AGE, "applicant_age": age}
        )

