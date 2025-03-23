from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from objects.glyphs.reversal_glyph import ReversalGlyph
from objects.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
    StartToEndPosGlyph,
)
from data.constants import RED, BLUE
from enums.glyph_enum import Glyph

if TYPE_CHECKING:
    from objects.prop.prop import Prop
    from objects.arrow.arrow import Arrow
    from .visibility_pictograph_interaction_manager import (
        VisibilityPictographInteractionManager,
    )


class EventAssigner:
    """Assigns hover and click events to pictograph elements."""

    def __init__(self, manager: "VisibilityPictographInteractionManager") -> None:
        self.manager = manager

    def assign_all_events(self):
        """Assign events to all interactive elements."""
        self._assign_glyph_events()
        self._assign_prop_events()
        self._assign_arrow_events()
        self._assign_non_radial_point_events()

    def _assign_glyph_events(self):
        """Assign events to all glyphs."""
        for glyph in self.manager.glyphs:
            self._assign_events_to_glyph(glyph)

    def _assign_events_to_glyph(self, glyph: Glyph):
        """Assign events to a specific glyph."""
        glyph.mousePressEvent = (
            self.manager.event_handler_factory.create_glyph_click_handler(glyph)
        )
        glyph.setAcceptHoverEvents(True)
        glyph.hoverEnterEvent = (
            self.manager.event_handler_factory.create_hover_enter_handler(glyph)
        )
        glyph.hoverLeaveEvent = (
            self.manager.event_handler_factory.create_hover_leave_handler(glyph)
        )

        if isinstance(glyph, (StartToEndPosGlyph, ReversalGlyph)):
            for child in glyph.childItems():
                child.setCursor(Qt.CursorShape.PointingHandCursor)
                child.setAcceptHoverEvents(True)
                child.mousePressEvent = (
                    self.manager.event_handler_factory.create_glyph_click_handler(glyph)
                )
                child.hoverEnterEvent = (
                    self.manager.event_handler_factory.create_hover_enter_handler(child)
                )
                child.hoverLeaveEvent = (
                    self.manager.event_handler_factory.create_hover_leave_handler(child)
                )

    def _assign_prop_events(self):
        """Assign events to all props."""
        red_prop = self.manager.pictograph.elements.props.get(RED)
        blue_prop = self.manager.pictograph.elements.props.get(BLUE)

        if red_prop:
            self._assign_events_to_prop(red_prop, RED)
        if blue_prop:
            self._assign_events_to_prop(blue_prop, BLUE)

    def _assign_events_to_prop(self, prop: "Prop", color: str):
        """Assign events to a specific prop."""
        prop.setAcceptHoverEvents(True)
        prop.mousePressEvent = (
            self.manager.event_handler_factory.create_prop_click_handler(color)
        )
        prop.hoverEnterEvent = (
            self.manager.event_handler_factory.create_hover_enter_handler(prop)
        )
        prop.hoverLeaveEvent = (
            self.manager.event_handler_factory.create_hover_leave_handler(prop)
        )

    def _assign_arrow_events(self):
        """Assign events to all arrows."""
        red_arrow = self.manager.pictograph.elements.arrows.get(RED)
        blue_arrow = self.manager.pictograph.elements.arrows.get(BLUE)

        if red_arrow:
            self._assign_events_to_arrow(red_arrow, RED)
        if blue_arrow:
            self._assign_events_to_arrow(blue_arrow, BLUE)

    def _assign_events_to_arrow(self, arrow: "Arrow", color: str):
        """Assign events to a specific arrow."""
        arrow.setAcceptHoverEvents(True)
        arrow.mousePressEvent = (
            self.manager.event_handler_factory.create_prop_click_handler(color)
        )
        arrow.hoverEnterEvent = (
            self.manager.event_handler_factory.create_hover_enter_handler(arrow)
        )
        arrow.hoverLeaveEvent = (
            self.manager.event_handler_factory.create_hover_leave_handler(arrow)
        )

    def _assign_non_radial_point_events(self):
        """Assign events to non-radial points."""
        points = self.manager.non_radial_points
        points.setAcceptHoverEvents(True)
        points.mousePressEvent = (
            self.manager.event_handler_factory.create_non_radial_click_handler()
        )
        points.hoverEnterEvent = (
            self.manager.event_handler_factory.create_hover_enter_handler(points)
        )
        points.hoverLeaveEvent = (
            self.manager.event_handler_factory.create_hover_leave_handler(points)
        )
