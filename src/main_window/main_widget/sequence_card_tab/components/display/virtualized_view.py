# src/main_window/main_widget/sequence_card_tab/components/display/virtualized_view.py
from typing import TYPE_CHECKING, List, Dict, Any, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QFrame,
    QGridLayout,
    QSizePolicy,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, QSize, QRect, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QPen

from ...core.models import SequenceCardData

if TYPE_CHECKING:
    from ...tab import SequenceCardTab


class VirtualizedCardView(QScrollArea):
    """
    A virtualized view for sequence cards that only renders visible items.

    This provides better performance for large datasets by only creating
    widgets for items that are currently visible in the viewport.
    """

    # Signal when the view needs to be refreshed
    refresh_needed = pyqtSignal()

    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        super().__init__(sequence_card_tab)
        self.sequence_card_tab = sequence_card_tab

        # Data
        self.all_data: List[SequenceCardData] = []
        self.filtered_data: List[SequenceCardData] = []

        # View settings
        self.columns = (
            sequence_card_tab.settings_manager.sequence_card_tab.get_column_count()
        )
        self.item_width = 300
        self.item_height = 400
        self.spacing = 20

        # Viewport tracking
        self.visible_range = (0, 0)
        self.rendered_items: Dict[int, QWidget] = {}

        # Setup UI
        self.setup_ui()

        # Connect signals
        self.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.refresh_needed.connect(self.refresh_view)

        # Delayed refresh for smoother scrolling
        self.refresh_timer = QTimer(self)
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.timeout.connect(self.refresh_view)

    def setup_ui(self):
        """Set up the UI components."""
        # Configure scroll area
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFrameShape(QFrame.Shape.NoFrame)

        # Create content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(self.spacing)
        self.content_layout.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )

        # Create grid for items
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(self.spacing)
        self.content_layout.addLayout(self.grid_layout)

        # Add spacer at the bottom
        self.content_layout.addStretch()

        # Set the content widget
        self.setWidget(self.content_widget)

        # Apply styling
        self.setStyleSheet(
            """
            VirtualizedCardView {
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

    def set_data(self, data: List[SequenceCardData]):
        """Set the data for the view."""
        self.all_data = data
        self.filtered_data = data.copy()
        self.update_layout()
        self.refresh_view()

    def filter_data(self, length: int):
        """Filter data by sequence length."""
        if length == 0:
            # Show all
            self.filtered_data = self.all_data.copy()
        else:
            # Filter by length
            self.filtered_data = [
                item for item in self.all_data if item.length == length
            ]

        self.update_layout()
        self.refresh_view()

    def update_layout(self):
        """Update the layout based on filtered data."""
        # Clear existing items
        self.clear_items()

        # Calculate total rows needed
        total_items = len(self.filtered_data)
        total_rows = (total_items + self.columns - 1) // self.columns

        # Calculate total height
        total_height = total_rows * (self.item_height + self.spacing) + self.spacing

        # Set minimum height for content widget
        self.content_widget.setMinimumHeight(total_height)

        # Calculate visible range
        self.calculate_visible_range()

    def clear_items(self):
        """Clear all rendered items."""
        for widget in self.rendered_items.values():
            widget.setParent(None)
            widget.deleteLater()

        self.rendered_items.clear()

    def calculate_visible_range(self):
        """Calculate which items are visible in the viewport."""
        # Get scroll position
        scroll_pos = self.verticalScrollBar().value()
        viewport_height = self.viewport().height()

        # Calculate visible rows
        start_row = max(0, scroll_pos // (self.item_height + self.spacing) - 1)
        end_row = min(
            (scroll_pos + viewport_height) // (self.item_height + self.spacing) + 2,
            (len(self.filtered_data) + self.columns - 1) // self.columns,
        )

        # Calculate visible items
        start_item = start_row * self.columns
        end_item = min(end_row * self.columns, len(self.filtered_data))

        # Update visible range
        self.visible_range = (start_item, end_item)

    def on_scroll(self):
        """Handle scroll events."""
        # Cancel any pending refresh
        if self.refresh_timer.isActive():
            self.refresh_timer.stop()

        # Start a new timer for delayed refresh
        self.refresh_timer.start(50)  # 50ms delay for smoother scrolling

    def refresh_view(self):
        """Refresh the view to show only visible items."""
        # Calculate visible range
        self.calculate_visible_range()

        # Get visible range
        start_item, end_item = self.visible_range

        # Determine which items to add and remove
        visible_indices = set(range(start_item, end_item))
        current_indices = set(self.rendered_items.keys())

        # Remove items that are no longer visible
        for idx in current_indices - visible_indices:
            if idx in self.rendered_items:
                self.rendered_items[idx].setParent(None)
                self.rendered_items[idx].deleteLater()
                del self.rendered_items[idx]

        # Add items that are now visible
        for idx in visible_indices - current_indices:
            if idx < len(self.filtered_data):
                item_widget = self.create_item_widget(idx)
                if item_widget:
                    # Calculate row and column
                    row = idx // self.columns
                    col = idx % self.columns

                    # Add to grid
                    self.grid_layout.addWidget(item_widget, row, col)
                    self.rendered_items[idx] = item_widget

    def create_item_widget(self, index: int) -> Optional[QWidget]:
        """Create a widget for a sequence card item."""
        if index >= len(self.filtered_data):
            return None

        # Get data for this item
        item_data = self.filtered_data[index]

        # Create container widget
        container = QFrame()
        container.setFixedSize(self.item_width, self.item_height)
        container.setFrameShape(QFrame.Shape.StyledPanel)
        container.setFrameShadow(QFrame.Shape.Raised)
        container.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
            }
            QFrame:hover {
                border: 1px solid #aaa;
                background-color: #f8f8f8;
            }
        """
        )

        # Create layout
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Create header with word
        header = QLabel(item_data.word)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            color: #333;
        """
        )
        layout.addWidget(header)

        # Create image label
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Load image if available
        if item_data.path and item_data.path.exists():
            # Load image with smooth scaling
            image = QImage(str(item_data.path))
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaled(
                    self.item_width - 40,
                    self.item_height - 80,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                image_label.setPixmap(scaled_pixmap)

        layout.addWidget(image_label)

        # Create footer with metadata
        if item_data.metadata:
            footer_text = f"Length: {item_data.length}"
            if "author" in item_data.metadata:
                footer_text += f" | Author: {item_data.metadata['author']}"

            footer = QLabel(footer_text)
            footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
            footer.setStyleSheet(
                """
                font-size: 12px;
                color: #666;
                font-style: italic;
            """
            )
            layout.addWidget(footer)

        return container

    def resizeEvent(self, event):
        """Handle resize events."""
        super().resizeEvent(event)

        # Update item width based on available space
        available_width = self.viewport().width() - 40  # Account for margins
        self.item_width = (
            available_width - (self.columns - 1) * self.spacing
        ) // self.columns
        self.item_height = int(self.item_width * 4 / 3)  # 4:3 aspect ratio

        # Update layout
        self.update_layout()

    def cleanup(self):
        """Clean up resources."""
        self.clear_items()
        self.all_data.clear()
        self.filtered_data.clear()
