from PyQt6.QtCore import QEvent
from typing import TYPE_CHECKING
from base_widgets.pictograph.elements.views.base_pictograph_view import (
    BasePictographView,
)
from data.constants import BLUE, RED
from main_window.main_widget.settings_dialog.ui.visibility.pictograph.visibility_pictograph_interaction_manager import (
    VisibilityPictographInteractionManager,
)

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.visibility.pictograph.visibility_pictograph import (
        VisibilityPictograph,
    )
    from main_window.main_widget.settings_dialog.ui.visibility.visibility_tab import (
        VisibilityTab,
    )


class VisibilityPictographView(BasePictographView):
    pictograph: "VisibilityPictograph"

    def __init__(self, tab: "VisibilityTab", pictograph: "VisibilityPictograph"):
        super().__init__(pictograph)
        self.tab = tab
        self.visibility_settings = tab.settings
        self.main_widget = tab.main_widget

        self.interaction_manager = VisibilityPictographInteractionManager(self)
        self.setStyleSheet("border: 2px solid black;")

    def resizeEvent(self, event: QEvent):
        available_height = self.tab.dialog.height()
        size = int(available_height * 0.55)
        self.setFixedSize(size, size)
        super().resizeEvent(event)

    def showEvent(self, event):
        for glyph in self.pictograph.glyphs:
            self.pictograph.update_opacity(
                glyph.name, self.pictograph.settings.get_glyph_visibility(glyph.name)
            )
        self.pictograph.update_opacity(
            "non_radial_points", self.pictograph.settings.get_non_radial_visibility()
        )
        for color in [RED, BLUE]:
            self.pictograph.update_opacity(
                color,
                self.pictograph.settings.get_motion_visibility(color),
            )
        return super().showEvent(event)
