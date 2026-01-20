"""Policy Entity"""
from dataclasses import dataclass
from uuid import UUID

from ..value_objects.channel import Channel
from ..value_objects.product_type import ProductType


@dataclass
class Policy:
    """Entidade que representa uma política de crédito"""

    id: UUID
    name: str
    version: str
    product_types: list[ProductType]
    channels: list[Channel]
    is_active: bool = True

    def __post_init__(self):
        """Validações"""
        if not self.name or not self.name.strip():
            raise ValueError("Policy name is required")
        if not self.version or not self.version.strip():
            raise ValueError("Policy version is required")
        if not self.product_types:
            raise ValueError("Policy must have at least one product type")
        if not self.channels:
            raise ValueError("Policy must have at least one channel")

    def applies_to(self, product_type: ProductType, channel: Channel) -> bool:
        """Verifica se a política se aplica a um produto e canal"""
        if not self.is_active:
            return False
        return product_type in self.product_types and channel in self.channels
