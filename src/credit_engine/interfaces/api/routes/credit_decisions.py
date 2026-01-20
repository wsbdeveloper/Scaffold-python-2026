"""Credit Decisions Routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from ....application.dto.proposal_dto import ProposalRequestDTO, DecisionResponseDTO
from ....application.services.credit_decision_service import CreditDecisionService
from ....infrastructure.database.base import get_db
from ....infrastructure.repositories.decision_repository_impl import DecisionRepositoryImpl
from ....infrastructure.repositories.policy_repository_impl import PolicyRepositoryImpl
from ....infrastructure.repositories.proposal_repository_impl import ProposalRepositoryImpl
from ....interfaces.engine.decision_engine import DecisionEngine
from ....interfaces.engine.rules.age_range_rule import AgeRangeRule
from ....interfaces.engine.rules.max_income_commitment_rule import MaxIncomeCommitmentRule
from ....interfaces.engine.rules.max_installments_rule import MaxInstallmentsRule
from ....interfaces.engine.rules.min_income_rule import MinIncomeRule


router = APIRouter(prefix="/credit_decisions", tags=["credit_decisions"])


def get_credit_decision_service(db: Session = Depends(get_db)) -> CreditDecisionService:
    """Factory para criar o serviço de decisão de crédito"""
    proposal_repo = ProposalRepositoryImpl(db)
    decision_repo = DecisionRepositoryImpl(db)
    policy_repo = PolicyRepositoryImpl(db)

    # Configura as regras do engine
    rules = [
        MinIncomeRule(),
        MaxIncomeCommitmentRule(),
        AgeRangeRule(),
        MaxInstallmentsRule(),
    ]
    engine = DecisionEngine(rules=rules)

    return CreditDecisionService(
        proposal_repository=proposal_repo,
        decision_repository=decision_repo,
        policy_repository=policy_repo,
        decision_engine=engine,
    )


@router.post("", response_model=DecisionResponseDTO, status_code=201)
async def create_credit_decision(
    request: ProposalRequestDTO,
    service: CreditDecisionService = Depends(get_credit_decision_service),
):
    """Submete uma proposta para análise de crédito"""
    try:
        decision = await service.analyze_proposal(request)
        return _decision_to_dto(decision)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/by-proposal/{proposal_id}", response_model=DecisionResponseDTO)
async def get_credit_decision_by_proposal(
    proposal_id: UUID,
    service: CreditDecisionService = Depends(get_credit_decision_service),
):
    """Consulta a decisão de uma proposta pelo ID da proposta"""
    decision = await service.get_decision_by_proposal_id(proposal_id)
    if not decision:
        raise HTTPException(
            status_code=404,
            detail=f"Decision not found for proposal_id: {proposal_id}. Make sure you submitted a proposal first using POST /credit_decisions"
        )
    return _decision_to_dto(decision)


@router.get("/{decision_id}", response_model=DecisionResponseDTO)
async def get_credit_decision(
    decision_id: UUID,
    service: CreditDecisionService = Depends(get_credit_decision_service),
):
    """Consulta uma decisão pelo ID da decisão"""
    decision = await service.get_decision_by_id(decision_id)
    if not decision:
        raise HTTPException(
            status_code=404,
            detail=f"Decision not found with id: {decision_id}. Use the 'id' field from the POST /credit_decisions response."
        )
    return _decision_to_dto(decision)


def _decision_to_dto(decision) -> DecisionResponseDTO:
    """Converte entidade Decision para DTO"""
    from ....application.dto.proposal_dto import RuleResultDTO

    rule_results_dto = [
        RuleResultDTO(
            rule_code=r.rule_code,
            passed=r.passed,
            message=r.message,
            metadata=r.metadata,
        )
        for r in decision.rule_results
    ]

    return DecisionResponseDTO(
        id=decision.id,
        proposal_id=decision.proposal_id,
        status=decision.status.value,
        policy_name=decision.policy_name,
        policy_version=decision.policy_version,
        rejected_reasons=decision.rejected_reasons,
        rule_results=rule_results_dto,
        created_at=decision.created_at.isoformat(),
    )

