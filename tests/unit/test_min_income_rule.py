"""Test Minimum Income Rule"""
import pytest

from credit_engine.domain.entities.applicant import Applicant
from credit_engine.domain.entities.proposal import Proposal
from credit_engine.domain.value_objects.channel import Channel
from credit_engine.domain.value_objects.product_type import ProductType
from credit_engine.interfaces.engine.rules.min_income_rule import MinIncomeRule


@pytest.mark.asyncio
async def test_min_income_rule_passes():
    """Testa que a regra passa quando a renda é suficiente"""
    applicant = Applicant(
        document_number="12345678900",
        name="John Doe",
        monthly_income=2000.0,
        age=30,
    )
    proposal = Proposal(
        applicant=applicant,
        requested_amount=5000.0,
        installments=12,
        product_type=ProductType.PERSONAL_LOAN,
        channel=Channel.APP,
    )

    rule = MinIncomeRule()
    result = await rule.evaluate(proposal)

    assert result.passed is True
    assert result.rule_code == "MIN_INCOME_NOT_MET"
    assert result.message is None


@pytest.mark.asyncio
async def test_min_income_rule_fails():
    """Testa que a regra falha quando a renda é insuficiente"""
    applicant = Applicant(
        document_number="12345678900",
        name="John Doe",
        monthly_income=500.0,
        age=30,
    )
    proposal = Proposal(
        applicant=applicant,
        requested_amount=5000.0,
        installments=12,
        product_type=ProductType.PERSONAL_LOAN,
        channel=Channel.APP,
    )

    rule = MinIncomeRule()
    result = await rule.evaluate(proposal)

    assert result.passed is False
    assert result.rule_code == "MIN_INCOME_NOT_MET"
    assert result.message is not None
    assert "Minimum income not met" in result.message
