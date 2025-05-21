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
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication
import os
from typing import TYPE_CHECKING

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from main_window.main_widget.sequence_card_tab.sequence_card_page_exporter import (
    SequenceCardPageExporter,
)
from utils.path_helpers import get_dictionary_path

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

        # Set up a timer to check for dictionary changes
        self.dictionary_check_timer = QTimer(self)
        self.dictionary_check_timer.timeout.connect(self.check_dictionary_changes)
        self.dictionary_check_timer.start(10000)  # Check every 10 seconds

        # Store the last modification time of the dictionary
        self.last_dictionary_mod_time = self.get_dictionary_mod_time()

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

        # Create refresh button
        self.refresh_button = QPushButton("Refresh Sequences")
        self.refresh_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.refresh_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2a82da;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #3a92ea;
            }
            QPushButton:pressed {
                background-color: #1a72ca;
            }
        """
        )
        self.refresh_button.clicked.connect(self.load_sequences)

        # Create regenerate button for batch exporting images
        self.regenerate_button = QPushButton("Regenerate All Images")
        self.regenerate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.regenerate_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2a82da;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #3a92ea;
            }
            QPushButton:pressed {
                background-color: #1a72ca;
            }
            """
        )
        self.regenerate_button.clicked.connect(self.regenerate_all_images)

        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.regenerate_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets to header layout
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.description_label)
        self.header_layout.addLayout(button_layout)

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
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setStyleSheet("background-color: transparent;")
        self.scroll_content.setStyleSheet("background-color: transparent;")
        self.scroll_area.setWidget(self.scroll_content)

        # Configure scroll layout for side-by-side pages
        self.scroll_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        self.scroll_layout.setSpacing(20)  # Increased spacing between rows
        self.scroll_layout.setContentsMargins(
            10, 20, 10, 20
        )  # Increased vertical margins

        # Add widgets to content layout
        self.content_layout.addWidget(self.nav_sidebar, 1)
        self.content_layout.addWidget(self.scroll_area, 9)

        # Add sections to main layout
        self.layout.addWidget(self.header_frame)
        self.layout.addLayout(self.content_layout, 1)

        # Set the main layout
        self.setLayout(self.layout)

    def get_dictionary_mod_time(self):
        """Get the latest modification time of the dictionary directory."""
        dictionary_path = get_dictionary_path()
        latest_mod_time = 0

        for root, _, files in os.walk(dictionary_path):
            for file in files:
                if file.endswith(".png") and not file.startswith("__"):
                    file_path = os.path.join(root, file)
                    mod_time = os.path.getmtime(file_path)
                    if mod_time > latest_mod_time:
                        latest_mod_time = mod_time

        return latest_mod_time

    def check_dictionary_changes(self):
        """Check if the dictionary has changed and reload if necessary."""
        current_mod_time = self.get_dictionary_mod_time()

        if current_mod_time > self.last_dictionary_mod_time:
            print("Dictionary has changed. Reloading sequences...")
            self.last_dictionary_mod_time = current_mod_time
            self.load_sequences()

    def load_sequences(self):
        """Load sequences directly from the dictionary."""
        # Clear the cache to force a reload
        self.pages_cache = {}

        # Load the sequences
        self.refresher.refresh_sequence_cards()

    def showEvent(self, event):
        super().showEvent(event)
        if not self.initialized:
            self.setCursor(Qt.CursorShape.WaitCursor)

            # Update the description label to show loading status
            self.description_label.setText("Loading sequence cards... Please wait")

            # Process events to update the UI
            QApplication.processEvents()

            # Initialize the tab
            self.initialized = True

            # Load sequences directly from the dictionary
            self.load_sequences()

            # Reset cursor
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def resizeEvent(self, event):
        """Handle resize events to maintain the two-column layout."""
        super().resizeEvent(event)

        # Only reload if we're initialized and have a selected length
        if self.initialized and hasattr(self.nav_sidebar, "selected_length"):
            # Reload the current view to adjust page sizes
            selected_length = self.nav_sidebar.selected_length

            # If we have cached pages for this length, update their sizes
            if selected_length in self.pages_cache:
                self.cached_page_displayer.display_cached_pages(selected_length)

    def regenerate_all_images(self):
        """Regenerate all sequence card images with consistent export settings."""
        # Show a loading cursor
        self.setCursor(Qt.CursorShape.WaitCursor)

        # Update the description label to show processing status
        original_text = self.description_label.text()
        self.description_label.setText(
            "Regenerating all sequence images... Please wait"
        )

        # Process events to update the UI
        QApplication.processEvents()

        try:
            # Run the image exporter
            self.image_exporter.export_all_images()

            # Clear the cache to force a reload with the new images
            self.pages_cache = {}

            # Reload the sequences
            self.load_sequences()

            # Update the description label to show success
            self.description_label.setText(
                "All sequence images regenerated successfully!"
            )

            # Set a timer to reset the description label after 3 seconds
            QTimer.singleShot(
                3000, lambda: self.description_label.setText(original_text)
            )

        except Exception as e:
            # Update the description label to show error
            self.description_label.setText(f"Error regenerating images: {str(e)}")

            # Set a timer to reset the description label after 5 seconds
            QTimer.singleShot(
                5000, lambda: self.description_label.setText(original_text)
            )

        finally:
            # Reset cursor
            self.setCursor(Qt.CursorShape.ArrowCursor)
