# src/main_window/main_widget/sequence_card_tab/components/navigation/sidebar.py
"""
Navigation sidebar for the sequence card tab with improved styling and functionality.
"""
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QFrame,
    QHBoxLayout,
    QComboBox,
    QPushButton,
    QGraphicsDropShadowEffect,
    QApplication,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QCursor, QFont, QColor
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class SequenceCardNavSidebar(QWidget):
    """Navigation sidebar with filtering options and column selection."""

    length_selected = pyqtSignal(int)  # Signal for length selection

    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        super().__init__(sequence_card_tab)
        self.sequence_card_tab = sequence_card_tab
        self.settings_manager = sequence_card_tab.settings_manager
        self.selected_length = 0  # Default to "Show All"
        self.labels: Dict[int, QLabel] = {}

        self.setup_ui()
        self.apply_modern_styling()

    def setup_ui(self):
        """Set up the UI with better structure."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

        # Header section
        header_frame = self.create_header()
        main_layout.addWidget(header_frame)

        # Scroll area for length options
        scroll_area = self.create_scroll_area()
        main_layout.addWidget(scroll_area, 1)  # Give it stretch

        # Column selector
        column_selector_frame = self.create_column_selector()
        main_layout.addWidget(column_selector_frame)

    def create_header(self) -> QFrame:
        """Create a clear, readable header."""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")

        layout = QVBoxLayout(header_frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        # Main title
        title_label = QLabel("Filter by Length")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("headerTitle")

        # Subtitle
        subtitle_label = QLabel("Select sequence length")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setObjectName("headerSubtitle")

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)

        return header_frame

    def create_scroll_area(self) -> QScrollArea:
        """Create scrollable area for length options."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setObjectName("lengthScrollArea")

        # Content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(6, 6, 6, 6)
        content_layout.setSpacing(8)

        # Add length options
        self.create_length_options(content_layout)

        content_layout.addStretch()
        scroll_area.setWidget(content_widget)

        return scroll_area

    def create_length_options(self, layout: QVBoxLayout):
        """Create length selection options with better visibility."""
        # "Show All" option
        self.add_length_option(layout, 0, "Show All")

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("separator")
        layout.addWidget(separator)

        # Specific lengths
        lengths = [2, 3, 4, 5, 6, 8, 10, 12, 16]
        for length in lengths:
            self.add_length_option(layout, length)

    def add_length_option(
        self, layout: QVBoxLayout, length: int, custom_text: str = None
    ):
        """Add a length option with proper styling."""
        # Create container frame
        frame = QFrame()
        frame.setObjectName(f"lengthFrame_{length}")
        frame.setMinimumHeight(45)
        frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Layout for the frame
        frame_layout = QHBoxLayout(frame)
        frame_layout.setContentsMargins(12, 8, 12, 8)

        # Label
        text = custom_text or str(length)
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName("lengthLabel")

        # Set minimum font size for readability
        font = QFont()
        font.setPointSize(14)  # Larger, more readable font
        font.setWeight(QFont.Weight.Medium)
        label.setFont(font)

        frame_layout.addWidget(label)

        # Mouse events
        frame.mousePressEvent = lambda event: self.on_length_selected(length)

        # Store references
        self.labels[length] = label

        layout.addWidget(frame)

    def create_column_selector(self) -> QFrame:
        """Create column selector with better styling."""
        column_selector_frame = QFrame()
        column_selector_frame.setObjectName("columnFrame")

        column_selector_layout = QVBoxLayout(column_selector_frame)
        column_selector_layout.setContentsMargins(8, 10, 8, 10)
        column_selector_layout.setSpacing(8)

        # Add a label for the column selector with improved styling and clearer description
        column_label = QLabel("Preview Columns")
        column_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        column_label.setWordWrap(True)  # Enable word wrap for better containment
        column_label.setToolTip(
            "Controls how many sequence cards appear side-by-side in each row"
        )

        # Calculate font size based on sidebar width
        label_font_size = min(max(11, int(self.width() / 18)), 13)
        label_font = QFont()
        label_font.setPointSize(label_font_size)
        label_font.setWeight(QFont.Weight.Medium)
        column_label.setFont(label_font)
        column_label.setObjectName("columnLabel")

        column_selector_layout.addWidget(column_label)

        # Create a horizontal layout for the dropdown and apply button
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        # Create the dropdown with column options
        self.column_dropdown = QComboBox()
        self.column_dropdown.addItems(["2", "3", "4"])
        self.column_dropdown.setObjectName("columnDropdown")
        self.column_dropdown.setFixedHeight(32)  # Fixed height for better containment

        # Set current value from settings
        current_count = self.settings_manager.sequence_card_tab.get_column_count()
        index = self.column_dropdown.findText(str(current_count))
        if index >= 0:
            self.column_dropdown.setCurrentIndex(index)

        # Create apply button
        apply_button = QPushButton("Apply")
        apply_button.setObjectName("applyButton")
        apply_button.setFixedHeight(32)  # Fixed height for better containment
        apply_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        apply_button.clicked.connect(self.apply_column_changes)

        # Add widgets to the controls layout
        controls_layout.addWidget(self.column_dropdown)
        controls_layout.addWidget(apply_button)

        # Add the controls layout to the main layout
        column_selector_layout.addLayout(controls_layout)

        return column_selector_frame

    def on_length_selected(self, length: int):
        """Handle length selection with proper state management."""
        self.selected_length = length
        self.update_selection_styles()

        # Emit the signal
        self.length_selected.emit(length)

    def select_length(self, length: int):
        """Programmatically select a length."""
        if length in self.labels:
            self.on_length_selected(length)

    def apply_column_changes(self):
        """Apply column count changes with visual feedback."""
        try:
            # Get the selected column count
            column_count = int(self.column_dropdown.currentText())

            # Show visual feedback that the change is being applied
            self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)
            self.sequence_card_tab.description_label.setText(
                f"Updating display to show {column_count} cards per row..."
            )
            QApplication.processEvents()

            # Save the setting
            self.settings_manager.sequence_card_tab.set_column_count(column_count)

            # Update image displayer if it exists
            if hasattr(self.sequence_card_tab, "image_displayer"):
                self.sequence_card_tab.image_displayer.max_images_per_row = column_count

            # Refresh the display
            self.refresh_with_feedback()

        except Exception as e:
            print(f"Error applying column changes: {e}")
            self.sequence_card_tab.description_label.setText(f"Error: {str(e)}")
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

    def refresh_with_feedback(self):
        """Refresh the display with visual feedback."""
        try:
            # Perform the refresh
            self.sequence_card_tab.refresher.refresh_sequence_cards()

            # Update the description label to show success with clearer message
            column_count = int(self.column_dropdown.currentText())
            self.sequence_card_tab.description_label.setText(
                f"Updated display to show {column_count} cards per row"
            )

            # Reset the description label after 2 seconds
            QTimer.singleShot(
                2000,
                lambda: self.sequence_card_tab.description_label.setText(
                    f"Viewing sequences with length {self.selected_length}"
                ),
            )

            # Reset the cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

        except Exception as e:
            print(f"Error refreshing display: {e}")
            self.sequence_card_tab.description_label.setText(f"Error: {str(e)}")
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

    def update_selection_styles(self):
        """Update styles to show current selection clearly."""
        for length, label in self.labels.items():
            frame = label.parent()
            if length == self.selected_length:
                frame.setObjectName(f"lengthFrame_{length}_selected")
            else:
                frame.setObjectName(f"lengthFrame_{length}")

        # Force style update
        self.style().unpolish(self)
        self.style().polish(self)

    def apply_modern_styling(self):
        """Apply modern, high-contrast styling for better readability."""
        self.setStyleSheet(
            """
            /* Main container */
            SequenceCardNavSidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a2a3a, stop:1 #2c3e50);
                border-radius: 12px;
                border: 1px solid #4a5568;
                padding: 10px;
            }

            /* Header styling */
            QFrame#headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 #1a2a3a);
                border-radius: 10px;
                border: 1px solid #4a5568;
            }

            QLabel#headerTitle {
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }

            QLabel#headerSubtitle {
                color: #bdc3c7;
                font-size: 12px;
                font-style: italic;
            }

            /* Scroll area */
            QScrollArea#lengthScrollArea {
                background: transparent;
                border: none;
            }

            QScrollArea#lengthScrollArea QScrollBar:vertical {
                background: rgba(0,0,0,0.1);
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }

            QScrollArea#lengthScrollArea QScrollBar::handle:vertical {
                background: rgba(0,0,0,0.3);
                border-radius: 4px;
                min-height: 20px;
            }

            QScrollArea#lengthScrollArea QScrollBar::handle:vertical:hover {
                background: rgba(0,0,0,0.5);
            }

            /* Length option frames - unselected */
            QFrame[objectName^="lengthFrame_"]:!QFrame[objectName$="_selected"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3e4651, stop:1 #2c3544);
                border: 1px solid #4a5568;
                border-radius: 10px;
                margin: 3px;
            }

            QFrame[objectName^="lengthFrame_"]:hover:!QFrame[objectName$="_selected"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5568, stop:1 #3e4651);
                border: 1px solid #5d6d7e;
            }

            /* Length option frames - selected */
            QFrame[objectName$="_selected"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #3498db);
                border: 1px solid #5dade2;
                border-radius: 10px;
                margin: 3px;
            }

            /* Length labels */
            QLabel#lengthLabel {
                color: #ffffff;
                font-size: 15px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }

            /* Separator */
            QFrame#separator {
                background-color: #4a5568;
                max-height: 1px;
                margin: 8px 0px;
            }

            /* Column selector frame */
            QFrame#columnFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 #1a2a3a);
                border-radius: 10px;
                border: 1px solid #4a5568;
                margin-top: 8px;
            }

            QLabel#columnLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }

            /* Column dropdown */
            QComboBox#columnDropdown {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4a5568, stop:1 #3e4651);
                color: #ffffff;
                border: 1px solid #5d6d7e;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                min-height: 28px;
                selection-background-color: #3498db;
            }

            QComboBox#columnDropdown:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5d6d7e, stop:1 #4a5568);
                border: 1px solid #7f8c8d;
            }

            QComboBox#columnDropdown::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #5d6d7e;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            /* Apply button */
            QPushButton#applyButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: #ffffff;
                border: 1px solid #5dade2;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: bold;
                min-height: 28px;
            }

            QPushButton#applyButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
                border: 1px solid #85c1e9;
            }

            QPushButton#applyButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1f618d);
                border: 1px solid #3498db;
                padding-top: 7px;
                padding-bottom: 5px;
            }
        """
        )

    def resizeEvent(self, event):
        """Handle resize events to adjust font sizes."""
        super().resizeEvent(event)

        # Update font sizes based on width
        if hasattr(self, "labels"):
            for label in self.labels.values():
                font = label.font()
                font.setPointSize(min(max(12, int(self.width() / 15)), 14))
                label.setFont(font)
