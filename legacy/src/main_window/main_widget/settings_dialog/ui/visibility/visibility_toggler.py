from typing import TYPE_CHECKING
from enums.glyph_enum import Glyph

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
    from main_window.main_widget.settings_dialog.ui.visibility.visibility_tab import (
        VisibilityTab,
    )


class VisibilityToggler:
    """Handles toggling visibility of pictograph elements across the application."""

    def __init__(self, visibility_tab: "VisibilityTab"):
        self.visibility_tab = visibility_tab
        self.main_widget = visibility_tab.main_widget

        # Get settings from dependency injection system
        try:
            settings_manager = self.main_widget.app_context.settings_manager
            self.settings = settings_manager.visibility
        except AttributeError:
            # Fallback for cases where app_context is not available
            self.settings = None
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "settings_manager not available during VisibilityToggler initialization"
            )

        self.dependent_glyphs = ["TKA", "VTG", "Elemental", "Positions"]

    def toggle_glyph_visibility(self, name: str, state: bool):
        """Toggle visibility for all glyphs of a specific type in all other pictographs."""
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()

        # Skip the visibility pictograph
        if self.visibility_tab.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph)
        elif self.visibility_tab.pictograph_view.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph_view.pictograph)

        # For dependent glyphs, check if both motions are visible
        actual_state = state
        if name in self.dependent_glyphs:
            all_motions_visible = self.settings.are_all_motions_visible()
            actual_state = state and all_motions_visible

        # Apply visibility to other pictographs
        for pictograph in pictographs:
            self._apply_glyph_visibility_to_pictograph(pictograph, name, actual_state)

    def toggle_non_radial_points(self, state: bool):
        """Toggle visibility for non-radial points in all pictographs."""
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()

        # Skip the visibility pictograph
        if self.visibility_tab.pictograph_view.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph_view.pictograph)

        for pictograph in pictographs:
            pictograph.elements.grid.toggle_non_radial_points(state)

        # Update settings
        self.settings.set_non_radial_visibility(state)

    def toggle_prop_visibility(self, color: str, state: bool):
        """Toggle visibility for props and arrows of a specific color in all pictographs."""
        # Update settings
        self.settings.set_motion_visibility(color, state)

        # Get all pictographs and update them
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()

        # Skip the visibility pictograph for settings update
        if self.visibility_tab.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph)

        # Make sure at least one motion remains visible
        other_color = "blue" if color == "red" else "red"
        if not state and not self.settings.get_motion_visibility(other_color):
            self.settings.set_motion_visibility(other_color, True)

        # Update prop visibility
        for pictograph in pictographs:
            prop = pictograph.elements.props.get(color)
            arrow = pictograph.elements.arrows.get(color)
            if prop:
                prop.setVisible(state)
            if arrow:
                arrow.setVisible(state)
            if pictograph.elements.reversal_glyph:
                pictograph.elements.reversal_glyph.update_reversal_symbols()

            # Update placement for props and arrows after visibility change
            # This ensures elements reposition themselves based on the new visibility state
            self._update_placements(pictograph)

        # Update dependent elements when motion visibility changes
        self.update_dependent_glyphs_visibility()

    def _update_placements(self, pictograph: "LegacyPictograph"):
        """Update arrow and prop placements for a pictograph."""
        if hasattr(pictograph.managers, "updater") and hasattr(
            pictograph.managers.updater, "placement_updater"
        ):
            # Use the pictograph's placement updater if available
            if pictograph.state.letter:
                pictograph.managers.updater.placement_updater.update()
        else:
            # Fall back to calling placement managers directly
            if pictograph.state.letter:
                if hasattr(pictograph.managers, "prop_placement_manager"):
                    pictograph.managers.prop_placement_manager.update_prop_positions()
                if hasattr(pictograph.managers, "arrow_placement_manager"):
                    pictograph.managers.arrow_placement_manager.update_arrow_placements()
                pictograph.update()

    def update_dependent_glyphs_visibility(self):
        """Update the visibility of glyphs that depend on motion visibility."""
        all_motions_visible = self.settings.are_all_motions_visible()

        # Update visibility of dependent glyphs
        for glyph_name in self.dependent_glyphs:
            # Get base visibility setting (user's preference)
            base_visibility = self.settings.settings.value(
                f"visibility/{glyph_name}",
                glyph_name == "TKA",  # TKA is visible by default
                type=bool,
            )

            # Calculate actual visibility based on motion visibility
            actual_visibility = base_visibility and all_motions_visible

            # Apply to all pictographs
            self.toggle_glyph_visibility(glyph_name, actual_visibility)

        # Update all pictographs
        self._update_all_pictographs()

    def _apply_glyph_visibility_to_pictograph(
        self, pictograph: "LegacyPictograph", glyph_type: str, is_visible: bool
    ):
        """Apply glyph visibility to a specific pictograph."""
        # Mapping of glyph types to pictograph elements
        glyph_mapping = {
            "VTG": pictograph.elements.vtg_glyph,
            "TKA": pictograph.elements.tka_glyph,
            "Elemental": pictograph.elements.elemental_glyph,
            "Positions": pictograph.elements.start_to_end_pos_glyph,
            "Reversals": pictograph.elements.reversal_glyph,
        }

        glyph: Glyph = glyph_mapping.get(glyph_type)
        if not glyph:
            return

        # Handle different glyph types appropriately
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

        # Special case for Greek letters
        if pictograph.state.letter in ["α", "β", "Γ"]:
            pictograph.elements.start_to_end_pos_glyph.setVisible(False)

    def _update_all_pictographs(self):
        """Update all pictographs (except the visibility pictograph) based on current settings."""
        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()

        # Skip the visibility pictograph
        if self.visibility_tab.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph)
        elif self.visibility_tab.pictograph_view.pictograph in pictographs:
            pictographs.remove(self.visibility_tab.pictograph_view.pictograph)

        for pictograph in pictographs:
            # Update each glyph type
            for glyph_type in ["TKA", "VTG", "Elemental", "Positions", "Reversals"]:
                # For dependent glyphs, check if both motions are visible
                if glyph_type in self.dependent_glyphs:
                    base_visibility = self.settings.settings.value(
                        f"visibility/{glyph_type}",
                        glyph_type == "TKA",  # TKA is visible by default
                        type=bool,
                    )
                    all_motions_visible = self.settings.are_all_motions_visible()
                    visibility = base_visibility and all_motions_visible
                else:
                    visibility = self.settings.settings.value(
                        f"visibility/{glyph_type}",
                        glyph_type == "Reversals",  # Reversals is visible by default
                        type=bool,
                    )

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

            # Update non-radial points
            non_radial_visibility = self.settings.get_non_radial_visibility()
            if pictograph.state.letter:
                pictograph.elements.grid.toggle_non_radial_points(non_radial_visibility)

            # Update placements after all visibility changes
            self._update_placements(pictograph)
