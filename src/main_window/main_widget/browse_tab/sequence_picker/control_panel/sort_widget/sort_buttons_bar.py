from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
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
        self.selected_button: QPushButton | None = None
        self.settings_manager = AppContext.settings_manager()
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setLayout(self.layout)

        # Create label
        self.sort_by_label = QLabel("Sort:")
        self.sort_by_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(2)
        self.layout.addWidget(self.sort_by_label)
        self.layout.addStretch(1)

        # Create buttons
        self.buttons = {}
        for option in self.sort_options:
            btn = QPushButton(option.label)
            btn.clicked.connect(option.on_click)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[option.identifier] = btn
            self.layout.addWidget(btn)
            self.layout.addStretch(1)

        self.layout.addStretch(2)

        # Apply initial styling
        self.style_buttons()

    def highlight_button(self, identifier: str):
        """Update UI to show which button is selected."""
        if self.selected_button:
            self._style_button(self.selected_button, selected=False)

        if identifier in self.buttons:
            new_btn = self.buttons[identifier]
            self._style_button(new_btn, selected=True)
            self.selected_button = new_btn

    def style_buttons(self):
        """Apply styles to all buttons based on the current UI theme."""
        bg_type = self.settings_manager.global_settings.get_background_type()

        for button in self.buttons.values():
            selected = button == self.selected_button
            self._style_button(button, selected=selected)

    def _style_button(
        self, button: QPushButton, selected: bool = False, font_color: str = "white"
    ) -> None:
        """Applies styling to the given button."""
        btn_font = button.font()
        font_size = self.sort_widget.sequence_picker.main_widget.width() // 130
        btn_font.setPointSize(font_size)
        button.setFont(btn_font)
        button.setContentsMargins(10, 5, 10, 5)
        sort_by_font = self.sort_by_label.font()
        sort_by_font.setPointSize(int(font_size * 1.4))
        self.sort_by_label.setFont(sort_by_font)

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
        """Handles resizing to adjust styles dynamically."""
        self.style_buttons()
        super().resizeEvent(event)
