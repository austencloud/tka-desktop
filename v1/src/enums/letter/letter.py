#
from enum import Enum
from functools import lru_cache
from typing import TYPE_CHECKING

from enums.letter.letter_condition import LetterCondition

if TYPE_CHECKING:
    from enums.letter.letter_type import LetterType


class Letter(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    Σ = "Σ"
    Δ = "Δ"
    θ = "θ"
    Ω = "Ω"
    W_DASH = "W-"
    X_DASH = "X-"
    Y_DASH = "Y-"
    Z_DASH = "Z-"
    Σ_DASH = "Σ-"
    Δ_DASH = "Δ-"
    θ_DASH = "θ-"
    Ω_DASH = "Ω-"
    Φ = "Φ"
    Ψ = "Ψ"
    Λ = "Λ"
    Φ_DASH = "Φ-"
    Ψ_DASH = "Ψ-"
    Λ_DASH = "Λ-"
    α = "α"
    β = "β"
    Γ = "Γ"

    @staticmethod
    @lru_cache(maxsize=None)  # Cache all unique callsFucking shit.
    def get_letters_by_condition(condition: LetterCondition) -> list["Letter"]:
        """
        Returns a list of letter enums based on a given condition.
        """
        from enums.letter.letter_condition_mappings import letter_condition_mappings

        return letter_condition_mappings.get(condition, [])

    @classmethod
    def from_string(cls, letter_str: str):
        """
        Convert a string to the corresponding enum member, including handling dashes.
        """
        # Attempt to find a direct match first
        for letter in cls:
            if letter.value == letter_str:
                return letter

        # If no direct match, try to convert dash-containing names
        normalized_str = letter_str.replace("-", "_DASH")
        if normalized_str in cls.__members__:
            return cls.__members__[normalized_str]

        # Raise an error if no match is found
        raise ValueError(f"No matching enum member for string: {letter_str}")

    def get_letter(letter_str: str) -> "Letter":
        return Letter(letter_str)

    def get_letter_type(self) -> "LetterType":
        from enums.letter.letter_type import LetterType

        return LetterType.get_letter_type(self)


