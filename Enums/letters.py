from enum import Enum
from functools import lru_cache


class LetterConditions(Enum):
    PRO = "pro"
    ANTI = "anti"
    DASH = "dash"
    HAS_STATIC = "static"
    ALPHA_ENDING = "alpha_ending"
    BETA_ENDING = "beta_ending"
    GAMMA_ENDING = "gamma_ending"
    ALPHA_STARTING = "alpha_starting"
    BETA_STARTING = "beta_starting"
    GAMMA_STARTING = "gamma_starting"
    FOUR_VARIATIONS = "four_variations"
    EIGHT_VARIATIONS = "eight_variations"
    SIXTEEN_VARIATIONS = "sixteen_variations"
    HYBRID = "hybrid"
    NON_HYBRID = "non_hybrid"
    TYPE1_HYBRID = "type1_hybrids"
    TYPE1_NON_HYBRID = "type1_non_hybrids"
    TYPE1 = "type1"
    TYPE2 = "type2"
    TYPE3 = "type3"
    TYPE4 = "type4"
    TYPE5 = "type5"
    TYPE6 = "type6"


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
    def get_letters_by_condition(condition: LetterConditions) -> list["Letter"]:
        """
        Returns a list of letter enums based on a given condition.
        """
        condition_mappings = {
            LetterConditions.PRO: [
                Letter.A,
                Letter.C,
                Letter.D,
                Letter.F,
                Letter.G,
                Letter.I,
                Letter.J,
                Letter.L,
                Letter.M,
                Letter.O,
                Letter.P,
                Letter.R,
                Letter.S,
                Letter.U,
                Letter.V,
                Letter.W,
                Letter.Y,
                Letter.Σ,
                Letter.θ,
                Letter.W_DASH,
                Letter.Y_DASH,
                Letter.Σ_DASH,
                Letter.θ_DASH,
            ],
            LetterConditions.ANTI: [
                Letter.B,
                Letter.C,
                Letter.E,
                Letter.F,
                Letter.H,
                Letter.I,
                Letter.K,
                Letter.L,
                Letter.N,
                Letter.O,
                Letter.Q,
                Letter.R,
                Letter.T,
                Letter.U,
                Letter.V,
                Letter.X,
                Letter.Z,
                Letter.Δ,
                Letter.Ω,
                Letter.X_DASH,
                Letter.Z_DASH,
                Letter.Δ_DASH,
                Letter.Ω_DASH,
            ],
            LetterConditions.DASH: [
                Letter.W_DASH,
                Letter.X_DASH,
                Letter.Y_DASH,
                Letter.Z_DASH,
                Letter.Σ_DASH,
                Letter.Δ_DASH,
                Letter.θ_DASH,
                Letter.Ω_DASH,
                Letter.Φ,
                Letter.Ψ,
                Letter.Λ,
                Letter.Φ_DASH,
                Letter.Ψ_DASH,
                Letter.Λ_DASH,
            ],
            LetterConditions.HAS_STATIC: [
                Letter.W,
                Letter.X,
                Letter.Y,
                Letter.Z,
                Letter.Σ,
                Letter.Δ,
                Letter.θ,
                Letter.Ω,
                Letter.Φ,
                Letter.Ψ,
                Letter.Λ,
                Letter.α,
                Letter.β,
                Letter.Γ,
            ],
            LetterConditions.ALPHA_ENDING: [
                Letter.A,
                Letter.B,
                Letter.C,
                Letter.D,
                Letter.E,
                Letter.F,
                Letter.W,
                Letter.X,
                Letter.W_DASH,
                Letter.X_DASH,
                Letter.Φ,
                Letter.Φ_DASH,
                Letter.α,
            ],
            LetterConditions.BETA_ENDING: [
                Letter.G,
                Letter.H,
                Letter.I,
                Letter.J,
                Letter.K,
                Letter.L,
                Letter.Y,
                Letter.Z,
                Letter.Y_DASH,
                Letter.Z_DASH,
                Letter.Ψ,
                Letter.Ψ_DASH,
                Letter.β,
            ],
            LetterConditions.GAMMA_ENDING: [
                Letter.M,
                Letter.N,
                Letter.O,
                Letter.P,
                Letter.Q,
                Letter.R,
                Letter.S,
                Letter.T,
                Letter.U,
                Letter.V,
                Letter.Σ,
                Letter.Δ,
                Letter.θ,
                Letter.Ω,
                Letter.Σ_DASH,
                Letter.Δ_DASH,
                Letter.θ_DASH,
                Letter.Ω_DASH,
                Letter.Λ,
                Letter.Λ_DASH,
                Letter.Γ,
            ],
            LetterConditions.ALPHA_STARTING: [
                Letter.A,
                Letter.B,
                Letter.C,
                Letter.J,
                Letter.K,
                Letter.L,
                Letter.Σ,
                Letter.Δ,
                Letter.θ_DASH,
                Letter.Ω_DASH,
                Letter.Ψ,
                Letter.Φ_DASH,
                Letter.α,
            ],
            LetterConditions.BETA_STARTING: [
                Letter.G,
                Letter.H,
                Letter.I,
                Letter.D,
                Letter.E,
                Letter.F,
                Letter.Σ_DASH,
                Letter.Δ_DASH,
                Letter.θ,
                Letter.Ω,
                Letter.Φ,
                Letter.Ψ_DASH,
                Letter.β,
            ],
            LetterConditions.GAMMA_STARTING: [
                Letter.M,
                Letter.N,
                Letter.O,
                Letter.P,
                Letter.Q,
                Letter.R,
                Letter.S,
                Letter.T,
                Letter.U,
                Letter.V,
                Letter.W,
                Letter.X,
                Letter.Y,
                Letter.Z,
                Letter.W_DASH,
                Letter.X_DASH,
                Letter.Y_DASH,
                Letter.Z_DASH,
                Letter.Λ,
                Letter.Λ_DASH,
                Letter.Γ,
            ],
            LetterConditions.FOUR_VARIATIONS: [
                Letter.Φ,
                Letter.Ψ,
                Letter.Λ,
                Letter.Φ_DASH,
                Letter.Ψ_DASH,
                Letter.Λ_DASH,
                Letter.α,
                Letter.β,
                Letter.Γ,
            ],
            LetterConditions.EIGHT_VARIATIONS: [
                Letter.A,
                Letter.B,
                Letter.D,
                Letter.E,
                Letter.G,
                Letter.H,
                Letter.J,
                Letter.K,
                Letter.M,
                Letter.N,
                Letter.P,
                Letter.Q,
            ],
            LetterConditions.SIXTEEN_VARIATIONS: [
                Letter.C,
                Letter.F,
                Letter.I,
                Letter.L,
                Letter.O,
                Letter.R,
                Letter.U,
                Letter.V,
                Letter.S,
                Letter.T,
                Letter.W,
                Letter.X,
                Letter.Y,
                Letter.Z,
                Letter.W_DASH,
                Letter.X_DASH,
                Letter.Y_DASH,
                Letter.Z_DASH,
                Letter.Σ,
                Letter.Δ,
                Letter.θ,
                Letter.Ω,
                Letter.Σ_DASH,
                Letter.Δ_DASH,
                Letter.θ_DASH,
                Letter.Ω_DASH,
            ],
            LetterConditions.HYBRID: [
                Letter.C,
                Letter.F,
                Letter.I,
                Letter.L,
                Letter.O,
                Letter.R,
                Letter.U,
                Letter.V,
                Letter.W,
                Letter.X,
                Letter.Y,
                Letter.Z,
                Letter.W_DASH,
                Letter.X_DASH,
                Letter.Y_DASH,
                Letter.Z_DASH,
                Letter.Σ,
                Letter.Δ,
                Letter.θ,
                Letter.Ω,
                Letter.Σ_DASH,
                Letter.Δ_DASH,
                Letter.θ_DASH,
                Letter.Ω_DASH,
                Letter.Φ,
                Letter.Ψ,
                Letter.Λ,
            ],
            LetterConditions.NON_HYBRID: [
                Letter.A,
                Letter.B,
                Letter.D,
                Letter.E,
                Letter.G,
                Letter.H,
                Letter.J,
                Letter.K,
                Letter.M,
                Letter.N,
                Letter.P,
                Letter.Q,
                Letter.S,
                Letter.T,
                Letter.Φ_DASH,
                Letter.Ψ_DASH,
                Letter.Λ_DASH,
                Letter.α,
                Letter.β,
                Letter.Γ,
            ],
            LetterConditions.TYPE1_HYBRID: [
                Letter.C,
                Letter.F,
                Letter.I,
                Letter.L,
                Letter.O,
                Letter.R,
                Letter.U,
                Letter.V,
            ],
            LetterConditions.TYPE1_NON_HYBRID: [
                Letter.A,
                Letter.B,
                Letter.D,
                Letter.E,
                Letter.G,
                Letter.H,
                Letter.J,
                Letter.K,
                Letter.M,
                Letter.N,
                Letter.P,
                Letter.Q,
                Letter.S,
                Letter.T,
            ],
            LetterConditions.TYPE1: [
                Letter.A,
                Letter.B,
                Letter.D,
                Letter.E,
                Letter.G,
                Letter.H,
                Letter.J,
                Letter.K,
                Letter.M,
                Letter.N,
                Letter.P,
                Letter.Q,
                Letter.S,
                Letter.T,
                Letter.C,
                Letter.F,
                Letter.I,
                Letter.L,
                Letter.O,
                Letter.R,
                Letter.U,
                Letter.V,
            ],
            LetterConditions.TYPE2: [
                Letter.W,
                Letter.X,
                Letter.Y,
                Letter.Z,
                Letter.Σ,
                Letter.Δ,
                Letter.θ,
                Letter.Ω,
            ],
            LetterConditions.TYPE3: [
                Letter.W_DASH,
                Letter.X_DASH,
                Letter.Y_DASH,
                Letter.Z_DASH,
                Letter.Σ_DASH,
                Letter.Δ_DASH,
                Letter.θ_DASH,
                Letter.Ω_DASH,
            ],
            LetterConditions.TYPE4: [Letter.Φ, Letter.Ψ, Letter.Λ],
            LetterConditions.TYPE5: [Letter.Φ_DASH, Letter.Ψ_DASH, Letter.Λ_DASH],
            LetterConditions.TYPE6: [Letter.α, Letter.β, Letter.Γ],
        }
        return condition_mappings.get(condition, [])

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
        return LetterType.get_letter_type(self)

from enum import Enum
from functools import lru_cache

class LetterType(Enum):
    Type1 = (
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
         "P", "Q", "R", "S", "T", "U", "V"],
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
