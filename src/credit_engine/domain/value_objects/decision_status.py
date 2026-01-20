"""Decision Status Value Object"""
from enum import Enum


class DecisionStatus(str, Enum):
    """Status da decisão de crédito"""

    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PENDING_DOCS = "PENDING_DOCS"
