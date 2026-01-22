"""Credit Decisions Routes"""
from uuid import UUID

from fastapi import APIRouter

from ....application.dto.user_dto import UserDTO

router = APIRouter(prefix="/user", tags=["user_examples"])


@router.get("", response_model=UserDTO)
async def get_user_by_document(document_number: str):
    """Consulta um usuário pelo documento"""
    return UserDTO(
        id=UUID("123e4567-e89b-12d3-a456-426614174000"),
        document_number=document_number,
        name="João Silva",
        monthly_income=5000.0,
        age=30,
    )
