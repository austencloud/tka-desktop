from PyQt6.QtCore import QEvent
from typing import TYPE_CHECKING
from base_widgets.base_pictograph.pictograph_view import PictographView
from .visibility_pictograph_interaction_manager import (
    VisibilityPictographInteractionManager,
)

if TYPE_CHECKING:
    from .visibility_pictograph import VisibilityPictograph
    from ..visibility_tab import VisibilityTab


class VisibilityPictographView(PictographView):
    pictograph: "VisibilityPictograph"

    def __init__(self, tab: "VisibilityTab", pictograph: "VisibilityPictograph"):
        super().__init__(pictograph)
        self.tab = tab
        self.visibility_settings = tab.settings
        self.main_widget = tab.main_widget

        self.interaction_manager = VisibilityPictographInteractionManager(self)
        self.setStyleSheet("border: 2px solid black;")

    def resizeEvent(self, event: QEvent):
        available_width = self.tab.dialog.width() - self.tab.buttons_widget.width()
        size = int(available_width * 0.7)
        self.setFixedSize(size, size)
        super().resizeEvent(event)
