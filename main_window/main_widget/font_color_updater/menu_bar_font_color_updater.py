# menu_bar_font_color_updater.py
from typing import TYPE_CHECKING
from .base_font_color_updater import BaseFontColorUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class MenuBarFontColorUpdater(BaseFontColorUpdater):
    def __init__(self, main_widget: "MainWidget", font_color: str):
        super().__init__(font_color)
        self.main_widget = main_widget

    def update(self):
        menu_bar = self.main_widget.menu_bar
        # for label, _ in menu_bar.selectors_widget.sections:
        #     self._apply_font_color(label)
