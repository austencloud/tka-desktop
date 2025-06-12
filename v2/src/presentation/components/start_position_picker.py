"""
Start Position Picker Component for Kinetic Constructor v2

This component handles the initial start position selection that precedes the main option picker.
It replicates v1's start position selection workflow and visual design.
"""

from typing import Optional, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
    QPushButton,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from ...domain.models.core_models import BeatData
from ..components.pictograph_component import PictographComponent
from ...application.services.pictograph_dataset_service import PictographDatasetService


class StartPositionOption(QWidget):
    """Individual start position option with pictograph preview."""

    position_selected = pyqtSignal(str)  # Emits position key like "alpha1_alpha1"

    def __init__(self, position_key: str, grid_mode: str = "diamond"):
        super().__init__()
        self.position_key = position_key
        self.grid_mode = grid_mode
        self.dataset_service = PictographDatasetService()
        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI for this start position option."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Create pictograph preview
        self.pictograph_component = PictographComponent()
        self.pictograph_component.setFixedSize(200, 200)
        self.pictograph_component.setStyleSheet(
            """
            QWidget {
                border: 2px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
            }
            QWidget:hover {
                border-color: #007bff;
                background-color: #f8f9fa;
            }
        """
        )

        # Create beat data for this start position using real dataset
        beat_data = self.dataset_service.get_start_position_pictograph(
            self.position_key, self.grid_mode
        )
        if beat_data:
            self.pictograph_component.update_from_beat(beat_data)
        else:
            print(f"⚠️ Could not load start position data for {self.position_key}")

        layout.addWidget(self.pictograph_component)

        # Add position label using actual dataset letter
        position_name = self._get_position_display_name(beat_data)
        label = QLabel(position_name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label.setStyleSheet("color: #2d3748; margin: 5px;")
        layout.addWidget(label)

        # Make clickable
        self.setFixedSize(220, 250)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _get_position_display_name(self, beat_data: Optional[BeatData] = None) -> str:
        """Get display name for this position using actual dataset letter."""
        if beat_data and beat_data.letter:
            # Use the actual letter from the dataset
            letter = beat_data.letter
            position_key_map = {
                "alpha1_alpha1": f"{letter} (Alpha 1)",
                "beta5_beta5": f"{letter} (Beta 5)",
                "gamma11_gamma11": f"{letter} (Gamma 11)",
                "alpha2_alpha2": f"{letter} (Alpha 2)",
                "beta4_beta4": f"{letter} (Beta 4)",
                "gamma12_gamma12": f"{letter} (Gamma 12)",
            }
            return position_key_map.get(
                self.position_key, f"{letter} ({self.position_key})"
            )
        else:
            # Fallback to position key only
            return self.position_key

    def mousePressEvent(self, event):
        """Handle mouse click to select this position."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.position_selected.emit(self.position_key)
        super().mousePressEvent(event)


class StartPositionPicker(QWidget):
    """
    Start position picker component that displays available start positions.

    This component replicates v1's start position selection workflow:
    1. Shows available start positions based on grid mode
    2. Displays pictograph previews for each position
    3. Emits selection signal when user chooses a position
    """

    start_position_selected = pyqtSignal(str)  # Emits selected position key

    # Start position keys for different grid modes (from v1)
    DIAMOND_START_POSITIONS = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
    BOX_START_POSITIONS = ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"]

    def __init__(self):
        super().__init__()
        self.current_grid_mode = "diamond"  # Default to diamond
        self.position_options: List[StartPositionOption] = []
        self._setup_ui()
        self._load_start_positions()

    def _setup_ui(self):
        """Setup the main UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Title
        title = QLabel("Choose Your Start Position")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2d3748; margin: 10px;")
        layout.addWidget(title)

        # Instructions
        instructions = QLabel(
            "Select a starting position to begin building your sequence.\n"
            "Each position represents a different way to hold your props."
        )
        instructions.setFont(QFont("Arial", 12))
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("color: #6c757d; margin: 5px;")
        layout.addWidget(instructions)

        # Scroll area for positions
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Container for position options
        self.positions_container = QWidget()
        self.positions_layout = QGridLayout(self.positions_container)
        self.positions_layout.setSpacing(15)

        scroll_area.setWidget(self.positions_container)
        layout.addWidget(scroll_area)

        # Grid mode toggle (for future enhancement)
        grid_toggle_layout = QHBoxLayout()
        grid_toggle_layout.addStretch()

        diamond_btn = QPushButton("Diamond Grid")
        diamond_btn.setCheckable(True)
        diamond_btn.setChecked(True)
        diamond_btn.clicked.connect(lambda: self._set_grid_mode("diamond"))

        box_btn = QPushButton("Box Grid")
        box_btn.setCheckable(True)
        box_btn.clicked.connect(lambda: self._set_grid_mode("box"))

        grid_toggle_layout.addWidget(diamond_btn)
        grid_toggle_layout.addWidget(box_btn)
        grid_toggle_layout.addStretch()

        layout.addLayout(grid_toggle_layout)

    def _load_start_positions(self):
        """Load start positions based on current grid mode."""
        # Clear existing positions
        for option in self.position_options:
            option.setParent(None)
        self.position_options.clear()

        # Get position keys for current grid mode
        position_keys = (
            self.DIAMOND_START_POSITIONS
            if self.current_grid_mode == "diamond"
            else self.BOX_START_POSITIONS
        )

        # Create position options using dataset service
        for i, position_key in enumerate(position_keys):
            option = StartPositionOption(position_key, self.current_grid_mode)
            option.position_selected.connect(self._handle_position_selection)

            # Add to grid layout (3 columns)
            row = i // 3
            col = i % 3
            self.positions_layout.addWidget(option, row, col)

            self.position_options.append(option)

    def _set_grid_mode(self, grid_mode: str):
        """Set the grid mode and reload positions."""
        self.current_grid_mode = grid_mode
        self._load_start_positions()

    def _handle_position_selection(self, position_key: str):
        """Handle position selection and emit signal."""
        print(f"🎯 Start position selected: {position_key}")
        self.start_position_selected.emit(position_key)
