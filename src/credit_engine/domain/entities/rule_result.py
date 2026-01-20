"""Rule Result Entity"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class RuleResult:
    """Resultado da avaliação de uma regra"""

    rule_code: str
    passed: bool
    message: Optional[str] = None
    metadata: Optional[dict] = None
