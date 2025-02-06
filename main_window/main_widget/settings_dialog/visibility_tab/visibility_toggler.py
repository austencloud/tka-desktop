from typing import TYPE_CHECKING
from Enums.Enums import Glyph
from base_widgets.base_pictograph.glyphs.beat_reversal_group import BeatReversalGroup

if TYPE_CHECKING:
    from base_widgets.base_pictograph.pictograph import Pictograph
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import (
        VisibilityTab,
    )


class VisibilityToggler:
    def __init__(self, visibility_tab: "VisibilityTab"):
        self.visibility_tab = visibility_tab
        self.main_widget = visibility_tab.main_widget
        self.settings = self.main_widget.settings_manager.visibility

    def toggle_glyph_visibility(self, name: str, state: int):
        """Toggle visibility for all glyphs of a specific type."""

        is_checked = state
        self.settings.set_glyph_visibility(name, state)

        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        for pictograph in pictographs:
            self._apply_glyph_visibility_to_pictograph(pictograph, name, is_checked)

    def _apply_glyph_visibility_to_pictograph(
        self, pictograph: "Pictograph", glyph_type: str, is_visible: bool
    ):
        """Apply glyph visibility to a specific pictograph."""
        glyph_mapping: dict[str, Glyph] = {
            "VTG": pictograph.vtg_glyph,
            "TKA": pictograph.tka_glyph,
            "Elemental": pictograph.elemental_glyph,
            "Positions": pictograph.start_to_end_pos_glyph,
            "Reversals": pictograph.reversal_glyph,  # Reference the BeatReversalGroup
        }
        glyphs = glyph_mapping.get(glyph_type, [])
        if not isinstance(glyphs, list):
            glyphs = [glyphs]

        for glyph in glyphs:
            if glyph:
                if glyph_type == "Reversals":
                    glyph.update_reversal_symbols(visible=is_visible)
                else:
                    glyph.setVisible(is_visible)

        if pictograph.letter in ["α", "β", "Γ"]:
            pictograph.start_to_end_pos_glyph.setVisible(False)

    def toggle_non_radial_points(self, state: bool):
        """Toggle visibility for non-radial points."""
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        for pictograph in pictographs:
            pictograph.grid.toggle_non_radial_points(state)
