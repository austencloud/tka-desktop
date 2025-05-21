from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QPushButton,
    QLabel,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication
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
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Header section
        self.header_frame = QFrame()
        self.header_frame.setObjectName("sequenceCardHeader")
        self.header_frame.setStyleSheet(
            """
            #sequenceCardHeader {
                background-color: rgba(40, 40, 40, 0.7);
                border-radius: 8px;
            }
        """
        )
        self.header_layout = QVBoxLayout(self.header_frame)

        # Title
        self.title_label = QLabel("Sequence Card Exporter")
        self.title_label.setObjectName("sequenceCardTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: white;")

        # Description
        self.description_label = QLabel(
            "Select a sequence length and export printable cards"
        )
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setStyleSheet("color: #cccccc;")

        # Export button
        self.export_button = QPushButton("Export Pages as Images")
        self.export_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.export_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2a82da;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a92ea;
            }
            QPushButton:pressed {
                background-color: #1a72ca;
            }
        """
        )
        self.export_button.clicked.connect(
            self.page_exporter.export_all_pages_as_images
        )

        # Add widgets to header layout
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.description_label)
        self.header_layout.addWidget(
            self.export_button, 0, Qt.AlignmentFlag.AlignCenter
        )

        # Content section
        self.content_layout = QHBoxLayout()

        # Navigation sidebar
        self.nav_sidebar.setMaximumWidth(150)
        self.nav_sidebar.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.nav_sidebar.setStyleSheet(
            """
            background-color: rgba(40, 40, 40, 0.7);
            border-radius: 8px;
            padding: 10px;
        """
        )

        # Scroll area for sequence cards
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.scroll_area.setWidget(self.scroll_content)

        # Configure scroll layout
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)

        # Add widgets to content layout
        self.content_layout.addWidget(self.nav_sidebar, 1)
        self.content_layout.addWidget(self.scroll_area, 9)

        # Add sections to main layout
        self.layout.addWidget(self.header_frame)
        self.layout.addLayout(self.content_layout, 1)

        # Set the main layout
        self.setLayout(self.layout)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.initialized:
            self.setCursor(Qt.CursorShape.WaitCursor)

            # Update the description label to show loading status
            self.description_label.setText(
                "Generating sequence card images... Please wait"
            )

            # Process events to update the UI
            QApplication.processEvents()

            # Export all images first to ensure we have content to display
            print("Starting sequence card image export...")
            self.image_exporter.export_all_images()
            print("Sequence card image export complete")

            # Initialize the tab
            self.initialized = True

            # Refresh the sequence cards
            print("Refreshing sequence cards...")
            self.refresher.refresh_sequence_cards()
            print("Sequence card refresh complete")

            # Reset cursor
            self.setCursor(Qt.CursorShape.ArrowCursor)
