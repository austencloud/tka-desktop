from typing import TYPE_CHECKING

from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import (
    ALPHA1,
    BLUE,
    END_POS,
    LETTER,
    MOTION_TYPE,
    RED,
    START_POS,
    PRO,
    ALPHA3,
)
from PyQt6.QtWidgets import QGraphicsProxyWidget

if TYPE_CHECKING:
    from ..visibility_tab import VisibilityTab
    from base_widgets.pictograph.elements.views.visibility_pictograph_view import (
        VisibilityPictographView,
    )


class VisibilityPictograph(LegacyPictograph):
    """Special class for the visibility tab pictograph with improved visibility behavior."""

    example_data = {
        LETTER: "A",
        START_POS: ALPHA1,
        END_POS: ALPHA3,
        f"{BLUE}_{MOTION_TYPE}": PRO,
        f"{RED}_{MOTION_TYPE}": PRO,
    }
    view: "VisibilityPictographView" = None

    def __init__(self, tab: "VisibilityTab"):
        super().__init__()
        self.state.red_reversal = True
        self.state.blue_reversal = True
        self.tab = tab
        self.main_widget = tab.main_widget

        # Get services from dependency injection system
        try:
            # Get PictographDataLoader from dependency injection
            from main_window.main_widget.pictograph_data_loader import (
                PictographDataLoader,
            )

            pictograph_data_loader = self.main_widget.app_context.get_service(
                PictographDataLoader
            )
            pictograph_data = pictograph_data_loader.find_pictograph_data(
                self.example_data
            )

            # Get settings_manager from dependency injection
            settings_manager = self.main_widget.app_context.settings_manager
            self.settings = settings_manager.visibility

            self.managers.updater.update_pictograph(pictograph_data)
        except (AttributeError, KeyError) as e:
            # Fallback for cases where services are not available during initialization
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Services not available during VisibilityPictograph initialization: {e}"
            )

            # Create a minimal pictograph data for fallback
            self.settings = None
            # Don't update pictograph if services aren't available
        self.glyphs = self.managers.get.glyphs()
        self.motion_set = self.managers.get.motions()

        # Initially make everything visible
        for glyph in self.glyphs:
            glyph.setVisible(True)
        self.elements.grid.toggle_non_radial_points(True)
        for motion in self.motion_set.values():
            motion.prop.setVisible(True)
            motion.arrow.setVisible(True)

        # Create dependency notice label

        # Register for state updates
        tab.state_manager.register_observer(
            self._update_from_state_manager, ["glyph", "motion", "non_radial"]
        )

        # Initial update
        self._update_from_state_manager()
        for arrow in self.elements.arrows.values():
            # make it unselectable
            arrow.setFlag(QGraphicsProxyWidget.GraphicsItemFlag.ItemIsSelectable, False)

    def _update_from_state_manager(self):
        """Update pictograph display based on the current state."""
        state_manager = self.tab.state_manager
        all_motions_visible = state_manager.are_all_motions_visible()

        # Update glyphs - actually hide dependent glyphs when not all motions are visible
        for glyph_type in ["TKA", "VTG", "Elemental", "Positions", "Reversals"]:
            is_dependent = glyph_type in ["TKA", "VTG", "Elemental", "Positions"]
            base_visibility = state_manager.get_glyph_visibility(glyph_type)

            # For dependent glyphs, check if they should be visible
            visibility = base_visibility
            if is_dependent and not all_motions_visible:
                visibility = False

            for glyph in self.glyphs:
                if glyph.name == glyph_type:
                    if visibility:
                        glyph.setVisible(True)
                        glyph.setOpacity(1.0)
                    else:
                        # For the visibility pictograph, use opacity for non-dependent glyphs,
                        # but actually hide dependent glyphs when motions are not visible
                        if is_dependent and not all_motions_visible:
                            glyph.setVisible(False)
                        else:
                            glyph.setVisible(True)
                            glyph.setOpacity(0.1)

        # Update motions
        for color in ["red", "blue"]:
            visibility = state_manager.get_motion_visibility(color)

            prop = self.elements.props.get(color)
            arrow = self.elements.arrows.get(color)

            if prop:
                prop.setVisible(True)  # Always visible in pictograph
                prop.setOpacity(1.0 if visibility else 0.1)
            if arrow:
                arrow.setVisible(True)  # Always visible in pictograph
                arrow.setOpacity(1.0 if visibility else 0.1)

            # Update reversal items for this color
            if (
                self.elements.reversal_glyph
                and color in self.elements.reversal_glyph.reversal_items
            ):
                reversal_visibility = state_manager.get_glyph_visibility("Reversals")
                reversal_item = self.elements.reversal_glyph.reversal_items[color]
                reversal_item.setVisible(reversal_visibility)
                reversal_item.setOpacity(1.0 if visibility else 0.1)

        # Update non-radial points
        non_radial_visibility = state_manager.get_non_radial_visibility()

        non_radial_points = self.elements.grid.items.get(
            f"{self.elements.grid.grid_mode}_nonradial"
        )
        if non_radial_points:
            non_radial_points.setVisible(
                True
            )  # Always visible in visibility pictograph
            non_radial_points.setOpacity(1.0 if non_radial_visibility else 0.1)

    def update_opacity(self, element_name: str, state: bool):
        """Animate the opacity of the corresponding element."""
        target_opacity = 1.0 if state else 0.1
        all_motions_visible = self.settings.are_all_motions_visible()

        # Handle props and arrows by color
        if element_name in [RED, BLUE]:
            prop = self.elements.props.get(element_name)
            arrow = self.elements.arrows.get(element_name)

            if prop:
                self.main_widget.fade_manager.widget_fader.fade_visibility_items_to_opacity(
                    prop, target_opacity
                )
            if arrow:
                self.main_widget.fade_manager.widget_fader.fade_visibility_items_to_opacity(
                    arrow, target_opacity
                )

            # Also update the reversal if this is a prop color
            if self.elements.reversal_glyph:
                reversal_item = self.elements.reversal_glyph.reversal_items.get(
                    element_name
                )
                if reversal_item:
                    self.main_widget.fade_manager.widget_fader.fade_visibility_items_to_opacity(
                        reversal_item, target_opacity
                    )

                # Always update the whole reversal glyph positioning
                self.elements.reversal_glyph.update_reversal_symbols(
                    is_visibility_pictograph=True
                )

        # Handle existing glyph case
        elif element_name in ["TKA", "Reversals", "VTG", "Elemental", "Positions"]:
            is_dependent = element_name in ["TKA", "VTG", "Elemental", "Positions"]

            for glyph in self.glyphs:
                if glyph.name == element_name:
                    # For dependent glyphs, check if they should be visible based on motions
                    if is_dependent and not all_motions_visible:
                        glyph.setVisible(False)
                    else:
                        glyph.setVisible(True)
                        self.main_widget.fade_manager.widget_fader.fade_visibility_items_to_opacity(
                            glyph, target_opacity
                        )

        # Handle non-radial points
        elif element_name == "non_radial_points":
            non_radial_points = self.elements.grid.items.get(
                f"{self.elements.grid.grid_mode}_nonradial"
            )
            if non_radial_points:
                self.main_widget.fade_manager.widget_fader.fade_visibility_items_to_opacity(
                    non_radial_points, target_opacity
                )
