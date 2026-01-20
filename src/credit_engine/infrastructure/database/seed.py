"""Database Seeding - Políticas padrão"""
from uuid import uuid4

from sqlalchemy.orm import Session

from ...domain.value_objects.channel import Channel
from ...domain.value_objects.product_type import ProductType
from .models import PolicyModel


def seed_default_policy(db: Session):
    """Cria a política padrão"""
    # Verifica se já existe
    existing = db.query(PolicyModel).filter_by(name="DEFAULT_POLICY_V1").first()
    if existing:
        return

    # Cria a política padrão (para teste é muito importante ter uma política padrão para testar a aplicação)
    policy = PolicyModel(
        id=uuid4(),
        name="DEFAULT_POLICY_V1",
        version="1.0",
        product_types=[ProductType.PERSONAL_LOAN.value],
        channels=[Channel.APP.value, Channel.BACKOFFICE.value, Channel.PARTNER_X.value],
        is_active=True,
    )
    db.add(policy)
    db.commit()
