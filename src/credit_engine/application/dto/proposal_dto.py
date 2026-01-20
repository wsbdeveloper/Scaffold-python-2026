"""Proposal DTOs"""
from uuid import UUID

from pydantic import BaseModel, Field

from ...domain.value_objects.channel import Channel
from ...domain.value_objects.product_type import ProductType


class ApplicantDTO(BaseModel):
    """DTO para dados do solicitante"""

    document_number: str = Field(..., description="CPF ou documento similar")
    name: str = Field(..., description="Nome completo")
    monthly_income: float = Field(..., gt=0, description="Renda mensal")
    age: int = Field(..., ge=0, le=120, description="Idade")


class ProposalRequestDTO(BaseModel):
    """DTO para requisição de análise de crédito"""

    applicant: ApplicantDTO
    requested_amount: float = Field(..., gt=0, description="Valor solicitado")
    installments: int = Field(..., gt=0, description="Número de parcelas")
    product_type: ProductType = Field(..., description="Tipo de produto")
    channel: Channel = Field(..., description="Canal de origem")


class RuleResultDTO(BaseModel):
    """DTO para resultado de regra"""

    rule_code: str
    passed: bool
    message: str | None = None
    metadata: dict | None = None


class DecisionResponseDTO(BaseModel):
    """DTO para resposta de decisão"""

    id: UUID
    proposal_id: UUID
    status: str
    policy_name: str
    policy_version: str
    rejected_reasons: list[str]
    rule_results: list[RuleResultDTO]
    created_at: str
