"""Policy Repository Implementation"""

from sqlalchemy.orm import Session

from ...domain.entities.policy import Policy
from ...domain.repositories.policy_repository import PolicyRepository
from ...domain.value_objects.channel import Channel
from ...domain.value_objects.product_type import ProductType
from ..database.models import PolicyModel


class PolicyRepositoryImpl(PolicyRepository):
    """Implementação do repositório de políticas"""

    def __init__(self, db: Session):
        self.db = db

    async def get_by_product_and_channel(
        self, product_type: ProductType, channel: Channel
    ) -> Policy | None:
        """Busca uma política ativa para um produto e canal"""
        policies = self.db.query(PolicyModel).filter_by(is_active=True).all()

        for policy_model in policies:
            # Converte JSON de volta para enums
            product_types = [ProductType(pt) for pt in policy_model.product_types]
            channels = [Channel(c) for c in policy_model.channels]

            policy = self._to_entity(policy_model, product_types, channels)
            if policy.applies_to(product_type, channel):
                return policy

        return None

    def _to_entity(
        self, policy_model: PolicyModel, product_types: list[ProductType], channels: list[Channel]
    ) -> Policy:
        """Converte modelo para entidade"""
        return Policy(
            id=policy_model.id,
            name=policy_model.name,
            version=policy_model.version,
            product_types=product_types,
            channels=channels,
            is_active=policy_model.is_active,
        )
