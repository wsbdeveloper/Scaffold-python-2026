"""Channel Value Object"""

from enum import Enum


class User(str, Enum):
    """Tipo de perfis de usuarios"""

    BACKOFFICE = "INTERNAL"
    PARTNER_X = "EXTERNAL"
