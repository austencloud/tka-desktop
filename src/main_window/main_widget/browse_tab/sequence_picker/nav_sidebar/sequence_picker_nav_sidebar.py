from PyQt6.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from .nav_sidebar_manager import NavSidebarManager
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from ..sequence_picker import SequencePicker


class SequencePickerNavSidebar(QWidget):
    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.settings_manager = AppContext.settings_manager()
        self.scroll_content = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.scroll_content)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.manager = NavSidebarManager(self)
        self.scroll_area = QScrollArea(self)
        self.setup_scroll_area()
        self.setup_main_layout()

    def setup_scroll_area(self):
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setStyleSheet("background: transparent;")

    def setup_main_layout(self):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def update_sidebar(self, sections, sort_order):
        self.manager.update_sidebar(sections, sort_order)

    def clear_sidebar(self):
        self.manager.clear_sidebar()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_sidebar()

    def resize_sidebar(self):
        if self.sequence_picker and self.sequence_picker.main_widget:
            fraction = 1 / 12.0
            new_width = int(self.sequence_picker.main_widget.width() * fraction)
            self.setFixedWidth(new_width)
        self.adjust_button_fonts()

    def adjust_button_fonts(self):
        for button in self.manager.buttons:
            font_size = self.sequence_picker.main_widget.width() // 80
            btn_font = button.font()
            btn_font.setPointSize(font_size)
            button.setFont(btn_font)
            button.resize_button()
