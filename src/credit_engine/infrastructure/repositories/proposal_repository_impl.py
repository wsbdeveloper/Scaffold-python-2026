"""Proposal Repository Implementation"""
from uuid import UUID

from sqlalchemy.orm import Session

from ...domain.entities.applicant import Applicant
from ...domain.entities.proposal import Proposal
from ...domain.repositories.proposal_repository import ProposalRepository
from ..database.models import ApplicantModel, ProposalModel


class ProposalRepositoryImpl(ProposalRepository):
    """Implementação do repositório de propostas"""

    def __init__(self, db: Session):
        self.db = db

    async def save(self, proposal: Proposal) -> Proposal:
        """Salva uma proposta no banco"""
        # Busca ou cria o applicant
        applicant_model = (
            self.db.query(ApplicantModel)
            .filter_by(document_number=proposal.applicant.document_number)
            .first()
        )

        if not applicant_model:
            applicant_model = ApplicantModel(
                document_number=proposal.applicant.document_number,
                name=proposal.applicant.name,
                monthly_income=proposal.applicant.monthly_income,
                age=proposal.applicant.age,
            )
            self.db.add(applicant_model)
            self.db.flush()
        else:
            # Atualiza dados do applicant se necessário
            applicant_model.name = proposal.applicant.name
            applicant_model.monthly_income = proposal.applicant.monthly_income
            applicant_model.age = proposal.applicant.age

        # Cria ou atualiza a proposta
        proposal_model = self.db.query(ProposalModel).filter_by(id=proposal.id).first()
        if not proposal_model:
            proposal_model = ProposalModel(
                id=proposal.id,
                applicant_id=applicant_model.id,
                requested_amount=proposal.requested_amount,
                installments=proposal.installments,
                product_type=proposal.product_type,
                channel=proposal.channel,
                created_at=proposal.created_at,
            )
            self.db.add(proposal_model)
        else:
            proposal_model.requested_amount = proposal.requested_amount
            proposal_model.installments = proposal.installments
            proposal_model.product_type = proposal.product_type
            proposal_model.channel = proposal.channel

        self.db.commit()
        self.db.refresh(proposal_model)

        # Converte de volta para entidade
        return self._to_entity(proposal_model, applicant_model)

    async def get_by_id(self, proposal_id: UUID) -> Proposal | None:
        """Busca uma proposta por ID"""
        proposal_model = self.db.query(ProposalModel).filter_by(id=proposal_id).first()
        if not proposal_model:
            return None

        applicant_model = proposal_model.applicant
        return self._to_entity(proposal_model, applicant_model)

    def _to_entity(
        self, proposal_model: ProposalModel, applicant_model: ApplicantModel
    ) -> Proposal:
        """Converte modelo para entidade"""
        applicant = Applicant(
            document_number=applicant_model.document_number,
            name=applicant_model.name,
            monthly_income=applicant_model.monthly_income,
            age=applicant_model.age,
        )

        return Proposal(
            id=proposal_model.id,
            applicant=applicant,
            requested_amount=proposal_model.requested_amount,
            installments=proposal_model.installments,
            product_type=proposal_model.product_type,
            channel=proposal_model.channel,
            created_at=proposal_model.created_at,
        )
