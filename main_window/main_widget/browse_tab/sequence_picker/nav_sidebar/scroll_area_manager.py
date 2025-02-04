from PyQt6.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_picker.nav_sidebar.sequence_picker_nav_sidebar import SequencePickerNavSidebar


class NavSidebarScrollManager:
    def __init__(self, nav_sidebar: "SequencePickerNavSidebar"):
        self.sidebar = nav_sidebar
        self.scroll_content = QWidget()
        self.layout = QVBoxLayout(self.scroll_content)
        self.scroll_area = QScrollArea(self.sidebar)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setStyleSheet("background: transparent;")
