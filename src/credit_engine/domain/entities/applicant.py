"""Applicant Entity"""
from dataclasses import dataclass


@dataclass
class Applicant:
    """Entidade que representa um solicitante de crédito"""

    document_number: str
    name: str
    monthly_income: float
    age: int

    def __post_init__(self):
        """Validações básicas"""
        if self.monthly_income < 0:
            raise ValueError("Monthly income must be positive")
        if self.age < 0 or self.age > 120:
            raise ValueError("Age must be between 0 and 120")
        if not self.document_number or not self.document_number.strip():
            raise ValueError("Document number is required")
        if not self.name or not self.name.strip():
            raise ValueError("Name is required")
