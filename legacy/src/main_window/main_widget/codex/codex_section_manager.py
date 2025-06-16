from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from enums.letter.letter_type import LetterType
from base_widgets.pictograph.elements.views.codex_pictograph_view import (
    CodexPictographView,
)
from .codex_section_type_label import CodexSectionTypeLabel
from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph

if TYPE_CHECKING:
    from .codex import Codex


class CodexSectionManager:
    """Manages the loading and organization of pictograph sections in the Codex."""

    VERT_SPACING = 7
    HOR_SPACING = 7
    ROWS = [
        ["A", "B", "C", "D", "E", "F"],
        ["G", "H", "I", "J", "K", "L"],
        ["M", "N", "O", "P", "Q", "R"],
        ["S", "T", "U", "V"],
        ["W", "X", "Y", "Z"],
        ["Σ", "Δ", "θ", "Ω"],
        ["W-", "X-", "Y-", "Z-"],
        ["Σ-", "Δ-", "θ-", "Ω-"],
        ["Φ", "Ψ", "Λ"],
        ["Φ-", "Ψ-", "Λ-"],
        ["α", "β", "Γ"],
    ]

    def __init__(self, codex: "Codex"):
        self.codex = codex
        self.scroll_area = self.codex.scroll_area
        self.content_layout = self.scroll_area.content_layout
        self.codex_views: dict[str, "CodexPictographView"] = {}
        self.setup_sections()

    def setup_sections(self) -> None:
        for letter_type in LetterType:
            self._load_letter_type_section(letter_type)

    def _load_letter_type_section(self, letter_type: LetterType) -> None:
        type_label = CodexSectionTypeLabel(self.codex, letter_type)
        self._add_type_label(type_label)

        letters = letter_type.letters
        if not letters:
            return

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(self.VERT_SPACING)
        vertical_layout.setContentsMargins(0, 0, 0, 0)

        for _, row_letters in enumerate(self.ROWS):
            current_letters = [l for l in row_letters if l in letters]
            if not current_letters:
                continue

            row_layout = self._create_row_layout(current_letters)
            vertical_layout.addLayout(row_layout)

        self.content_layout.addLayout(vertical_layout)

    def _add_type_label(self, type_label: CodexSectionTypeLabel) -> None:
        self.content_layout.addSpacing(self.VERT_SPACING)
        self.content_layout.addWidget(
            type_label, alignment=Qt.AlignmentFlag.AlignHCenter
        )

        self.content_layout.addSpacing(self.VERT_SPACING)

    def _create_row_layout(self, row_letters: list[str]) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(self.HOR_SPACING)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        for letter_str in row_letters:
            self._add_pictograph_view(letter_str, layout)

        return layout

    def _add_pictograph_view(self, letter_str: str, layout: QHBoxLayout) -> None:
        p_dict = self.codex.data_manager.pictograph_data.get(letter_str)
        if p_dict is None:
            return

        if letter_str not in self.codex_views:
            pictograph = LegacyPictograph()
            view = CodexPictographView(pictograph, self.codex)
            pictograph.managers.updater.update_pictograph(p_dict)
            self.codex_views[letter_str] = view
        else:
            view = self.codex_views[letter_str]

        layout.addWidget(view)
