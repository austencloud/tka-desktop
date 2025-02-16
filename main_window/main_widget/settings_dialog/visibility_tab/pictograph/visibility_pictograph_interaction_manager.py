from typing import Union, TYPE_CHECKING
from PyQt6.QtCore import Qt
from base_widgets.pictograph.glyphs.beat_reversal_group import BeatReversalGroup
from base_widgets.pictograph.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
    StartToEndPosGlyph,
)
from base_widgets.pictograph.grid.grid import NonRadialPointsGroup
from Enums.Enums import Glyph

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.pictograph.visibility_pictograph_view import (
        VisibilityPictographView,
    )


class VisibilityPictographInteractionManager:
    """Manages glyph and non-radial point interactions for the pictograph view."""

    def __init__(self, view: "VisibilityPictographView"):
        self.view = view
        self.pictograph = view.pictograph
        self.visibility_settings = view.visibility_settings
        self.toggler = self.view.tab.toggler

        self.glyphs = view.pictograph.get.glyphs()
        self.non_radial_points = self.pictograph.get.non_radial_points()
        self._initialize_interactions()

    def _initialize_interactions(self):
        """Initialize all hover and click events for glyphs and non-radial points."""
        for glyph in self.glyphs:
            self._assign_glyph_events(glyph)
        self._assign_non_radial_point_events()

    def _assign_glyph_events(self, glyph: Glyph):
        """Assign hover and click events to a glyph."""
        glyph.mousePressEvent = self._create_click_event(glyph)
        glyph.setAcceptHoverEvents(True)
        glyph.hoverEnterEvent = self._create_hover_event(glyph, entering=True)
        glyph.hoverLeaveEvent = self._create_hover_event(glyph, entering=False)

        if isinstance(glyph, (StartToEndPosGlyph, BeatReversalGroup)):
            for child in glyph.childItems():
                child.setCursor(Qt.CursorShape.PointingHandCursor)
                child.setAcceptHoverEvents(True)
                child.mousePressEvent = self._create_click_event(glyph)
                child.hoverEnterEvent = self._create_hover_event(child, entering=True)
                child.hoverLeaveEvent = self._create_hover_event(child, entering=False)

    def _assign_non_radial_point_events(self):
        """Assign hover and click events to non-radial points."""
        self.non_radial_points.setAcceptHoverEvents(True)
        self.non_radial_points.mousePressEvent = self._create_non_radial_click_event()
        self.non_radial_points.hoverEnterEvent = self._create_hover_event(
            self.non_radial_points, entering=True
        )
        self.non_radial_points.hoverLeaveEvent = self._create_hover_event(
            self.non_radial_points, entering=False
        )

    def _create_hover_event(
        self, item: Union[Glyph, NonRadialPointsGroup], entering: bool
    ):
        """Create a hover event for entering or leaving."""

        def hoverEvent(event):
            cursor = Qt.CursorShape.PointingHandCursor
            if entering:
                item.setOpacity(0.5)
                item.setCursor(cursor)
                if item.name == "non_radial_points":
                    item.setOpacity(0.5)
                    for point in item.child_points:
                        point.setCursor(cursor)
                        point.setOpacity(0.5)  # Set opacity for the group
                elif item.name == "Reversals":
                    for child_group in item.reversal_items.values():
                        child_group.setCursor(cursor)
                        child_group.setOpacity(0.5)  # Set opacity for the group
                elif item.name == "TKA":
                    for child in item.get_all_items():
                        child.setCursor(cursor)
                        child.setOpacity(0.5)  # Set opacity for the group
            else:
                (
                    self.fade_and_toggle_visibility(
                        item, self.visibility_settings.get_glyph_visibility(item.name)
                    )
                    if item.name != "non_radial_points"
                    else self.fade_and_toggle_visibility(
                        item, self.visibility_settings.get_non_radial_visibility()
                    )
                )

        return hoverEvent

    def _create_click_event(self, glyph: Glyph):
        """Create a click event for toggling glyph visibility."""

        def clickEvent(event):
            current_visibility = self.visibility_settings.get_glyph_visibility(
                glyph.name
            )
            new_visibility = not current_visibility
            self.visibility_settings.set_glyph_visibility(glyph.name, new_visibility)
            self.view.tab.buttons_widget.update_button_flags()
            self.fade_and_toggle_visibility(glyph, new_visibility)

        return clickEvent

    def _create_non_radial_click_event(self):
        """Create a click event for toggling non-radial points visibility."""

        def clickEvent(event):
            current_visibility = self.visibility_settings.get_non_radial_visibility()
            new_visibility = not current_visibility
            self.visibility_settings.set_non_radial_visibility(new_visibility)
            self.fade_and_toggle_visibility(self.non_radial_points, new_visibility)
            self.view.tab.buttons_widget.update_button_flags()

        return clickEvent

    def fade_and_toggle_visibility(
        self, item: Union[Glyph, NonRadialPointsGroup], new_visibility
    ):
        target_opacity = 1.0 if new_visibility else 0.1

        if new_visibility and item.opacity() < 1.0:
            item.setOpacity(1.0)

        widget_fader = self.pictograph.main_widget.fade_manager.widget_fader
        widget_fader.fade_visibility_items_to_opacity(
            item,
            target_opacity,
            300,
            lambda: (
                self.toggler.toggle_non_radial_points(new_visibility)
                if item.name == "non_radial_points"
                else self.toggler.toggle_glyph_visibility(item.name, new_visibility)
            ),
        )
