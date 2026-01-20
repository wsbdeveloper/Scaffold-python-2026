"""Channel Value Object"""
from enum import Enum


class Channel(str, Enum):
    """Canais de origem da proposta"""
    APP = "APP"
    BACKOFFICE = "BACKOFFICE"
    PARTNER_X = "PARTNER_X" # exemplo de canal de parceiro (deixei de exemplo para avaliação e de como seria num ambiente real)


