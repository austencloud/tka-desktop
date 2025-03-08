from dataclasses import dataclass
from enums.letter.letter import Letter


@dataclass
class LetterDeterminationCase:
    name: str
    pictograph_data: dict[
        str, dict[str, str | int | float | dict[str, str | int | float]]
    ]
    expected: Letter
    description: str
    direction: str = "same"
    swap_prop_rot: bool = False
