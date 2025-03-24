from typing import TYPE_CHECKING
from data.constants import BLUE, RED
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
        """Toggle visibility for all glyphs of a specific type in all other pictographs."""
        # State is already handled by the state manager
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()

        # Skip the visibility pictograph
        if self.visibility_tab.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph)
        elif self.visibility_tab.pictograph_view.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph_view.pictograph)

        # Apply visibility to other pictographs
        actual_state = state
        if name in ["TKA", "VTG", "Elemental", "Positions"]:
            actual_state = (
                state and self.visibility_tab.state_manager.are_all_motions_visible()
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
        # self._update_visibility_pictograph()

    def toggle_prop_visibility(self, color: str, state: bool):
        """Toggle visibility for props and arrows of a specific color."""
        self.settings.set_motion_visibility(color, state)

        # Update buttons to reflect new state
        if color.lower() == "red":
            self.visibility_tab.buttons_widget.glyph_buttons["Red Motion"].set_active(
                state
            )
        elif color.lower() == "blue":
            self.visibility_tab.buttons_widget.glyph_buttons["Blue Motion"].set_active(
                state
            )

        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        if self.visibility_tab.pictograph in pictographs:
            pictographs.pop(pictographs.index(self.visibility_tab.pictograph))

        # Update all pictographs
        for pictograph in pictographs:
            prop = pictograph.elements.props.get(color)
            arrow = pictograph.elements.arrows.get(color)
            if prop:
                prop.setVisible(state)
            if arrow:
                arrow.setVisible(state)
            if pictograph.elements.reversal_glyph:
                pictograph.elements.reversal_glyph.update_reversal_symbols()

        # Update dependent elements
        self.update_dependent_glyphs_visibility()
        # self._update_visibility_pictograph()

    def update_dependent_glyphs_visibility(self):
        """Update the visibility of glyphs that depend on motion visibility."""
        all_motions_visible = self.settings.are_all_motions_visible()
        any_motion_visible = self.settings.get_motion_visibility(
            RED
        ) or self.settings.get_motion_visibility(BLUE)

        # When only one motion is visible, handle specially
        if any_motion_visible and not all_motions_visible:
            # Keep only reversals and non-radial points
            for glyph_name in ["TKA", "VTG", "Elemental", "Positions"]:
                # Force these to invisible
                self.settings.set_glyph_visibility(glyph_name, False)

                # Update buttons to show them as disabled
                if glyph_name in self.visibility_tab.buttons_widget.glyph_buttons:
                    button = self.visibility_tab.buttons_widget.glyph_buttons[
                        glyph_name
                    ]
                    button.set_active(False)
        else:
            # Normal behavior when both motions visible or none visible
            for glyph_name in self.dependent_glyphs:
                user_intent = self.settings.get_user_intent_visibility(glyph_name)
                actual_state = user_intent and all_motions_visible
                self.settings.set_effective_visibility(glyph_name, actual_state)

                # Update buttons
                if glyph_name in self.visibility_tab.buttons_widget.glyph_buttons:
                    button = self.visibility_tab.buttons_widget.glyph_buttons[
                        glyph_name
                    ]
                    button.set_active(actual_state)

        # Update all pictographs
        self._update_all_pictographs()

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
                elif glyph_type == "TKA":
                    glyph.update_tka_glyph(visible=is_visible)
                else:
                    glyph.setVisible(is_visible)

        if pictograph.state.letter in ["α", "β", "Γ"]:
            pictograph.elements.start_to_end_pos_glyph.setVisible(False)

    def _update_all_pictographs(self):
        """
        Update all pictographs (except the visibility pictograph) based on current settings.
        """
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()

        # Skip the visibility pictograph
        if self.visibility_tab.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph)
        elif self.visibility_tab.pictograph_view.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph_view.pictograph)

        for pictograph in pictographs:
            # Update each glyph type
            for glyph_type in ["TKA", "VTG", "Elemental", "Positions", "Reversals"]:
                visibility = self.settings.get_effective_visibility(glyph_type)
                self._apply_glyph_visibility_to_pictograph(
                    pictograph, glyph_type, visibility
                )

            # Update motion visibility
            for color in ["red", "blue"]:
                visibility = self.settings.get_motion_visibility(color)
                prop = pictograph.elements.props.get(color)
                arrow = pictograph.elements.arrows.get(color)

                if prop:
                    prop.setVisible(visibility)
                if arrow:
                    arrow.setVisible(visibility)

                # Update reversal symbols if color visibility changed
                if pictograph.elements.reversal_glyph:
                    pictograph.elements.reversal_glyph.update_reversal_symbols()

            # Update non-radial points
            non_radial_visibility = self.settings.get_non_radial_visibility()
            pictograph.elements.grid.toggle_non_radial_points(non_radial_visibility)

    def _update_visibility_pictograph(self):
        """Update the visibility pictograph based on current settings."""
        pictograph = self.visibility_tab.pictograph

        # Update all glyphs
        for glyph_type in ["TKA", "VTG", "Elemental", "Positions", "Reversals"]:
            visibility = self.settings.get_effective_visibility(glyph_type)
            target_opacity = 1.0 if visibility else 0.1

            # For glyphs that exist in the visibility pictograph
            for glyph in pictograph.glyphs:
                if glyph.name == glyph_type:
                    # Always keep visible, just change opacity
                    glyph.setVisible(True)
                    glyph.setOpacity(target_opacity)

                    # Special handling for reversal glyph
                    if glyph_type == "Reversals":
                        # Make sure reversal symbols are visible but at proper opacity
                        for color in ["red", "blue"]:
                            if color in glyph.reversal_items:
                                color_visibility = self.settings.get_motion_visibility(
                                    color
                                )
                                color_opacity = 1.0 if color_visibility else 0.1
                                glyph.reversal_items[color].setVisible(True)
                                glyph.reversal_items[color].setOpacity(color_opacity)

                        # Ensure the whole glyph remains visible
                        glyph.setVisible(True)

        # Update motion visibility
        for color in ["red", "blue"]:
            visibility = self.settings.get_motion_visibility(color)
            target_opacity = 1.0 if visibility else 0.1

            prop = pictograph.elements.props.get(color)
            arrow = pictograph.elements.arrows.get(color)

            if prop:
                prop.setVisible(True)  # Always visible in visibility pictograph
                prop.setOpacity(target_opacity)
            if arrow:
                arrow.setVisible(True)  # Always visible in visibility pictograph
                arrow.setOpacity(target_opacity)

        # Update non-radial points
        non_radial_visibility = self.settings.get_non_radial_visibility()
        target_opacity = 1.0 if non_radial_visibility else 0.1

        # Get non-radial points and update them
        non_radial_points = pictograph.elements.grid.items.get(
            f"{pictograph.elements.grid.grid_mode}_nonradial"
        )
        if non_radial_points:
            non_radial_points.setVisible(True)  # Always visible
            non_radial_points.setOpacity(target_opacity)
