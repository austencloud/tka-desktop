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
        """Add a length option with enhanced styling and hover effects."""
        # Create container frame
        frame = QFrame()
        frame.setObjectName(f"lengthFrame_{length}")
        frame.setMinimumHeight(45)
        frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Add shadow effect for depth
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        frame.setGraphicsEffect(shadow)

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

        # Enhanced mouse events with visual feedback
        def on_mouse_press(_):
            # Visual feedback - darken the frame slightly
            frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2);")
            self.on_length_selected(length)

        def on_mouse_enter(_):
            # Scale up the shadow slightly on hover for a subtle "lift" effect
            shadow = frame.graphicsEffect()
            if shadow:
                shadow.setBlurRadius(15)
                shadow.setOffset(0, 3)

        def on_mouse_leave(_):
            # Reset the shadow when mouse leaves
            shadow = frame.graphicsEffect()
            if shadow:
                shadow.setBlurRadius(10)
                shadow.setOffset(0, 2)
            frame.setStyleSheet("")

        # Connect the enhanced mouse events
        frame.mousePressEvent = on_mouse_press
        frame.enterEvent = on_mouse_enter
        frame.leaveEvent = on_mouse_leave

        # Store references
        self.labels[length] = label

        layout.addWidget(frame)

    def create_column_selector(self) -> QFrame:
        """Create column selector with better styling and real-time updates."""
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
            "Controls ONLY how many page previews appear side-by-side in the UI"
        )

        # Calculate font size based on sidebar width
        label_font_size = min(max(11, int(self.width() / 18)), 13)
        label_font = QFont()
        label_font.setPointSize(label_font_size)
        label_font.setWeight(QFont.Weight.Medium)
        column_label.setFont(label_font)
        column_label.setObjectName("columnLabel")

        column_selector_layout.addWidget(column_label)

        # Create the dropdown with column options
        self.column_dropdown = QComboBox()
        self.column_dropdown.addItems(["2", "3", "4"])
        self.column_dropdown.setObjectName("columnDropdown")
        self.column_dropdown.setFixedHeight(32)  # Fixed height for better containment
        self.column_dropdown.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Set current value from settings using the generic get_setting method
        current_count = int(
            self.settings_manager.get_setting("sequence_card_tab", "column_count", 3)
        )
        index = self.column_dropdown.findText(str(current_count))
        if index >= 0:
            self.column_dropdown.setCurrentIndex(index)

        # Connect the dropdown's currentIndexChanged signal to handle real-time updates
        self.column_dropdown.currentIndexChanged.connect(self.on_column_count_changed)

        # Add the dropdown to the layout
        column_selector_layout.addWidget(self.column_dropdown)

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

    def on_column_count_changed(self, _):
        """
        Handle column count changes with real-time updates and transition effect.

        This method ONLY affects how many page previews are displayed side-by-side in the UI.
        It does NOT change the internal grid layout of each page, which is determined by sequence length.

        Args:
            _: Index parameter from signal (unused)
        """
        try:
            # Get the selected column count for page previews
            column_count = int(self.column_dropdown.currentText())

            # Save the current scroll position
            scroll_position = (
                self.sequence_card_tab.scroll_area.verticalScrollBar().value()
            )

            # Show visual feedback that the change is being applied
            self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)
            self.sequence_card_tab.description_label.setText(
                f"Updating display to show {column_count} preview columns..."
            )
            QApplication.processEvents()

            # Add a brief transition effect
            self._apply_transition_effect()

            # Save the setting using the generic set_setting method
            self.settings_manager.set_setting(
                "sequence_card_tab", "column_count", column_count
            )

            # Update the column count in the tab
            # This only affects the UI layout of page previews, not the internal grid layout of each page
            self.sequence_card_tab.update_column_count(column_count)

            # Restore scroll position after a short delay
            QTimer.singleShot(
                100, lambda: self._restore_scroll_position(scroll_position)
            )

            # Update the description label with more detailed information
            total_pages = 0
            if hasattr(self.sequence_card_tab, "printable_displayer"):
                total_pages = len(self.sequence_card_tab.printable_displayer.pages)

            # Get the current length text
            length_text = (
                f"{self.selected_length}-step" if self.selected_length > 0 else "all"
            )

            # Update the description label
            if total_pages > 0:
                self.sequence_card_tab.description_label.setText(
                    f"Showing {length_text} sequences across {total_pages} pages with {column_count} preview columns"
                )
            else:
                self.sequence_card_tab.description_label.setText(
                    f"Updated display to show {column_count} preview columns"
                )

            # Reset the cursor
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

        except Exception as e:
            print(f"Error updating column count: {e}")
            self.sequence_card_tab.description_label.setText(f"Error: {str(e)}")
            self.sequence_card_tab.setCursor(Qt.CursorShape.ArrowCursor)

    def _apply_transition_effect(self):
        """Apply a brief transition effect during layout updates."""
        # Create a semi-transparent overlay
        overlay = QLabel(self.sequence_card_tab)
        overlay.setGeometry(self.sequence_card_tab.scroll_area.geometry())
        overlay.setStyleSheet(
            """
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
        """
        )
        overlay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        overlay.setText("Updating layout...")
        overlay.setStyleSheet(
            """
            color: white;
            font-size: 16px;
            font-weight: bold;
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 20px;
        """
        )

        # Show the overlay
        overlay.show()
        QApplication.processEvents()

        # Remove the overlay after a short delay
        QTimer.singleShot(300, overlay.deleteLater)

    def _restore_scroll_position(self, position):
        """Restore the scroll position after layout changes."""
        if hasattr(self.sequence_card_tab, "scroll_area"):
            self.sequence_card_tab.scroll_area.verticalScrollBar().setValue(position)

    def refresh_with_feedback(self):
        """Refresh the display with visual feedback."""
        try:
            # Get the column count
            column_count = int(self.column_dropdown.currentText())

            # Update the cursor to show processing
            self.sequence_card_tab.setCursor(Qt.CursorShape.WaitCursor)

            # Update the description label to show processing
            self.sequence_card_tab.description_label.setText(
                f"Updating display to show {column_count} columns..."
            )
            QApplication.processEvents()

            # Update the column count in the tab
            self.sequence_card_tab.update_column_count(column_count)

            # Update the description label to show success with clearer message
            self.sequence_card_tab.description_label.setText(
                f"Updated display to show {column_count} columns"
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
        """Apply modern, high-contrast styling for better readability and visual appeal."""
        self.setStyleSheet(
            """
            /* Main container */
            SequenceCardNavSidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e293b, stop:1 #0f172a);
                border-radius: 12px;
                border: 1px solid #334155;
                padding: 10px;
            }

            /* Header styling */
            QFrame#headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #334155, stop:1 #1e293b);
                border-radius: 10px;
                border: 1px solid #475569;
            }

            QLabel#headerTitle {
                color: #f8fafc;
                font-size: 16px;
                font-weight: bold;
                letter-spacing: 0.5px;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
            }

            QLabel#headerSubtitle {
                color: #cbd5e1;
                font-size: 12px;
                font-style: italic;
            }

            /* Scroll area */
            QScrollArea#lengthScrollArea {
                background: transparent;
                border: none;
            }

            QScrollArea#lengthScrollArea QScrollBar:vertical {
                background: rgba(15, 23, 42, 0.2);
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }

            QScrollArea#lengthScrollArea QScrollBar::handle:vertical {
                background: rgba(100, 116, 139, 0.5);
                border-radius: 4px;
                min-height: 20px;
            }

            QScrollArea#lengthScrollArea QScrollBar::handle:vertical:hover {
                background: rgba(100, 116, 139, 0.8);
            }

            QScrollArea#lengthScrollArea QScrollBar::add-line:vertical,
            QScrollArea#lengthScrollArea QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QScrollArea#lengthScrollArea QScrollBar::add-page:vertical,
            QScrollArea#lengthScrollArea QScrollBar::sub-page:vertical {
                background: none;
            }

            /* Length option frames - unselected */
            QFrame[objectName^="lengthFrame_"]:!QFrame[objectName$="_selected"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #334155, stop:1 #1e293b);
                border: 1px solid #475569;
                border-radius: 10px;
                margin: 3px;
            }

            QFrame[objectName^="lengthFrame_"]:hover:!QFrame[objectName$="_selected"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #475569, stop:1 #334155);
                border: 1px solid #64748b;
            }

            /* Length option frames - selected */
            QFrame[objectName$="_selected"] {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                border: 1px solid #60a5fa;
                border-radius: 10px;
                margin: 3px;
            }

            QFrame[objectName$="_selected"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60a5fa, stop:1 #3b82f6);
                border: 1px solid #93c5fd;
            }

            /* Length labels */
            QLabel#lengthLabel {
                color: #f8fafc;
                font-size: 15px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }

            /* Separator */
            QFrame#separator {
                background-color: #475569;
                max-height: 1px;
                margin: 8px 0px;
            }

            /* Column selector frame */
            QFrame#columnFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #334155, stop:1 #1e293b);
                border-radius: 10px;
                border: 1px solid #475569;
                margin-top: 8px;
            }

            QLabel#columnLabel {
                color: #f8fafc;
                font-size: 14px;
                font-weight: 600;
                letter-spacing: 0.5px;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            }

            /* Column dropdown */
            QComboBox#columnDropdown {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #475569, stop:1 #334155);
                color: #f8fafc;
                border: 1px solid #64748b;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                min-height: 28px;
                selection-background-color: #3b82f6;
            }

            QComboBox#columnDropdown:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #64748b, stop:1 #475569);
                border: 1px solid #94a3b8;
            }

            QComboBox#columnDropdown:focus {
                border: 1px solid #60a5fa;
            }

            QComboBox#columnDropdown::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #64748b;
                border-left-style: solid;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            /* Apply button */
            QPushButton#applyButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                color: #f8fafc;
                border: 1px solid #60a5fa;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 13px;
                font-weight: bold;
                min-height: 28px;
            }

            QPushButton#applyButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #60a5fa, stop:1 #3b82f6);
                border: 1px solid #93c5fd;
            }

            QPushButton#applyButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
                border: 1px solid #3b82f6;
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
