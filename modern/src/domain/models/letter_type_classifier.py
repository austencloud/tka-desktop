"""
Letter Type Classifier - Legacy Compatible Classification System

This module implements Legacy's exact letter type classification system for sectional assignment
in the option picker. The classifications are based on Legacy's letter_condition_mappings.py.
"""

from typing import Dict, List


class LetterTypeClassifier:
    """
    Legacy-compatible letter type classifier for option picker sectional assignment.

    This classifier uses Legacy's exact letter type definitions to ensure identical
    sectional assignment behavior in Modern's option picker.
    """

    # Legacy's exact letter type classifications from letter_condition_mappings.py
    TYPE1_LETTERS = [
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
    ]

    TYPE2_LETTERS = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]

    TYPE3_LETTERS = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"]

    TYPE4_LETTERS = ["Φ", "Ψ", "Λ"]

    TYPE5_LETTERS = ["Φ-", "Ψ-", "Λ-"]

    TYPE6_LETTERS = ["α", "β", "Γ"]

    @classmethod
    def get_letter_type(cls, letter: str) -> str:
        """
        Get the letter type for sectional assignment using Legacy's classification.

        Args:
            letter: The letter to classify (e.g., "D", "W", "Φ-", etc.)

        Returns:
            Letter type string ("Type1", "Type2", "Type3", "Type4", "Type5", "Type6")
            Defaults to "Type1" for unknown letters (Legacy behavior)
        """
        if letter in cls.TYPE1_LETTERS:
            return "Type1"
        elif letter in cls.TYPE2_LETTERS:
            return "Type2"
        elif letter in cls.TYPE3_LETTERS:
            return "Type3"
        elif letter in cls.TYPE4_LETTERS:
            return "Type4"
        elif letter in cls.TYPE5_LETTERS:
            return "Type5"
        elif letter in cls.TYPE6_LETTERS:
            return "Type6"
        else:
            # Legacy default fallback behavior
            return "Type1"

    @classmethod
    def get_all_letter_types(cls) -> List[str]:
        """Get all available letter types."""
        return ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"]

    @classmethod
    def get_letters_for_type(cls, letter_type: str) -> List[str]:
        """Get all letters that belong to a specific type."""
        type_mapping = {
            "Type1": cls.TYPE1_LETTERS,
            "Type2": cls.TYPE2_LETTERS,
            "Type3": cls.TYPE3_LETTERS,
            "Type4": cls.TYPE4_LETTERS,
            "Type5": cls.TYPE5_LETTERS,
            "Type6": cls.TYPE6_LETTERS,
        }
        return type_mapping.get(letter_type, [])

    @classmethod
    def get_classification_stats(cls) -> Dict[str, int]:
        """Get statistics about letter type classifications."""
        return {
            "Type1": len(cls.TYPE1_LETTERS),
            "Type2": len(cls.TYPE2_LETTERS),
            "Type3": len(cls.TYPE3_LETTERS),
            "Type4": len(cls.TYPE4_LETTERS),
            "Type5": len(cls.TYPE5_LETTERS),
            "Type6": len(cls.TYPE6_LETTERS),
        }
