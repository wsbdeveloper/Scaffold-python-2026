"""Proposal DTOs"""

from pydantic import BaseModel, Field


class UserDTO(BaseModel):
    """DTO para dados do usuário"""

    document_number: str = Field(..., description="CPF ou documento similar")
    name: str = Field(..., description="Nome completo")
    monthly_income: float = Field(..., gt=0, description="Renda mensal")
    age: int = Field(..., ge=0, le=120, description="Idade")


# DTO Request e Response podem ser adicionados conforme necessário
