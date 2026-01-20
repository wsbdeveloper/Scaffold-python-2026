"""Proposal Entity"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from ..value_objects.channel import Channel
from ..value_objects.product_type import ProductType
from .applicant import Applicant


@dataclass
class Proposal:
    """Entidade que representa uma proposta de crédito"""
    applicant: Applicant
    requested_amount: float
    installments: int
    product_type: ProductType
    channel: Channel
    id: Optional[UUID] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Validações e inicializações"""
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.requested_amount <= 0:
            raise ValueError("Requested amount must be positive")
        if self.installments <= 0:
            raise ValueError("Installments must be positive")

