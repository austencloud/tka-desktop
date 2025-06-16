# codex_letter_groups.py

from enums.letter.letter_type import LetterType

LETTER_TYPE_GROUPS = {
    LetterType.Type1: [
        ["A", "B", "C"],
        ["D", "E", "F"],
        ["G", "H", "I"],
        ["J", "K", "L"],
        ["M", "N", "O"],
        ["P", "Q", "R"],
        ["S", "T", "U", "V"],
    ],
    LetterType.Type2: [["W", "X"], ["Y", "Z"], ["Σ", "Δ"], ["θ", "Ω"]],
    LetterType.Type3: [["W-", "X-"], ["Y-", "Z-"], ["Σ-", "Δ-"], ["θ-", "Ω-"]],
    LetterType.Type4: [["Φ", "Ψ", "Λ"]],
    LetterType.Type5: [["Φ-", "Ψ-", "Λ-"]],
    LetterType.Type6: [["α", "β", "Γ"]],
}
