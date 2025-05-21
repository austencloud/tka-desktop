from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.sequence_card_tab.sequence_card_page_exporter import (
    SequenceCardPageExporter,
)


from .sequence_card_image_displayer import SequenceCardImageDisplayer
from .sequence_card_cached_page_displayer import SequenceCardCachedPageDisplayer
from .sequence_card_refresher import SequenceCardRefresher
from .sequence_card_page_factory import SequenceCardPageFactory
from .sequence_card_image_exporter import SequenceCardImageExporter
from .sequence_card_nav_sidebar import SequenceCardNavSidebar

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


from PyQt6.QtWidgets import QPushButton


class SequenceCardTab(QWidget):
    def __init__(
        self,
        main_widget: "MainWidget",
        settings_manager: ISettingsManager,
        json_manager: IJsonManager,
    ):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.settings_manager = settings_manager
        self.json_manager = json_manager
        self.global_settings = settings_manager.get_global_settings()
        self.pages: list[QWidget] = []
        self.pages_cache: dict[int, list[QWidget]] = {}
        self.initialized = False
        self.currently_displayed_length = 16
        self.nav_sidebar = SequenceCardNavSidebar(self)
        self.page_factory = SequenceCardPageFactory(self)
        self.cached_page_displayer = SequenceCardCachedPageDisplayer(self)
        self.image_displayer = SequenceCardImageDisplayer(self)
        self.refresher = SequenceCardRefresher(self)

        self.image_exporter = SequenceCardImageExporter(self)
        self.page_exporter = SequenceCardPageExporter(self)
        self.init_ui()
        self.background_manager = None

    def init_ui(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.top_layout: QHBoxLayout = QHBoxLayout()
        self.bottom_layout: QHBoxLayout = QHBoxLayout()
        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)
        self.setLayout(self.layout)

        export_button = QPushButton("Export Pages as Images")
        export_button.clicked.connect(self.page_exporter.export_all_pages_as_images)
        self.top_layout.addWidget(export_button)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.scroll_area.setWidget(self.scroll_content)

        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(0)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.bottom_layout.addWidget(self.nav_sidebar, 1)
        self.bottom_layout.addWidget(self.scroll_area, 15)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.initialized:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.initialized = True
            self.refresher.refresh_sequence_cards()
            self.setCursor(Qt.CursorShape.ArrowCursor)
