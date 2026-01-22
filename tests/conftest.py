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

    # Seeds here

    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
