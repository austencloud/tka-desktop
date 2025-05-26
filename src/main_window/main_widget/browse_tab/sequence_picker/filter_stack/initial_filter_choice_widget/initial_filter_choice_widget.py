from typing import TYPE_CHECKING, Union, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QSizePolicy, QScrollArea
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QResizeEvent
from functools import partial
from datetime import datetime, timedelta

from data.constants import GRID_MODE
from ..choose_filter_label import ChooseFilterLabel
from .filter_button_group.filter_button_group import FilterButtonGroup

if TYPE_CHECKING:
    from ..sequence_picker_filter_stack import SequencePickerFilterStack


class InitialFilterChoiceWidget(QWidget):
    """Modern 2025 filter choice widget with responsive grid layout and glass-morphism design."""

    def _get_recent_date_string(self) -> str:
        """Return a string representing the date one week ago."""
        one_week_ago = datetime.now() - timedelta(weeks=1)
        date_string = one_week_ago.strftime("%B %d")
        return date_string.replace(" 0", " ")

    FILTER_OPTIONS: dict[str, tuple[str, Union[str, dict[str, Any]]]] = {
        "Start Letter": (
            "Sequences starting with a specific letter.",
            "starting_letter",
        ),
        "Contains Letter": (
            "Sequences containing specific letters.",
            "contains_letters",
        ),
        "Length": ("Sequences by length.", "sequence_length"),
        "Level": ("Sequences by difficulty level.", "level"),
        "Start Position": ("Sequences by starting position.", "starting_position"),
        "Author": ("Sequences by author.", "author"),
        "Favorites": ("Your favorite sequences.", {"favorites": True}),
        "Most Recent": (
            f"Sequences created since {datetime.now() - timedelta(weeks=1)}.",
            {"most_recent": datetime.now() - timedelta(weeks=1)},
        ),
        "Grid Mode": ("Sequences by grid mode (Box or Diamond).", GRID_MODE),
        "Show All": ("All sequences in the dictionary.", {"show_all": True}),
    }

    def __init__(self, filter_stack: "SequencePickerFilterStack"):
        super().__init__(filter_stack)
        self.filter_selector = filter_stack
        self.browse_tab = filter_stack.browse_tab
        self.main_widget = filter_stack.browse_tab.main_widget
        self.button_groups: dict[str, FilterButtonGroup] = {}

        # Modern responsive properties
        self._grid_columns = 3  # Default columns
        self._layout_initialized = False

        self._setup_modern_ui()

    def _setup_modern_ui(self):
        """Setup modern 2025 UI with responsive design."""
        self.header_label = ChooseFilterLabel(self)
        self._setup_button_groups()
        self._setup_responsive_grid_layout()
        self._setup_modern_main_layout()
        self._apply_modern_container_styling()

        # Defer layout calculations until widget is shown
        QTimer.singleShot(100, self._finalize_layout_initialization)

    def _setup_modern_main_layout(self):
        """Setup modern main layout with proper spacing and responsive design."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(16)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Modern spacing with flexible stretches
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.header_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(24)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addSpacing(16)
        self.main_layout.addWidget(
            self.button_groups["Show All"], 0, Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addStretch(1)

        self.setLayout(self.main_layout)

    def _setup_responsive_grid_layout(self):
        """Setup responsive grid layout that adapts to container size."""
        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Modern spacing (will be updated in resize event)
        self.grid_layout.setHorizontalSpacing(16)
        self.grid_layout.setVerticalSpacing(16)

        # Initially populate with default 3-column layout
        self._populate_grid_layout()

    def _populate_grid_layout(self):
        """Populate grid layout with button groups using responsive columns."""
        # Clear existing layout
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

        # Add button groups to grid with responsive column count
        index = 0
        for label, _ in self.FILTER_OPTIONS.items():
            if label != "Show All":
                button_group = self.button_groups[label]
                row = index // self._grid_columns
                col = index % self._grid_columns
                self.grid_layout.addWidget(
                    button_group, row, col, Qt.AlignmentFlag.AlignCenter
                )
                index += 1

    def _setup_button_groups(self):
        """Create button groups for all filter options."""
        for label, (description, handler_arg) in self.FILTER_OPTIONS.items():
            if label == "Most Recent":
                date_string = self._get_recent_date_string()
                description = f"Sequences created since {date_string}."
            if isinstance(handler_arg, str):
                handler = partial(self.filter_selector.show_section, handler_arg)
            else:
                handler = partial(
                    self.browse_tab.filter_controller.apply_filter, handler_arg
                )
            self.button_groups[label] = FilterButtonGroup(
                label, description, handler, self
            )
        self.description_labels = {
            label: self.button_groups[label].description_label
            for label in self.button_groups
        }

    def _apply_modern_container_styling(self):
        """Apply PyQt6-compatible modern container styling."""
        self.setStyleSheet(
            """
            InitialFilterChoiceWidget {
                background: rgba(0, 0, 0, 0.02);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.05);
                margin: 8px;
                padding: 16px;
            }
        """
        )

    def _finalize_layout_initialization(self):
        """Finalize layout initialization after widget is properly sized."""
        self._layout_initialized = True
        self._update_responsive_layout()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events with modern responsive design."""
        super().resizeEvent(event)
        if self._layout_initialized:
            self._update_responsive_layout()

    def _update_responsive_layout(self):
        """Update layout based on current widget size for optimal responsiveness."""
        if not self.isVisible() or self.width() < 100:
            return

        # Calculate optimal column count based on width
        widget_width = self.width()

        if widget_width < 400:
            new_columns = 1
        elif widget_width < 700:
            new_columns = 2
        elif widget_width < 1000:
            new_columns = 3
        else:
            new_columns = 4

        # Update grid if column count changed
        if new_columns != self._grid_columns:
            self._grid_columns = new_columns
            self._populate_grid_layout()

        # Update spacing based on available space
        self._update_responsive_spacing(widget_width)

    def _update_responsive_spacing(self, widget_width: int):
        """Update spacing based on widget width for optimal visual balance."""
        # Calculate responsive spacing
        base_spacing = max(12, min(24, widget_width // 40))

        # Update grid spacing
        self.grid_layout.setHorizontalSpacing(base_spacing)
        self.grid_layout.setVerticalSpacing(base_spacing)

        # Update main layout margins
        margin = max(16, min(32, widget_width // 30))
        self.main_layout.setContentsMargins(margin, margin, margin, margin)

    def showEvent(self, event):
        """Handle show event to ensure proper layout initialization."""
        super().showEvent(event)
        if not self._layout_initialized:
            QTimer.singleShot(50, self._finalize_layout_initialization)
