# act_tab_font_color_updater.py
from typing import TYPE_CHECKING
from .base_font_color_updater import BaseFontColorUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class WriteTabFontColorUpdater(BaseFontColorUpdater):
    def __init__(self, main_widget: "MainWidget", font_color: str):
        super().__init__(font_color)
        self.main_widget = main_widget

    def update(self):
        act_tab = self.main_widget.write_tab
        act_sheet = self.main_widget.write_tab.act_sheet
        self._apply_font_color(act_sheet.act_header)
        self._apply_font_color(act_sheet.act_container)

        for thumbnail_box in act_tab.act_browser.thumbnail_boxes:
            self._apply_font_color(thumbnail_box.header)

        for box in act_sheet.act_container.cue_scroll.cue_frame.cue_boxes.values():
            for widget in [box.timestamp, box.cue_label]:
                self._apply_font_color(widget)
            for edit in [box.timestamp.edit, box.cue_label.edit]:
                self._apply_font_color(edit)

            box.setStyleSheet(f"#cue_box {{border-top: 1px solid {self.font_color};}}")
