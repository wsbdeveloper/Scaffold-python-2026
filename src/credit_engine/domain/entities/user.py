"""Applicant Entity"""

from dataclasses import dataclass


@dataclass
class User:
    """Entidade que representa um usuário"""

    document_number: str
    name: str
    age: int

    # Validations and methods can be added here as needed
