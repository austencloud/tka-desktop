from enums.letter.letter import Letter


complementary_letter_mapping = {
    "A": "B",
    "B": "A",
    "C": "C",
    "D": "E",
    "E": "D",
    "F": "F",
    "G": "H",
    "H": "G",
    "I": "I",
    "J": "K",
    "K": "J",
    "L": "L",
    "M": "N",
    "N": "M",
    "O": "O",
    "P": "Q",
    "Q": "P",
    "R": "R",
    "S": "T",
    "T": "S",
    "U": "V",
    "V": "U",
    "W": "X",
    "X": "W",
    "Y": "Z",
    "Z": "Y",
    "Σ": "Δ",
    "Δ": "Σ",
    "θ": "Ω",
    "Ω": "θ",
    "W-": "X-",
    "X-": "W-",
    "Y-": "Z-",
    "Z-": "Y-",
    "Σ-": "Δ-",
    "Δ-": "Σ-",
    "θ-": "Ω-",
    "Ω-": "θ-",
    "Φ": "Φ",
    "Ψ": "Ψ",
    "Λ": "Λ",
    "Φ-": "Φ-",
    "Ψ-": "Ψ-",
    "Λ-": "Λ-",
    "α": "α",
    "β": "β",
    "Γ": "Γ",
}


class ComplementaryLetterGetter:

    @staticmethod
    def get_complimentary_letter(letter: str) -> Letter:
        return Letter(complementary_letter_mapping[letter])
