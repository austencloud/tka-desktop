from typing import TYPE_CHECKING
from .event_assigner import EventAssigner
from .event_handler_factory import EventHandlerFactory
from .visibility_controller import VisibilityController

if TYPE_CHECKING:
    from base_widgets.pictograph.elements.views.visibility_pictograph_view import (
        VisibilityPictographView,
    )


class VisibilityPictographInteractionManager:
    """Main coordinator for pictograph interactions."""

    def __init__(self, view: "VisibilityPictographView") -> None:
        self.view = view
        self.pictograph = view.pictograph
        self.visibility_settings = view.visibility_settings
        self.toggler = self.view.tab.toggler

        self.event_assigner = EventAssigner(self)
        self.event_handler_factory = EventHandlerFactory(self)
        self.visibility_controller = VisibilityController(self)

        self.glyphs = view.pictograph.managers.get.glyphs()
        self.non_radial_points = self.pictograph.managers.get.non_radial_points()

        self._initialize_interactions()

    def _initialize_interactions(self) -> None:
        """Initialize all hover and click events for pictograph elements."""
        self.event_assigner.assign_all_events()
