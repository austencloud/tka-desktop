from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt
from .section_button import OptionPickerSectionButton
from .letter_types import LetterType


class OptionPickerSection(QWidget):
    def __init__(self, letter_type: str, parent=None):
        super().__init__(parent)
        self.letter_type = letter_type
        self.pictographs: List = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        self.header_button = OptionPickerSectionButton(self.letter_type)
        self.header_button.clicked.connect(self._toggle_section)
        layout.addWidget(self.header_button)

        # V1-style container: simple QFrame with QGridLayout
        from PyQt6.QtWidgets import QFrame

        self.pictograph_container = QFrame()
        self.pictograph_layout = QGridLayout(self.pictograph_container)

        # V1-style layout settings
        self.pictograph_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pictograph_layout.setContentsMargins(0, 0, 0, 0)
        self.pictograph_layout.setSpacing(8)  # V1 uses spacing from option_scroll

        layout.addWidget(self.pictograph_container)

        self.pictograph_container.setStyleSheet(
            """
            QWidget {
                background-color: rgba(248, 249, 250, 180);
                border: 1px solid rgba(222, 226, 230, 180);
                border-radius: 6px;
            }
        """
        )

        # Initialize container visibility to match button state (expanded by default)
        self.pictograph_container.setVisible(self.header_button.is_expanded)

    def _toggle_section(self):
        self.header_button.toggle_expansion()
        self.pictograph_container.setVisible(self.header_button.is_expanded)

    def add_pictograph(self, pictograph_frame):
        """Add pictograph using V1-style direct layout positioning"""
        self.pictographs.append(pictograph_frame)

        # V1-style direct positioning: use COLUMN_COUNT = 8 and divmod calculation
        COLUMN_COUNT = 8  # V1's exact column count
        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)

        # Add directly to layout like V1 does
        self.pictograph_layout.addWidget(pictograph_frame, row, col)
        pictograph_frame.setVisible(True)

        # Ensure container is large enough for V1-style 8-column layout
        self._update_container_size_for_v1_layout()

        print(
            f"🎯 V1-style add: pictograph {count} at ({row}, {col}) in section {self.letter_type}"
        )

    def clear_pictographs(self):
        """Clear pictographs using V1-style removal"""
        for pictograph in self.pictographs:
            if pictograph is not None:
                # V1-style removal: remove from layout and hide
                self.pictograph_layout.removeWidget(pictograph)
                pictograph.setVisible(False)
        self.pictographs.clear()
        print(f"🧹 V1-style clear: section {self.letter_type} cleared")

    def _update_container_size_for_v1_layout(self):
        """Update container size to accommodate V1-style 8-column layout"""
        if len(self.pictographs) == 0:
            return

        # V1-style sizing: 8 columns, each pictograph is 160px + spacing
        COLUMN_COUNT = 8
        pictograph_width = 160
        spacing = 8

        # Calculate required dimensions
        max_row = (len(self.pictographs) - 1) // COLUMN_COUNT
        rows_needed = max_row + 1

        min_width = (
            COLUMN_COUNT * (pictograph_width + spacing) + 20
        )  # 8 columns + margins
        min_height = rows_needed * (pictograph_width + spacing) + 20  # rows + margins

        # Set minimum size to ensure proper spacing
        self.pictograph_container.setMinimumSize(min_width, min_height)

        print(
            f"🔧 V1-style container sizing: {min_width}x{min_height} for {rows_needed} rows x {COLUMN_COUNT} cols"
        )

    def update_layout(self):
        # Clear layout without removing parent relationships
        while self.pictograph_layout.count():
            item = self.pictograph_layout.takeAt(0)
            if item and item.widget():
                # Don't set parent to None, just remove from layout
                pass

        columns = self._calculate_optimal_columns()
        for i, pictograph in enumerate(self.pictographs):
            row = i // columns
            col = i % columns
            self.pictograph_layout.addWidget(pictograph, row, col)

            # Ensure widget is visible and properly positioned
            pictograph.setVisible(True)
            pictograph.raise_()  # Bring to front to avoid stacking issues

        # Force container to update its size to fit the layout
        self.pictograph_container.updateGeometry()
        self.pictograph_container.adjustSize()

        # Calculate and set minimum size based on grid layout
        if len(self.pictographs) > 0:
            rows = (len(self.pictographs) - 1) // columns + 1
            min_width = columns * (160 + 8) + 20  # pictographs + spacing + margins
            min_height = rows * (160 + 8) + 20  # pictographs + spacing + margins

            self.pictograph_container.setMinimumSize(min_width, min_height)
            print(
                f"🔧 Set container minimum size: {min_width}x{min_height} for {rows} rows x {columns} cols"
            )

            # Force immediate visual update to prevent stacking issues
            self.pictograph_container.update()
            self.pictograph_container.repaint()

            # Also update parent widgets to ensure layout propagation
            parent = self.parent()
            if parent:
                parent.updateGeometry()
                parent.update()

        print(
            f"🔧 Updated layout for {self.letter_type}: {len(self.pictographs)} items in {columns} columns"
        )

    def _calculate_optimal_columns(self) -> int:
        """Calculate optimal columns based on V1 behavior and available width"""
        # Get available width from the option picker container
        available_width = 600  # Default fallback

        # Try to get actual available width from parent hierarchy
        parent = self.parent()
        while parent:
            if hasattr(parent, "sections_container"):
                available_width = (
                    parent.sections_container.width() - 40
                )  # Account for margins
                break
            parent = parent.parent()

        pictograph_width = 160 + 8  # Frame width + spacing

        # Calculate max columns that fit
        max_possible_columns = max(1, available_width // pictograph_width)

        # Apply V1-style limits based on letter type (but more generous than before)
        if self.letter_type == LetterType.TYPE1:
            # Type1 can have more columns like V1's COLUMN_COUNT = 8
            max_columns = min(8, max_possible_columns)
        elif self.letter_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
            max_columns = min(6, max_possible_columns)
        else:
            max_columns = min(7, max_possible_columns)

        result = max(2, max_columns)
        print(
            f"🔧 Column calculation for {self.letter_type}: available_width={available_width}, max_possible={max_possible_columns}, result={result}"
        )
        return result
