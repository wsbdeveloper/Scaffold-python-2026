"""Pytest Configuration"""
import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from credit_engine.infrastructure.database.base import Base
from credit_engine.infrastructure.database.models import PolicyModel
from credit_engine.domain.value_objects.channel import Channel
from credit_engine.domain.value_objects.product_type import ProductType
from uuid import uuid4


@pytest.fixture(scope="function")
def db_session():
    """Cria uma sessão de banco de dados para testes"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Seed política padrão
    policy = PolicyModel(
        id=uuid4(),
        name="DEFAULT_POLICY_V1",
        version="1.0",
        product_types=[ProductType.PERSONAL_LOAN.value],
        channels=[Channel.APP.value, Channel.BACKOFFICE.value, Channel.PARTNER_X.value],
        is_active=True,
    )
    session.add(policy)
    session.commit()

    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

