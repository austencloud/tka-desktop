from enum import Enum
from functools import lru_cache

from enums.letter.letter import Letter


class LetterType(Enum):
    Type1 = (
        [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
        ],
        "Dual-Shift",
    )
    Type2 = (["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"], "Shift")
    Type3 = (["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"], "Cross-Shift")
    Type4 = (["Φ", "Ψ", "Λ"], "Dash")
    Type5 = (["Φ-", "Ψ-", "Λ-"], "Dual-Dash")
    Type6 = (["α", "β", "Γ"], "Static")

    def __init__(self, letters: list[str], description: str):
        self._letters = letters
        self._description = description

    @property
    def letters(self):
        return self._letters

    @property
    def description(self):
        return self._description

    @staticmethod
    def get_letter_type(letter: "Letter") -> "LetterType":
        """Takes a letter enum and returns the corresponding letter type."""
        letter_str = letter.value
        for letter_type in LetterType:
            if letter_str in letter_type.letters:
                return letter_type
        return None

    # I want a function that lets me pass in a string like "Type1" and get the corresponding enum member
    @classmethod
    def from_string(cls, type_str: str) -> "LetterType":
        for letter_type in cls:
            if letter_type.name == type_str:
                return letter_type
        raise ValueError(f"No matching enum member for string: {type_str}")

    @classmethod
    def sort_key(cls, letter_str: str) -> tuple[int, int]:
        """
        Return a tuple (type_index, letter_index).
        If letter_str isn't found in any type, return a large tuple (999,999).
        """
        # 1) Convert the string to your Letter enum
        from_string_letter = Letter.from_string(letter_str)
        if not from_string_letter:
            return (999, 999)

        # 2) Find which LetterType it belongs to
        letter_type = cls.get_letter_type(from_string_letter)
        if letter_type is None:
            return (999, 999)

        # 3) Figure out the LetterType's index among all LetterTypes
        type_index = list(cls).index(letter_type)

        # 4) Find position of letter_str in that type's .letters
        try:
            letter_index = letter_type.letters.index(letter_str)
        except ValueError:
            letter_index = 999

        return (type_index, letter_index)
