from typing import TYPE_CHECKING
from enums.glyph_enum import Glyph

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph
    from main_window.main_widget.settings_dialog.ui.visibility.visibility_tab import (
        VisibilityTab,
    )


class VisibilityToggler:
    def __init__(self, visibility_tab: "VisibilityTab"):
        self.visibility_tab = visibility_tab
        self.main_widget = visibility_tab.main_widget
        self.settings = self.main_widget.settings_manager.visibility

        self.dependent_glyphs = ["TKA", "VTG", "Elemental", "Positions"]

    def toggle_glyph_visibility(self, name: str, state: bool):
        """Toggle visibility for all glyphs of a specific type."""
        self.settings.set_real_glyph_visibility(name, state)
        actual_state = state and self.settings.are_all_motions_visible()
        self.settings.set_glyph_visibility(name, actual_state)
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        pictographs.pop(
            pictographs.index(self.visibility_tab.pictograph_view.pictograph)
        )
        for pictograph in pictographs:
            self._apply_glyph_visibility_to_pictograph(pictograph, name, actual_state)

    def toggle_non_radial_points(self, state: bool):
        """Toggle visibility for non-radial points."""
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        pictographs.pop(
            pictographs.index(self.visibility_tab.pictograph_view.pictograph)
        )
        for pictograph in pictographs:
            pictograph.elements.grid.toggle_non_radial_points(state)
        self.settings.set_non_radial_visibility(state)

    def toggle_prop_visibility(self, color: str, state: bool):
        """Toggle visibility for props and arrows of a specific color."""
        self.settings.set_motion_visibility(color, state)
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        if self.visibility_tab.pictograph in pictographs:
            pictographs.pop(pictographs.index(self.visibility_tab.pictograph))
        for pictograph in pictographs:
            prop = pictograph.elements.props.get(color)
            arrow = pictograph.elements.arrows.get(color)
            if prop:
                prop.setVisible(state)
            if arrow:
                arrow.setVisible(state)
            if pictograph.elements.reversal_glyph:
                pictograph.elements.reversal_glyph.update_reversal_symbols()
        self.update_dependent_glyphs_visibility()

    def update_dependent_glyphs_visibility(self):
        """Update the visibility of glyphs that depend on motion visibility."""
        all_motions_visible = self.settings.are_all_motions_visible()
        for glyph_name in self.dependent_glyphs:
            real_state = self.settings.get_real_glyph_visibility(glyph_name)
            actual_state = real_state and all_motions_visible
            self.settings.set_glyph_visibility(glyph_name, actual_state)
            pictographs = (
                self.main_widget.pictograph_collector.collect_all_pictographs()
            )
            if self.visibility_tab.pictograph in pictographs:
                pictographs.pop(pictographs.index(self.visibility_tab.pictograph))

            for pictograph in pictographs:
                self._apply_glyph_visibility_to_pictograph(
                    pictograph, glyph_name, actual_state
                )

            if glyph_name in self.visibility_tab.buttons_widget.glyph_buttons:
                button = self.visibility_tab.buttons_widget.glyph_buttons[glyph_name]
                button.set_active(actual_state)

    def _apply_glyph_visibility_to_pictograph(
        self, pictograph: "Pictograph", glyph_type: str, is_visible: bool
    ):
        """Apply glyph visibility to a specific pictograph."""
        glyph_mapping: dict[str, Glyph] = {
            "VTG": pictograph.elements.vtg_glyph,
            "TKA": pictograph.elements.tka_glyph,
            "Elemental": pictograph.elements.elemental_glyph,
            "Positions": pictograph.elements.start_to_end_pos_glyph,
            "Reversals": pictograph.elements.reversal_glyph,
        }
        glyphs = glyph_mapping.get(glyph_type, [])
        if not isinstance(glyphs, list):
            glyphs = [glyphs]

        for glyph in glyphs:
            if glyph:
                is_visibility_pictograph = hasattr(pictograph, "example_data")

                if glyph_type == "Reversals":
                    glyph.update_reversal_symbols(
                        visible=is_visible,
                        is_visibility_pictograph=is_visibility_pictograph,
                    )

        if pictograph.state.letter in ["α", "β", "Γ"]:
            pictograph.elements.start_to_end_pos_glyph.setVisible(False)
