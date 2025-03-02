from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QApplication
from PyQt6.QtCore import Qt

from settings_manager.global_settings.app_context import AppContext


if TYPE_CHECKING:
    from .sequence_picker import SequencePicker


class SequencePickerSortWidget(QWidget):
    """Widget for sorting the dictionary entries by sequence length, alphabetical order, or date added"""

    def __init__(self, sequence_picker: "SequencePicker") -> None:
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.main_widget = self.sequence_picker.main_widget
        self.browse_tab = self.sequence_picker.browse_tab
        self.settings_manager = AppContext.settings_manager()
        self.selected_button: QPushButton = None  # Track the selected button
        self._setup_sort_buttons()
        self._setup_layout()

    def _setup_sort_buttons(self):
        self.buttons: dict[str, QPushButton] = {}

        button_data = {
            "sort_by_length_button": {
                "text": "Sequence Length",
                "clicked": self.on_sort_by_length,
            },
            "sort_alphabetically_button": {
                "text": "Alphabetical",
                "clicked": self.on_sort_alphabetically,
            },
            "sort_date_added_button": {
                "text": "Date Added",
                "clicked": self.on_sort_by_date_added,
            },
            "sort_by_level_button": { 
                "text": "Level",
                "clicked": self.on_sort_by_level,
            },
        }

        for button_name, button_info in button_data.items():
            button = QPushButton(button_info["text"])
            button.clicked.connect(button_info["clicked"])
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[button_name] = button

    def on_sort_by_level(self):
        # QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.update_selected_button(self.buttons["sort_by_level_button"])
        self.settings_manager.browse_settings.set_sort_method("level")
        self.sequence_picker.sorter.sort_and_display_currently_filtered_sequences_by_method(
            "level"
        )
        self.browse_tab.sequence_picker.scroll_widget.scroll_area.verticalScrollBar().setValue(
            0
        )
        # QApplication.restoreOverrideCursor()

    def highlight_appropriate_button(self, sort_method):
        button_map = {
            "sequence_length": "sort_by_length_button",
            "date_added": "sort_date_added_button",
            "level": "sort_by_level_button",  # ✅ Added Level Sorting
            "alphabetical": "sort_alphabetically_button"
        }
        button_name = button_map.get(sort_method, "sort_alphabetically_button")
        self.update_selected_button(self.buttons[button_name])

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)

        self.sort_by_label = QLabel("Sort:")
        self.sort_by_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(2)
        self.layout.addWidget(self.sort_by_label)
        self.layout.addStretch(1)
        for button in self.buttons.values():
            self.layout.addWidget(button)
            self.layout.addStretch(1)

        self.layout.addStretch(2)

    def on_sort_by_length(self):
        self.update_selected_button(self.buttons["sort_by_length_button"])
        self.settings_manager.browse_settings.set_sort_method("sequence_length")
        self.sequence_picker.sorter.sort_and_display_currently_filtered_sequences_by_method(
            "sequence_length"
        )
        self.browse_tab.sequence_picker.scroll_widget.scroll_area.verticalScrollBar().setValue(
            0
        )

    def on_sort_alphabetically(self):
        self.update_selected_button(self.buttons["sort_alphabetically_button"])
        self.settings_manager.browse_settings.set_sort_method("alphabetical")
        self.sequence_picker.sorter.sort_and_display_currently_filtered_sequences_by_method(
            "alphabetical"
        )
        self.browse_tab.sequence_picker.scroll_widget.scroll_area.verticalScrollBar().setValue(
            0
        )

    def on_sort_by_date_added(self):
        self.update_selected_button(self.buttons["sort_date_added_button"])
        self.settings_manager.browse_settings.set_sort_method("date_added")
        self.sequence_picker.sorter.sort_and_display_currently_filtered_sequences_by_method(
            "date_added"
        )
        self.browse_tab.sequence_picker.scroll_widget.scroll_area.verticalScrollBar().setValue(
            0
        )

    def update_selected_button(self, button: QPushButton):
        if self.selected_button:
            self._style_button(self.selected_button, selected=False)
        self._style_button(button, selected=True)
        self.selected_button = button

    def _style_sort_by_label(self):
        sort_by_label_font = self.sort_by_label.font()
        sort_by_label_font.setPointSize(self.browse_tab.main_widget.width() // 100)
        self.sort_by_label.setFont(sort_by_label_font)

    def style_buttons(self):
        bg_type = self.settings_manager.global_settings.get_background_type()
        font_color = self.main_widget.font_color_updater.get_font_color(bg_type)
        for button in self.buttons.values():
            selected = button == self.selected_button
            self._style_button(button, selected=selected, font_color=font_color)

    def _style_button(
        self, button: QPushButton, selected: bool = False, font_color: str = "white"
    ) -> None:
        button_font = button.font()
        button_font.setPointSize(self.browse_tab.main_widget.width() // 130)
        button.setFont(button_font)
        button.setContentsMargins(10, 5, 10, 5)

        button_background_color = "lightgray" if font_color == "black" else "#555"
        hover_color = "lightgray" if font_color == "black" else "#555"
        if selected:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {button_background_color};
                    color: {font_color};
                    border-radius: 5px;
                    font-weight: bold;
                    padding: 5px;
                }}
                """
            )
        else:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    font-weight: bold;
                    color: {font_color};
                    padding: 5px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    background: {hover_color};
                }}
                """
            )

    def resizeEvent(self, event):
        self._style_sort_by_label()
        self.style_buttons()
        super().resizeEvent(event)
