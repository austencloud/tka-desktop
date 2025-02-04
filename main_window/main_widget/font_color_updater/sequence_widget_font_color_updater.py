# sequence_widget_font_color_updater.py
from typing import TYPE_CHECKING
from .base_font_color_updater import BaseFontColorUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceWorkbenchFontColorUpdater(BaseFontColorUpdater):
    def __init__(self, main_widget: "MainWidget", font_color: str):
        super().__init__(font_color)
        self.main_widget = main_widget

    def update(self):
        sequence_widget = self.main_widget.sequence_widget
        self._apply_font_colors(
            [
                sequence_widget.current_word_label,
                sequence_widget.difficulty_label,
                sequence_widget.indicator_label,
            ]
        )
