"""Credit Decision Service"""
from uuid import UUID

from ...domain.entities.applicant import Applicant
from ...domain.entities.decision import Decision
from ...domain.entities.policy import Policy
from ...domain.entities.proposal import Proposal
from ...domain.repositories.decision_repository import DecisionRepository
from ...domain.repositories.policy_repository import PolicyRepository
from ...domain.repositories.proposal_repository import ProposalRepository
from ...interfaces.engine.decision_engine import DecisionEngine
from ..dto.proposal_dto import ProposalRequestDTO


class CreditDecisionService:
    """Serviço de aplicação para decisões de crédito"""

    def __init__(
        self,
        proposal_repository: ProposalRepository,
        decision_repository: DecisionRepository,
        policy_repository: PolicyRepository,
        decision_engine: DecisionEngine,
    ):
        self.proposal_repository = proposal_repository
        self.decision_repository = decision_repository
        self.policy_repository = policy_repository
        self.decision_engine = decision_engine

    async def analyze_proposal(self, request: ProposalRequestDTO) -> Decision:
        """
        Analisa uma proposta de crédito e retorna a decisão
        """
        # Converte DTO para entidade de domínio
        applicant = Applicant(
            document_number=request.applicant.document_number,
            name=request.applicant.name,
            monthly_income=request.applicant.monthly_income,
            age=request.applicant.age,
        )

        proposal = Proposal(
            applicant=applicant,
            requested_amount=request.requested_amount,
            installments=request.installments,
            product_type=request.product_type,
            channel=request.channel,
        )

        # Busca a política aplicável
        policy = await self.policy_repository.get_by_product_and_channel(
            proposal.product_type, proposal.channel
        )
        if not policy:
            raise ValueError(
                f"No active policy found for product {proposal.product_type} and channel {proposal.channel}"
            )

        
        proposal = await self.proposal_repository.save(proposal)
        decision = await self.decision_engine.evaluate(proposal, policy)
        decision = await self.decision_repository.save(decision)

        return decision

    async def get_decision_by_proposal_id(self, proposal_id: UUID) -> Decision | None:
        """Busca uma decisão pelo ID da proposta"""
        return await self.decision_repository.get_by_proposal_id(proposal_id)

    async def get_decision_by_id(self, decision_id: UUID) -> Decision | None:
        """Busca uma decisão pelo ID"""
        return await self.decision_repository.get_by_id(decision_id)

