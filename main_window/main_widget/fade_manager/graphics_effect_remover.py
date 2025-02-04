from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel

if TYPE_CHECKING:
    from .fade_manager import FadeManager


class GraphicsEffectRemover:
    def __init__(self, fade_manager: "FadeManager"):
        self.manager = fade_manager

    def clear_graphics_effects(self, widgets: list[QWidget] = []) -> None:
        """Remove all graphics effects from widgets and their children."""
        default_widgets = [
            self.manager.parallel_stack_fader.right_old_widget,
            self.manager.parallel_stack_fader.left_old_widget,
            self.manager.parallel_stack_fader.right_new_widget,
            self.manager.parallel_stack_fader.left_new_widget,
            self.manager.main_widget.right_stack.currentWidget(),
            self.manager.main_widget.left_stack.currentWidget(),
        ]
        widgets = default_widgets + widgets
        for widget in widgets:
            if widget:
                self._remove_all_graphics_effects(widget)

        # self._clear_visibility_tab_graphics_effects()

    def _clear_visibility_tab_graphics_effects(self):
        """Clear graphics effects specifically for the visibility tab."""
        visibility_tab = self.manager.main_widget.settings_dialog.visibility_tab
        if visibility_tab:
            for button in visibility_tab.buttons_widget.glyph_buttons.values():
                if button.graphicsEffect():
                    button.setGraphicsEffect(None)
            if visibility_tab.pictograph_view:
                for glyph in visibility_tab.pictograph.get.glyphs():
                    self.widget_fader = self.manager.widget_fader
                    items = self.widget_fader._get_corresponding_items(glyph)
                    for item in items:
                        if item.graphicsEffect():
                            item.setGraphicsEffect(None)
                if visibility_tab.pictograph.get.non_radial_points():
                    for (
                        point
                    ) in visibility_tab.pictograph.get.non_radial_points().child_points:
                        if point.graphicsEffect():
                            point.setGraphicsEffect(None)

    def _remove_all_graphics_effects(self, widget: QWidget):
        """Remove graphics effects recursively and reset widget visibility."""
        if widget.graphicsEffect():
            widget.setGraphicsEffect(None)
        if hasattr(widget, "children"):
            for child in widget.findChildren(QWidget):
                if child.graphicsEffect():
                    if child.__class__.__base__ != BaseIndicatorLabel:
                        child.setGraphicsEffect(None)
