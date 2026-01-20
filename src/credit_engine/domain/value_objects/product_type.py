"""Product Type Value Object"""
from enum import Enum


class ProductType(str, Enum):
    """Tipos de produto de crédito"""
    PERSONAL_LOAN = "PERSONAL_LOAN"
    PAYROLL_LOAN = "PAYROLL_LOAN"  # Exemplo de produto de crédito para folha de pagamento (deixei de exemplo para avaliação e de como seria num ambiente real)
    CREDIT_CARD = "CREDIT_CARD"  # Exemplo de produto de crédito para cartão de crédito (deixei de exemplo para avaliação e de como seria num ambiente real)


