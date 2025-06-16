from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from enums.letter.letter import Letter


@dataclass(frozen=True)
class DeterminationResult:
    letter: Optional[Letter]
    matched_attributes: dict[str, str]
