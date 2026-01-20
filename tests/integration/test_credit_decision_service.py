"""Integration Tests for Credit Decision Service"""
import pytest

from credit_engine.application.dto.proposal_dto import ApplicantDTO, ProposalRequestDTO
from credit_engine.application.services.credit_decision_service import CreditDecisionService
from credit_engine.domain.value_objects.channel import Channel
from credit_engine.domain.value_objects.product_type import ProductType
from credit_engine.infrastructure.repositories.decision_repository_impl import (
    DecisionRepositoryImpl,
)
from credit_engine.infrastructure.repositories.policy_repository_impl import PolicyRepositoryImpl
from credit_engine.infrastructure.repositories.proposal_repository_impl import (
    ProposalRepositoryImpl,
)
from credit_engine.interfaces.engine.decision_engine import DecisionEngine
from credit_engine.interfaces.engine.rules.age_range_rule import AgeRangeRule
from credit_engine.interfaces.engine.rules.max_income_commitment_rule import MaxIncomeCommitmentRule
from credit_engine.interfaces.engine.rules.max_installments_rule import MaxInstallmentsRule
from credit_engine.interfaces.engine.rules.min_income_rule import MinIncomeRule


@pytest.mark.asyncio
async def test_approved_proposal(db_session):
    """Testa uma proposta aprovada"""

    proposal_repo = ProposalRepositoryImpl(db_session)
    decision_repo = DecisionRepositoryImpl(db_session)
    policy_repo = PolicyRepositoryImpl(db_session)
    rules = [
        MinIncomeRule(),
        MaxIncomeCommitmentRule(),
        AgeRangeRule(),
        MaxInstallmentsRule(),
    ]
    engine = DecisionEngine(rules=rules)
    service = CreditDecisionService(
        proposal_repository=proposal_repo,
        decision_repository=decision_repo,
        policy_repository=policy_repo,
        decision_engine=engine,
    )

    request = ProposalRequestDTO(
        applicant=ApplicantDTO(
            document_number="12345678900",
            name="John Doe",
            monthly_income=5000.0,
            age=30,
        ),
        requested_amount=10000.0,
        installments=24,
        product_type=ProductType.PERSONAL_LOAN,
        channel=Channel.APP,
    )

    decision = await service.analyze_proposal(request)

    assert decision.status.value == "APPROVED"
    assert len(decision.rejected_reasons) == 0
    assert decision.policy_name == "DEFAULT_POLICY_V1"
    assert len(decision.rule_results) == 4
    assert all(r.passed for r in decision.rule_results)


@pytest.mark.asyncio
async def test_rejected_proposal_low_income(db_session):
    """Testa uma proposta rejeitada por renda baixa"""

    proposal_repo = ProposalRepositoryImpl(db_session)
    decision_repo = DecisionRepositoryImpl(db_session)
    policy_repo = PolicyRepositoryImpl(db_session)
    rules = [
        MinIncomeRule(),
        MaxIncomeCommitmentRule(),
        AgeRangeRule(),
        MaxInstallmentsRule(),
    ]
    engine = DecisionEngine(rules=rules)
    service = CreditDecisionService(
        proposal_repository=proposal_repo,
        decision_repository=decision_repo,
        policy_repository=policy_repo,
        decision_engine=engine,
    )

    request = ProposalRequestDTO(
        applicant=ApplicantDTO(
            document_number="98765432100",
            name="Jane Doe",
            monthly_income=500.0,  # Renda muito baixa
            age=30,
        ),
        requested_amount=5000.0,
        installments=12,
        product_type=ProductType.PERSONAL_LOAN,
        channel=Channel.APP,
    )

    decision = await service.analyze_proposal(request)

    assert decision.status.value == "REJECTED"
    assert "MIN_INCOME_NOT_MET" in decision.rejected_reasons
    assert decision.policy_name == "DEFAULT_POLICY_V1"
