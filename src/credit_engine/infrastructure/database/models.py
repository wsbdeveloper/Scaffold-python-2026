"""Database Models"""
from datetime import datetime
from uuid import uuid4, UUID
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship

from .base import Base
from ...domain.value_objects.channel import Channel
from ...domain.value_objects.decision_status import DecisionStatus
from ...domain.value_objects.product_type import ProductType


class ApplicantModel(Base):
    """Modelo de banco para Applicant"""
    __tablename__ = "applicants"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    document_number = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    monthly_income = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ProposalModel(Base):
    """Modelo de banco para Proposal"""
    __tablename__ = "proposals"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    applicant_id = Column(PostgresUUID(as_uuid=True), ForeignKey("applicants.id"), nullable=False)
    requested_amount = Column(Float, nullable=False)
    installments = Column(Integer, nullable=False)
    product_type = Column(SQLEnum(ProductType), nullable=False)
    channel = Column(SQLEnum(Channel), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    applicant = relationship("ApplicantModel", backref="proposals")


class PolicyModel(Base):
    """Modelo de banco para Policy"""
    __tablename__ = "policies"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False, index=True)
    version = Column(String, nullable=False)
    product_types = Column(JSON, nullable=False)  # Lista de ProductType como JSON
    channels = Column(JSON, nullable=False)  # Lista de Channel como JSON
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DecisionModel(Base):
    """Modelo de banco para Decision"""
    __tablename__ = "decisions"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    proposal_id = Column(PostgresUUID(as_uuid=True), ForeignKey("proposals.id"), nullable=False, unique=True, index=True)
    status = Column(SQLEnum(DecisionStatus), nullable=False)
    policy_name = Column(String, nullable=False)
    policy_version = Column(String, nullable=False)
    rule_results = Column(JSON, nullable=False)  # Lista de RuleResult como JSON
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    proposal = relationship("ProposalModel", backref="decision")

