from typing import TYPE_CHECKING

from main_window.main_widget.font_color_updater.sequence_widget_font_color_updater import (
    SequenceWorkbenchFontColorUpdater,
)
from .base_font_color_updater import BaseFontColorUpdater
from .construct_tab_font_color_updater import ConstructTabFontColorUpdater
from .generate_tab_font_color_updater import GenerateTabFontColorUpdater
from .browse_tab_font_color_updater import BrowseTabFontColorUpdater
from .learn_tab_font_color_updater import LearnTabFontColorUpdater


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class FontColorUpdater:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.font_color = "white"

        self.sub_updater_classes: list[BaseFontColorUpdater] = [
            SequenceWorkbenchFontColorUpdater,
            ConstructTabFontColorUpdater,
            GenerateTabFontColorUpdater,
            BrowseTabFontColorUpdater,
            LearnTabFontColorUpdater,
            # WriteTabFontColorUpdater,
        ]

    def update_main_widget_font_colors(self, bg_type: str):
        self.font_color = self.get_font_color(bg_type)
        self._apply_main_widget_colors()

    @staticmethod
    def get_font_color(bg_type: str) -> str:
        return (
            "black" if bg_type in ["Rainbow", "AuroraBorealis", "Aurora"] else "white"
        )

    def _apply_main_widget_colors(self) -> None:
        for updater_cls in self.sub_updater_classes:
            instance: BaseFontColorUpdater = updater_cls(
                self.main_widget, self.font_color
            )
            instance.update()
