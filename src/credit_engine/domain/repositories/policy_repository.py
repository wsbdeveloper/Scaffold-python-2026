"""Policy Repository Interface"""
from abc import ABC, abstractmethod

from ..entities.policy import Policy
from ..value_objects.channel import Channel
from ..value_objects.product_type import ProductType


class PolicyRepository(ABC):
    """Interface para repositório de políticas"""

    @abstractmethod
    async def get_by_product_and_channel(
        self, product_type: ProductType, channel: Channel
    ) -> Policy | None:
        """Busca uma política ativa para um produto e canal"""
        pass
