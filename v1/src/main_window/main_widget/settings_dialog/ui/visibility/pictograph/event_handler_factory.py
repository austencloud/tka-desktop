from typing import Union, TYPE_CHECKING
from PyQt6.QtCore import Qt
from base_widgets.pictograph.elements.grid.non_radial_points_group import (
    NonRadialPointsGroup,
)
from enums.glyph_enum import Glyph

if TYPE_CHECKING:
    from .visibility_pictograph_interaction_manager import (
        VisibilityPictographInteractionManager,
    )


class EventHandlerFactory:
    """Creates event handlers for different elements of the pictograph."""

    def __init__(self, manager: "VisibilityPictographInteractionManager") -> None:
        self.manager = manager

    def create_hover_enter_handler(self, item: "Union[Glyph, NonRadialPointsGroup]"):
        """Create a hover enter event handler for any item."""

        def hover_enter_event(event):
            cursor = Qt.CursorShape.PointingHandCursor
            item.setOpacity(0.5)
            item.setCursor(cursor)

            if hasattr(item, "name"):
                if item.name == "non_radial_points":
                    item.setOpacity(0.5)
                    for point in item.child_points:
                        point.setCursor(cursor)
                        point.setOpacity(0.5)
                elif item.name == "Reversals":
                    for child_group in item.reversal_items.values():
                        child_group.setCursor(cursor)
                        child_group.setOpacity(0.5)
                elif item.name == "TKA":
                    for child in item.get_all_items():
                        child.setCursor(cursor)
                        child.setOpacity(0.5)

        return hover_enter_event

    def create_hover_leave_handler(self, item: Union[Glyph, NonRadialPointsGroup]):
        """Create a hover leave event handler for any item."""

        def hover_leave_event(event):
            if hasattr(item, "name"):
                # Determine appropriate visibility based on item type
                if item.name != "non_radial_points" and item.name not in [
                    "arrow",
                    "prop",
                ]:
                    visibility = self.manager.visibility_settings.get_glyph_visibility(
                        item.name
                    )
                    self.manager.visibility_controller.fade_and_toggle_visibility(
                        item, visibility
                    )
                elif item.name not in ["arrow", "prop"]:
                    visibility = (
                        self.manager.visibility_settings.get_non_radial_visibility()
                    )
                    self.manager.visibility_controller.fade_and_toggle_visibility(
                        item, visibility
                    )
                else:
                    visibility = self.manager.visibility_settings.get_motion_visibility(
                        item.state.color
                    )
                    self.manager.visibility_controller.fade_and_toggle_visibility(
                        item, visibility
                    )

        return hover_leave_event

    def create_glyph_click_handler(self, glyph: Glyph):
        """Create a click event handler for a glyph."""

        def glyph_click_event(event):
            if glyph.name == "Reversals":
                self._handle_reversal_glyph_click(glyph)
            elif glyph.name in ["TKA", "VTG", "Elemental"]:
                self._handle_dependent_glyph_click(glyph)
            else:
                self._handle_independent_glyph_click(glyph)

        return glyph_click_event

    def _handle_reversal_glyph_click(self, glyph: Glyph):
        """Handle a click on a reversal glyph."""
        current_visibility = self.manager.visibility_settings.get_glyph_visibility(
            glyph.name
        )
        new_visibility = not current_visibility

        # Update settings
        self.manager.visibility_settings.set_glyph_visibility(
            glyph.name, new_visibility
        )

        self.manager.view.tab.buttons_widget.update_button_flags()

        # Update UI
        glyph.setVisible(new_visibility)
        glyph.update_reversal_symbols(visible=new_visibility)

    def _handle_dependent_glyph_click(self, glyph: Glyph):
        """Handle a click on a motion-dependent glyph."""
        current_visibility = self.manager.visibility_settings.get_glyph_visibility(
            glyph.name
        )
        new_visibility = not current_visibility

        # Update real state (user's intent)

        # Calculate actual visibility based on motion visibility
        actual_visibility = (
            new_visibility
            and self.manager.visibility_settings.are_all_motions_visible()
        )
        self.manager.visibility_settings.set_glyph_visibility(
            glyph.name, actual_visibility
        )

        # Update UI
        self.manager.view.tab.buttons_widget.update_button_flags()
        self.manager.visibility_controller.fade_and_toggle_visibility(
            glyph, actual_visibility
        )

    def _handle_independent_glyph_click(self, glyph: Glyph):
        """Handle a click on a non-dependent glyph."""
        current_visibility = self.manager.visibility_settings.get_glyph_visibility(
            glyph.name
        )
        new_visibility = not current_visibility

        # Update settings
        self.manager.visibility_settings.set_glyph_visibility(
            glyph.name, new_visibility
        )


        # Update UI
        self.manager.view.tab.buttons_widget.update_button_flags()
        self.manager.visibility_controller.fade_and_toggle_visibility(
            glyph, new_visibility
        )

    def create_prop_click_handler(self, color: str):
        """Create a click event handler for a prop or arrow."""

        def prop_click_event(event):
            current_visibility = self.manager.visibility_settings.get_motion_visibility(
                color
            )
            new_visibility = not current_visibility

            # Update state manager
            self.manager.view.tab.state_manager.set_motion_visibility(
                color, new_visibility
            )

            # Update local UI
            self.manager.view.tab.buttons_widget.update_button_flags()

            # Update all pictographs via toggler
            self.manager.toggler.toggle_prop_visibility(color, new_visibility)

            # Ensure local pictograph updates properly
            prop = self.manager.pictograph.elements.props.get(color)
            arrow = self.manager.pictograph.elements.arrows.get(color)

            if prop:
                prop.setOpacity(1.0 if new_visibility else 0.1)
            if arrow:
                arrow.setOpacity(1.0 if new_visibility else 0.1)

            # Update reversal UI
            reversal_glyph = self.manager.pictograph.elements.reversal_glyph
            if reversal_glyph and color in reversal_glyph.reversal_items:
                reversal_item = reversal_glyph.reversal_items[color]
                reversal_item.setOpacity(1.0 if new_visibility else 0.1)
                reversal_glyph.update_reversal_symbols(is_visibility_pictograph=True)

        return prop_click_event

    def create_non_radial_click_handler(self):
        """Create a click event handler for non-radial points."""

        def non_radial_click_event(event):
            current_visibility = (
                self.manager.visibility_settings.get_non_radial_visibility()
            )
            new_visibility = not current_visibility

            # Update settings
            self.manager.visibility_settings.set_non_radial_visibility(new_visibility)

            # Update UI
            self.manager.visibility_controller.fade_and_toggle_visibility(
                self.manager.non_radial_points, new_visibility
            )
            self.manager.view.tab.buttons_widget.update_button_flags()

        return non_radial_click_event
