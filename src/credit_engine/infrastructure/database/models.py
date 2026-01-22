"""Database Models"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from .base import Base


class UserModel(Base):
    """Modelo de banco para Applicant"""

    __tablename__ = "applicants"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    document_number = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    monthly_income = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
