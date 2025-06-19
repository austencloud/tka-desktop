from typing import Dict, List, Callable, Optional, Tuple
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QSize, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QScreen
import math


class ResponsiveSizingManager(QObject):
    """
    Dynamic sizing manager that ensures option picker never requires scrolling.
    Adapts all elements to fit perfectly within available screen space.
    """

    sizing_changed = pyqtSignal()

    def __init__(
        self,
        option_picker_widget: QWidget,
        sections_container: QWidget,
        filter_widget: Optional[QWidget] = None,
    ):
        super().__init__()
        self.option_picker_widget = option_picker_widget
        self.sections_container = sections_container
        self.filter_widget = filter_widget

        # Sizing parameters
        self.sections: Dict[str, QWidget] = {}
        self.section_headers: Dict[str, QWidget] = {}

        # Dynamic sizing constraints
        self.min_header_height = 20
        self.max_header_height = 60
        self.min_pictograph_size = 40
        self.max_pictograph_size = 120
        self.section_margins = 5
        self.header_margins = 10

        # Calculated values
        self._current_sizing: Optional[Dict] = None

        # Resize timer for performance
        self.resize_timer = QTimer()
        self.resize_timer.timeout.connect(self._recalculate_sizing)
        self.resize_timer.setSingleShot(True)

    def register_section(
        self, section_type: str, section_widget: QWidget, header_widget: QWidget
    ):
        """Register a section for dynamic sizing management"""
        self.sections[section_type] = section_widget
        self.section_headers[section_type] = header_widget

        # Connect to section resize events
        original_resize = section_widget.resizeEvent
        section_widget.resizeEvent = self._create_resize_handler(original_resize)

    def get_dynamic_size_provider(self) -> Callable[[], QSize]:
        """Returns a size provider that gives optimal dimensions for current screen"""

        def size_provider():
            if self._current_sizing:
                return QSize(
                    self._current_sizing["container_width"],
                    self._current_sizing["container_height"],
                )
            return self._calculate_optimal_size()

        return size_provider

    def _calculate_optimal_size(self) -> QSize:
        """Calculate optimal size based on available screen space"""
        # Get available screen space
        screen = QApplication.primaryScreen()
        if not screen:
            return QSize(800, 600)

        screen_geometry = screen.availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate container dimensions (accounting for other UI elements)
        if self.option_picker_widget and self.option_picker_widget.parent():
            parent = self.option_picker_widget.parent()
            container_width = min(
                parent.width() if parent.width() > 0 else screen_width // 2,
                screen_width // 2,
            )
            container_height = min(
                parent.height() if parent.height() > 0 else screen_height - 100,
                screen_height - 100,
            )
        else:
            # Fallback - use portion of screen
            container_width = screen_width // 2
            container_height = (
                screen_height - 100
            )  # Reserve space for taskbar/window frame

        return QSize(container_width, container_height)

    def calculate_dynamic_sizing(self) -> Dict:
        """Calculate comprehensive sizing for all elements to fit perfectly"""
        optimal_size = self._calculate_optimal_size()
        container_width = optimal_size.width()
        container_height = optimal_size.height()

        # Calculate number of sections and their arrangement
        section_count = len(self.sections)
        if section_count == 0:
            section_count = 6  # Default assumption

        # Reserve space for filter widget
        filter_height = 40 if self.filter_widget else 0

        # Calculate available height for sections
        total_margins = (
            self.section_margins * 2 * section_count
        )  # Top/bottom margins per section
        header_space_needed = self.header_margins * section_count  # Space for headers

        available_height = (
            container_height - filter_height - total_margins - header_space_needed
        )

        # Calculate optimal header height
        header_height = self._calculate_optimal_header_height(
            available_height, section_count
        )

        # Calculate remaining space for pictographs
        total_header_height = header_height * section_count
        pictograph_space = available_height - total_header_height

        # Calculate optimal pictograph dimensions
        pictograph_height_per_section = pictograph_space // section_count
        pictograph_size = self._calculate_optimal_pictograph_size(
            container_width, pictograph_height_per_section
        )

        # Calculate section arrangements
        # Types 1,2,3 get full width, Types 4,5,6 share width
        full_width_sections = min(3, section_count)
        shared_width_sections = max(0, section_count - 3)

        individual_section_width = container_width
        shared_section_width = (
            container_width // 3 if shared_width_sections > 0 else container_width
        )

        sizing_config = {
            "container_width": container_width,
            "container_height": container_height,
            "header_height": header_height,
            "pictograph_size": pictograph_size,
            "pictograph_space_per_section": pictograph_height_per_section,
            "individual_section_width": individual_section_width,
            "shared_section_width": shared_section_width,
            "section_margins": self.section_margins,
            "filter_height": filter_height,
            "max_rows_per_section": self._calculate_max_rows(
                pictograph_height_per_section, pictograph_size
            ),
            "columns_per_section": 8,  # Standard from legacy
        }

        self._current_sizing = sizing_config
        return sizing_config

    def _calculate_optimal_header_height(
        self, available_height: int, section_count: int
    ) -> int:
        """Calculate header height that fits proportionally within available space"""
        # Headers should take roughly 15% of available space, distributed among sections
        ideal_header_space = available_height * 0.15
        header_height = int(ideal_header_space / section_count)

        # Apply constraints
        header_height = max(
            self.min_header_height, min(self.max_header_height, header_height)
        )
        return header_height

    def _calculate_optimal_pictograph_size(
        self, container_width: int, height_per_section: int
    ) -> int:
        """Calculate pictograph size that maximizes space usage without overflow"""
        # Calculate based on width constraints (8 columns standard)
        columns = 8
        available_width = container_width - (self.section_margins * 2)
        width_based_size = available_width // columns

        # Calculate based on height constraints
        # Assume maximum 3 rows per section for good UX
        max_rows = 3
        height_based_size = height_per_section // max_rows

        # Use the smaller constraint to ensure both fit
        optimal_size = min(width_based_size, height_based_size)

        # Apply absolute constraints
        optimal_size = max(
            self.min_pictograph_size, min(self.max_pictograph_size, optimal_size)
        )
        return optimal_size

    def _calculate_max_rows(self, height_per_section: int, pictograph_size: int) -> int:
        """Calculate maximum rows that can fit in the allocated section height"""
        if pictograph_size <= 0:
            return 1
        return max(1, height_per_section // pictograph_size)

    def apply_sizing_to_sections(self):
        """Apply calculated sizing to all registered sections"""
        if not self._current_sizing:
            self.calculate_dynamic_sizing()

        sizing = self._current_sizing
        if not sizing:
            return

        for section_type, section_widget in self.sections.items():
            self._apply_section_sizing(section_widget, section_type, sizing)

        for section_type, header_widget in self.section_headers.items():
            self._apply_header_sizing(header_widget, sizing)

        self.sizing_changed.emit()

    def _apply_section_sizing(
        self, section_widget: QWidget, section_type: str, sizing: Dict
    ):
        """Apply sizing to individual section"""
        # Determine width based on section type
        if section_type in ["Type1", "Type2", "Type3"]:
            width = sizing["individual_section_width"]
        else:
            width = sizing["shared_section_width"]

        # Set section dimensions
        section_widget.setFixedWidth(width)

        # Calculate and set maximum height to prevent overflow
        max_section_height = (
            sizing["header_height"]
            + sizing["pictograph_space_per_section"]
            + sizing["section_margins"] * 2
        )
        section_widget.setMaximumHeight(max_section_height)

    def _apply_header_sizing(self, header_widget: QWidget, sizing: Dict):
        """Apply dynamic sizing to section header"""
        if hasattr(header_widget, "setFixedHeight"):
            header_widget.setFixedHeight(sizing["header_height"])

        # If it's a section button, update its sizing logic
        if hasattr(header_widget, "set_dynamic_sizing"):
            header_widget.set_dynamic_sizing(sizing)

    def _create_resize_handler(self, original_resize_event):
        """Create a resize event handler that triggers recalculation"""

        def new_resize_event(event):
            original_resize_event(event)
            self.schedule_resize_recalculation()

        return new_resize_event

    def schedule_resize_recalculation(self):
        """Schedule a resize recalculation (debounced for performance)"""
        self.resize_timer.start(100)  # 100ms delay

    def _recalculate_sizing(self):
        """Recalculate and apply sizing after resize"""
        self.calculate_dynamic_sizing()
        self.apply_sizing_to_sections()

    def get_sizing_info(self) -> Dict:
        """Get current sizing information for debugging"""
        if not self._current_sizing:
            self.calculate_dynamic_sizing()
        return self._current_sizing.copy() if self._current_sizing else {}

    def set_sizing_constraints(
        self,
        min_header: Optional[int] = None,
        max_header: Optional[int] = None,
        min_pictograph: Optional[int] = None,
        max_pictograph: Optional[int] = None,
    ):
        """Update sizing constraints and recalculate"""
        if min_header is not None:
            self.min_header_height = min_header
        if max_header is not None:
            self.max_header_height = max_header
        if min_pictograph is not None:
            self.min_pictograph_size = min_pictograph
        if max_pictograph is not None:
            self.max_pictograph_size = max_pictograph

        self.schedule_resize_recalculation()
