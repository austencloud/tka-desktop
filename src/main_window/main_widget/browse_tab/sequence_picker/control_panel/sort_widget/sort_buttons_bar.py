from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from main_window.main_widget.browse_tab.sequence_picker.control_panel.sort_widget.sort_button import SortButton
from main_window.main_widget.browse_tab.sequence_picker.control_panel.sort_widget.sort_option import SortOption
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_picker.control_panel.sequence_picker_control_panel import (
        SequencePickerSortWidget,
    )


class SortButtonsBar(QWidget):
    """A horizontal bar containing sort buttons and a label 'Sort:'."""

    def __init__(
        self, sort_options: list[SortOption], sort_widget: "SequencePickerSortWidget"
    ) -> None:
        super().__init__(sort_widget)
        self.sort_widget = sort_widget
        self.sort_options = sort_options
        self.selected_button: SortButton | None = None
        self.settings_manager = AppContext.settings_manager()
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # Create label
        self.sort_by_label = QLabel("Sort:")
        self.sort_by_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(2)
        self.layout.addWidget(self.sort_by_label)
        self.layout.addStretch(1)

        # Create buttons using SortButton class
        self.buttons: dict[str, SortButton] = {}
        for option in self.sort_options:
            btn = SortButton(option.label, option.identifier)
            btn.clicked.connect(option.on_click)
            btn.clicked_signal.connect(self.highlight_button)
            self.buttons[option.identifier] = btn
            self.layout.addWidget(btn)
            self.layout.addStretch(1)

        self.layout.addStretch(2)

    def highlight_button(self, identifier: str):
        """Update UI to show which button is selected."""
        if self.selected_button:
            self.selected_button.set_selected(False)

        if identifier in self.buttons:
            new_btn = self.buttons[identifier]
            new_btn.set_selected(True)
            self.selected_button = new_btn

    def resizeEvent(self, event):
        """Handles resizing to adjust styles dynamically."""
        self._apply_font_sizes()
        super().resizeEvent(event)

    def _apply_font_sizes(self):
        """Applies font sizes to buttons and label based on the main widget width."""
        font_size = self.sort_widget.sequence_picker.main_widget.width() // 130
        sort_by_font_size = int(font_size * 1.4)

        # Update label font size
        sort_by_font = self.sort_by_label.font()
        sort_by_font.setPointSize(sort_by_font_size)
        self.sort_by_label.setFont(sort_by_font)

        # Update buttons font size
        for button in self.buttons.values():
            btn_font = button.font()
            btn_font.setPointSize(font_size)
            button.setFont(btn_font)
            button.setContentsMargins(10, 5, 10, 5)
