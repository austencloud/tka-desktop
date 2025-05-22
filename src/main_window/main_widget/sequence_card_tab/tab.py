# src/main_window/main_widget/sequence_card_tab/tab.py
import os
import gc
import psutil
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QPushButton,
    QLabel,
    QFrame,
    QSizePolicy,
    QApplication,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from interfaces.settings_manager_interface import ISettingsManager
from interfaces.json_manager_interface import IJsonManager
from utils.path_helpers import (
    get_sequence_card_image_exporter_path,
    get_dictionary_path,
)

# Import components using new structure
from .components.navigation.sidebar import SequenceCardNavSidebar
from .components.pages.factory import SequenceCardPageFactory
from .components.pages.printable_factory import PrintablePageFactory
from .components.pages.printable_layout import PaperSize, PaperOrientation
from .export.image_exporter import SequenceCardImageExporter
from .export.page_exporter import SequenceCardPageExporter
from .components.display.simple_displayer import SimpleSequenceCardDisplayer
from .components.display.printable_displayer import PrintableDisplayer

# Use printable displayer for optimized print layout
USE_PRINTABLE_LAYOUT = True

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceCardTab(QWidget):
    """Optimized sequence card tab with smooth performance and no UI blocking."""

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

        # State management
        self.pages = []
        self.initialized = False
        self.currently_displayed_length = 16

        # Performance tracking
        self.load_start_time = 0
        self.memory_check_timer = QTimer(self)
        self.memory_check_timer.timeout.connect(self._check_memory_usage)
        self.memory_check_timer.start(30000)  # Check every 30 seconds

        # Dictionary change monitoring
        self.dictionary_check_timer = QTimer(self)
        self.dictionary_check_timer.timeout.connect(self.check_dictionary_changes)
        self.dictionary_check_timer.start(10000)  # Check every 10 seconds
        self.last_dictionary_mod_time = self.get_dictionary_mod_time()

        # Initialize components
        self._create_components()
        self.init_ui()

    def _create_components(self):
        """Create all components with proper initialization order."""
        # Core components that other components depend on
        self.nav_sidebar = SequenceCardNavSidebar(self)

        # Create appropriate page factory based on layout mode
        if USE_PRINTABLE_LAYOUT:
            self.page_factory = PrintablePageFactory(self)
        else:
            self.page_factory = SequenceCardPageFactory(self)

        # Create appropriate displayer based on layout mode
        if USE_PRINTABLE_LAYOUT:
            self.printable_displayer = PrintableDisplayer(self)
            # Set default paper size and orientation
            self.printable_displayer.set_paper_size(PaperSize.A4)
            self.printable_displayer.set_orientation(PaperOrientation.PORTRAIT)
            # Set default columns per row (page previews side-by-side)
            self.printable_displayer.set_columns_per_row(2)

        # Always create simple displayer as fallback
        self.simple_displayer = SimpleSequenceCardDisplayer(self)

        # Export functionality
        self.image_exporter = SequenceCardImageExporter(self)
        self.page_exporter = SequenceCardPageExporter(self)

        # Initialize empty pages list
        self.pages = []

    def init_ui(self):
        """Initialize UI with optimized layout and styling."""
        # Main layout
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Header section with modern styling
        self.header_frame = self._create_header()
        self.layout.addWidget(self.header_frame)

        # Content section
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(15)

        # Navigation sidebar with optimized width
        sidebar_width = 200
        self.nav_sidebar.setFixedWidth(sidebar_width)
        self.nav_sidebar.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )
        self.nav_sidebar.setStyleSheet(
            """
            SequenceCardNavSidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                border-radius: 10px;
                border: 1px solid #4a5568;
                padding: 8px;
                margin-right: 10px;
            }
        """
        )

        # Main content area (scroll area or virtualized view)
        self._create_main_content_area()

        # Add to content layout
        self.content_layout.addWidget(self.nav_sidebar, 0)
        self.content_layout.addWidget(self.scroll_area, 1)

        # Add content to main layout
        self.layout.addLayout(self.content_layout, 1)

        # Connect navigation signals
        if hasattr(self.nav_sidebar, "length_selected"):
            self.nav_sidebar.length_selected.connect(self._on_length_selected)

    def _create_header(self) -> QFrame:
        """Create optimized header with better styling."""
        header_frame = QFrame()
        header_frame.setObjectName("sequenceCardHeader")
        header_frame.setStyleSheet(
            """
            #sequenceCardHeader {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34495e, stop:1 #2c3e50);
                border-radius: 10px;
                border: 1px solid #4a5568;
            }
        """
        )

        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.setSpacing(8)

        # Title with better typography
        self.title_label = QLabel("Sequence Card Manager")
        self.title_label.setObjectName("sequenceCardTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setWeight(QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #ffffff; letter-spacing: 0.5px;")

        # Status/description label
        self.description_label = QLabel("Select a sequence length to view cards")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label.setStyleSheet(
            """
            color: #bdc3c7;
            font-size: 13px;
            font-style: italic;
        """
        )

        # Button layout with better spacing
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        # Styled buttons
        self.export_button = self._create_action_button(
            "Export Pages", self.page_exporter.export_all_pages_as_images
        )
        self.refresh_button = self._create_action_button("Refresh", self.load_sequences)
        self.regenerate_button = self._create_action_button(
            "Regenerate Images", self.regenerate_all_images
        )

        button_layout.addStretch()
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.regenerate_button)
        button_layout.addStretch()

        # Add to header
        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.description_label)
        header_layout.addLayout(button_layout)

        return header_frame

    def _create_action_button(self, text: str, callback) -> QPushButton:
        """Create consistently styled action button."""
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        button.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: 1px solid #5dade2;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 12px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
                border: 1px solid #85c1e9;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1f618d);
                border: 1px solid #3498db;
            }
        """
        )
        return button

    def _create_main_content_area(self):
        """Create main content area with scroll area."""
        # Traditional scroll area (always available)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # Scroll content
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        # Configure scroll layout
        self.scroll_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        self.scroll_layout.setSpacing(20)
        self.scroll_layout.setContentsMargins(10, 20, 10, 20)

        # Styling
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                background-color: #f8f9fa;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(0,0,0,0.1);
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0,0,0,0.3);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0,0,0,0.5);
            }
        """
        )

    def _on_length_selected(self, length: int):
        """Handle length selection with appropriate displayer based on layout mode."""
        # Store the selected length
        self.currently_displayed_length = length

        # Save the selected length in settings for persistence
        if hasattr(self, "settings_manager") and hasattr(
            self.settings_manager, "sequence_card_tab_settings"
        ):
            self.settings_manager.sequence_card_tab_settings.set_last_length(length)

        # Clear any instruction labels
        self._clear_scroll_layout()

        # Show loading indicator in the description label
        self.description_label.setText(
            f"Loading {length if length > 0 else 'all'}-step sequences..."
        )
        QApplication.processEvents()

        # Use appropriate displayer based on layout mode
        if USE_PRINTABLE_LAYOUT and hasattr(self, "printable_displayer"):
            # Use printable displayer for optimized print layout
            self.printable_displayer.display_sequences(length)
        elif hasattr(self, "simple_displayer"):
            # Fall back to simple displayer
            self.simple_displayer.display_sequences(length)
        else:
            print("Error: No displayer available")

    def showEvent(self, event):
        """Optimized show event with deferred initialization."""
        super().showEvent(event)
        if not self.initialized:
            self.initialized = True

            # Initialize the UI without loading sequences
            self.setCursor(Qt.CursorShape.WaitCursor)
            QTimer.singleShot(50, self._initialize_content)

    def _initialize_content(self):
        """Initialize content without loading sequences automatically."""
        try:
            # Check if we need to generate images, but don't load them yet
            images_path = get_sequence_card_image_exporter_path()
            images_exist = self._has_sequence_images(images_path)

            if not images_exist:
                # We need to generate images first
                self.description_label.setText("Generating sequence images...")
                QApplication.processEvents()

                # Generate images
                if hasattr(self.image_exporter, "export_all_images"):
                    self.image_exporter.export_all_images()

            # Show instruction to select a length from the sidebar
            self._show_selection_instructions()

            # Highlight the sidebar to draw attention to it
            self._highlight_sidebar()

        except Exception as e:
            print(f"Error initializing content: {e}")
            self.description_label.setText(f"Error: {str(e)}")
        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _show_selection_instructions(self):
        """Show instructions to select a length from the sidebar."""
        # Create a label with instructions
        instruction_label = QLabel(
            "Select a sequence length from the sidebar to view cards"
        )
        instruction_label.setObjectName("instructionLabel")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instruction_label.setWordWrap(True)

        # Apply modern styling
        instruction_label.setStyleSheet(
            """
            QLabel#instructionLabel {
                color: #bdc3c7;
                font-size: 16px;
                padding: 20px;
                background-color: rgba(44, 62, 80, 0.7);
                border-radius: 10px;
                margin: 40px;
            }
        """
        )

        # Add to scroll layout
        if hasattr(self, "scroll_layout") and self.scroll_layout:
            # Clear any existing content
            self._clear_scroll_layout()

            # Add the instruction label
            self.scroll_layout.addWidget(
                instruction_label, 0, Qt.AlignmentFlag.AlignCenter
            )

        # Update description label
        self.description_label.setText("Ready - select a sequence length to begin")

    def _highlight_sidebar(self):
        """Temporarily highlight the sidebar to draw attention to it."""
        if hasattr(self, "nav_sidebar"):
            # Save original style
            original_style = self.nav_sidebar.styleSheet()

            # Apply highlight style
            highlight_style = """
                SequenceCardNavSidebar {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3498db, stop:1 #2980b9);
                    border-radius: 10px;
                    border: 2px solid #5dade2;
                    padding: 8px;
                    margin-right: 10px;
                }
            """
            self.nav_sidebar.setStyleSheet(highlight_style)

            # Restore original style after a delay
            QTimer.singleShot(
                2000, lambda: self.nav_sidebar.setStyleSheet(original_style)
            )

    def _clear_scroll_layout(self):
        """Clear all widgets from the scroll layout."""
        if hasattr(self, "scroll_layout") and self.scroll_layout:
            while self.scroll_layout.count():
                item = self.scroll_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
                elif item.layout():
                    # Remove sublayouts
                    while item.layout().count():
                        subitem = item.layout().takeAt(0)
                        if subitem.widget():
                            subitem.widget().setParent(None)

    def _has_sequence_images(self, images_path: str) -> bool:
        """Check if sequence images exist."""
        if not os.path.exists(images_path):
            return False

        # Check for at least one image
        for item in os.listdir(images_path):
            item_path = os.path.join(images_path, item)
            if os.path.isdir(item_path) and not item.startswith("__"):
                for file in os.listdir(item_path):
                    if file.endswith(".png") and not file.startswith("__"):
                        return True
        return False

    def load_sequences(self):
        """Load sequences with appropriate displayer based on layout mode."""
        # Get the selected length from the sidebar
        selected_length = self.nav_sidebar.selected_length

        # Update UI with more specific message
        length_text = f"{selected_length}-step" if selected_length > 0 else "all"
        self.description_label.setText(f"Loading {length_text} sequences...")
        QApplication.processEvents()

        # Use appropriate displayer based on layout mode
        if USE_PRINTABLE_LAYOUT and hasattr(self, "printable_displayer"):
            # Use printable displayer for optimized print layout
            self.printable_displayer.display_sequences(
                selected_length, show_progress_dialog=False
            )
        elif hasattr(self, "simple_displayer"):
            # Fall back to simple displayer
            self.simple_displayer.display_sequences(
                selected_length, show_progress_dialog=False
            )
        else:
            print("Error: No displayer available")

    def regenerate_all_images(self):
        """Regenerate all images with progress feedback."""
        self.setCursor(Qt.CursorShape.WaitCursor)
        original_text = self.description_label.text()
        self.description_label.setText("Regenerating images... Please wait")
        QApplication.processEvents()

        try:
            if hasattr(self.image_exporter, "export_all_images"):
                self.image_exporter.export_all_images()

            # Get the selected length from the sidebar
            selected_length = self.nav_sidebar.selected_length

            # Reload sequences without showing additional loading dialog
            # Use appropriate displayer based on layout mode
            if USE_PRINTABLE_LAYOUT and hasattr(self, "printable_displayer"):
                # Use printable displayer for optimized print layout
                self.printable_displayer.display_sequences(
                    selected_length, show_progress_dialog=False
                )
            elif hasattr(self, "simple_displayer"):
                # Fall back to simple displayer
                self.simple_displayer.display_sequences(
                    selected_length, show_progress_dialog=False
                )

            self.description_label.setText("Images regenerated successfully!")
            QTimer.singleShot(
                3000, lambda: self.description_label.setText(original_text)
            )

        except Exception as e:
            self.description_label.setText(f"Error regenerating: {str(e)}")
            QTimer.singleShot(
                5000, lambda: self.description_label.setText(original_text)
            )
        finally:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def get_dictionary_mod_time(self) -> float:
        """Get latest modification time of sequence images."""
        images_path = get_sequence_card_image_exporter_path()
        latest_mod_time = 0

        if os.path.exists(images_path):
            for root, _, files in os.walk(images_path):
                for file in files:
                    if file.endswith(".png") and not file.startswith("__"):
                        file_path = os.path.join(root, file)
                        mod_time = os.path.getmtime(file_path)
                        if mod_time > latest_mod_time:
                            latest_mod_time = mod_time

        return latest_mod_time

    def check_dictionary_changes(self):
        """Check for changes and reload if necessary."""
        current_mod_time = self.get_dictionary_mod_time()

        if current_mod_time > self.last_dictionary_mod_time:
            print("Sequence images changed. Reloading...")
            self.last_dictionary_mod_time = current_mod_time
            QTimer.singleShot(100, self.load_sequences)

    def resizeEvent(self, event):
        """Handle resize with simple reload."""
        super().resizeEvent(event)

        # Only reload if we're initialized
        if self.initialized and hasattr(self.nav_sidebar, "selected_length"):
            # Reload after a short delay to avoid multiple reloads during resize
            QTimer.singleShot(300, self.load_sequences)

    def _check_memory_usage(self):
        """Monitor and manage memory usage."""
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / (1024 * 1024)

            if memory_mb > 800:  # 800MB threshold
                print(f"High memory usage: {memory_mb:.1f}MB. Cleaning up...")

                # Clear image cache in simple_displayer
                if hasattr(self, "simple_displayer") and hasattr(
                    self.simple_displayer, "image_cache"
                ):
                    self.simple_displayer.image_cache.clear()
                    print("Cleared simple_displayer image cache")

                # Force garbage collection
                gc.collect()

                # Log results
                new_memory_mb = psutil.Process().memory_info().rss / (1024 * 1024)
                print(f"Memory after cleanup: {new_memory_mb:.1f}MB")

        except ImportError:
            pass  # psutil not available
        except Exception as e:
            print(f"Error checking memory: {e}")

    def cleanup(self):
        """Clean up resources."""
        # Stop timers
        if hasattr(self, "memory_check_timer"):
            self.memory_check_timer.stop()
        if hasattr(self, "dictionary_check_timer"):
            self.dictionary_check_timer.stop()

        # Clear image cache in simple_displayer
        if hasattr(self, "simple_displayer") and hasattr(
            self.simple_displayer, "image_cache"
        ):
            self.simple_displayer.image_cache.clear()
            print("Cleared simple_displayer image cache")

        # Force garbage collection
        gc.collect()

    def closeEvent(self, event):
        """Handle close event."""
        self.cleanup()
        super().closeEvent(event)
