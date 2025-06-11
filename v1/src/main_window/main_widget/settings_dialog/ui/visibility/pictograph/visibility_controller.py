from typing import TYPE_CHECKING, Union
from base_widgets.pictograph.elements.grid.non_radial_points_group import (
    NonRadialPointsGroup,
)
from enums.glyph_enum import Glyph

if TYPE_CHECKING:
    from .visibility_pictograph_interaction_manager import (
        VisibilityPictographInteractionManager,
    )


class VisibilityController:
    """Controls visibility and opacity transitions for pictograph elements."""

    def __init__(self, manager: "VisibilityPictographInteractionManager") -> None:
        self.manager = manager

    def fade_and_toggle_visibility(
        self, item: Union[Glyph, NonRadialPointsGroup], new_visibility: bool
    ) -> None:
        """Fade an item to a new visibility state with callback handling."""
        target_opacity = 1.0 if new_visibility else 0.1

        # Set initial opacity if needed
        if new_visibility and item.opacity() < 1.0:
            item.setOpacity(1.0)

        # Access widget fader from main widget
        widget_fader = self.manager.pictograph.main_widget.fade_manager.widget_fader

        # Define callback for after fade completion
        def after_fade_complete():
            self._process_after_fade(item, new_visibility)

        # Start fade animation
        widget_fader.fade_visibility_items_to_opacity(
            item, target_opacity, 300, after_fade_complete
        )

    def _process_after_fade(
        self, item: Union[Glyph, NonRadialPointsGroup], new_visibility: bool
    ) -> None:
        """Process actions after fade animation completes."""
        if not hasattr(item, "name"):
            return

        if item.name == "non_radial_points":
            self.manager.toggler.toggle_non_radial_points(new_visibility)

        elif item.name in ["arrow", "prop"]:
            self.manager.toggler.toggle_prop_visibility(
                item.state.color, new_visibility
            )

            # Update reversal symbols for motion visibility changes
            if (
                hasattr(self.manager.pictograph.elements, "reversal_glyph")
                and self.manager.pictograph.elements.reversal_glyph
            ):
                self.manager.pictograph.elements.reversal_glyph.update_reversal_symbols(
                    is_visibility_pictograph=True
                )

        elif item.name == "Reversals":
            # Special handling for reversal glyph
            item.update_reversal_symbols(
                visible=new_visibility, is_visibility_pictograph=True
            )

        else:
            # For other glyphs
            self.manager.toggler.toggle_glyph_visibility(item.name, new_visibility)
