#!/usr/bin/env python3
"""
Standalone Option Picker Test - V1-style Layout
Tests option picker display with Alpha 1 start position options
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFrame,
    QGridLayout,
    QScrollArea,
    QGroupBox,
    QPushButton,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

# Add v2 src to path
v2_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src_path))

from src.domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from presentation.components.pictograph.pictograph_component import PictographComponent


class CollapsibleSection(QGroupBox):
    """V1-style collapsible section with header button"""

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.section_title = title
        self.is_expanded = True
        self._setup_ui()

    def _setup_ui(self):
        self.setTitle("")  # No default title
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Header button (V1-style)
        self.header_button = QPushButton(f"▼ {self.section_title}")
        self.header_button.setStyleSheet(
            """
            QPushButton {
                background: rgba(70, 130, 180, 0.8);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background: rgba(70, 130, 180, 1.0);
            }
        """
        )
        self.header_button.clicked.connect(self._toggle_section)
        layout.addWidget(self.header_button)

        # Content frame (V1-style grid)
        self.content_frame = QFrame()
        self.content_layout = QGridLayout(self.content_frame)
        self.content_layout.setContentsMargins(5, 5, 5, 5)
        self.content_layout.setSpacing(8)  # V1 spacing
        self.content_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        self.content_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(248, 249, 250, 180);
                border: 1px solid rgba(222, 226, 230, 180);
                border-radius: 6px;
            }
        """
        )

        layout.addWidget(self.content_frame)

    def _toggle_section(self):
        self.is_expanded = not self.is_expanded
        self.content_frame.setVisible(self.is_expanded)
        arrow = "▼" if self.is_expanded else "▶"
        self.header_button.setText(f"{arrow} {self.section_title}")

    def add_pictograph(self, widget, row: int, col: int):
        """Add pictograph widget to grid layout"""
        self.content_layout.addWidget(widget, row, col)


class SimplePictographWidget(QFrame):
    """Simple pictograph widget for testing"""

    clicked = pyqtSignal(str)

    def __init__(self, beat_data: BeatData, parent=None):
        super().__init__(parent)
        self.beat_data = beat_data
        self._setup_ui()

    def _setup_ui(self):
        self.setFixedSize(160, 160)  # V1-style size
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(0)

        try:
            # Use real pictograph component
            self.pictograph_component = PictographComponent(parent=self)
            self.pictograph_component.update_from_beat(self.beat_data)
            layout.addWidget(self.pictograph_component)

        except Exception as e:
            print(
                f"Failed to create pictograph component for {self.beat_data.letter}: {e}"
            )
            # Fallback to simple display
            letter_label = QLabel(self.beat_data.letter or "?")
            letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            letter_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
            layout.addWidget(letter_label)

        self.setStyleSheet(
            """
            SimplePictographWidget {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 6px;
            }
            SimplePictographWidget:hover {
                border-color: #007bff;
                background-color: #f8f9fa;
                border-width: 3px;
            }
        """
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(f"beat_{self.beat_data.letter}")
        super().mousePressEvent(event)


class TestOptionPicker(QWidget):
    """Test option picker with V1-style layout"""

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self._create_test_data()
        self._populate_sections()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("Option Picker Test - Following Alpha 1")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Scroll area (V1-style)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Container for sections
        self.sections_container = QWidget()
        self.sections_layout = QVBoxLayout(self.sections_container)
        self.sections_layout.setContentsMargins(5, 5, 5, 5)
        self.sections_layout.setSpacing(10)
        self.sections_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll_area.setWidget(self.sections_container)
        layout.addWidget(scroll_area)

        # Create sections (V1-style)
        self.sections = {}
        section_names = ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"]
        for section_name in section_names:
            section = CollapsibleSection(section_name)
            self.sections[section_name] = section
            self.sections_layout.addWidget(section)

    def _create_test_data(self):
        """Create test beat data that would follow Alpha 1"""
        self.test_beats = []

        # Type1 options (A-L range)
        type1_letters = ["D", "E", "F", "G", "H", "I", "J", "K", "L"]
        for letter in type1_letters:
            beat = BeatData(
                letter=letter,
                blue_motion=MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.SOUTH,
                    end_loc=Location.WEST,
                ),
            )
            self.test_beats.append((beat, "Type1"))

        # Type2 options (M-R range)
        type2_letters = ["M", "N", "O", "P", "Q", "R"]
        for letter in type2_letters:
            beat = BeatData(
                letter=letter,
                blue_motion=MotionData(
                    motion_type=MotionType.ANTI,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.EAST,
                    end_loc=Location.SOUTH,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.ANTI,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.WEST,
                    end_loc=Location.NORTH,
                ),
            )
            self.test_beats.append((beat, "Type2"))

        # Type3 options (S-X range)
        type3_letters = ["S", "T", "U", "V", "W", "X"]
        for letter in type3_letters:
            beat = BeatData(
                letter=letter,
                blue_motion=MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.EAST,
                    end_loc=Location.WEST,
                ),
            )
            self.test_beats.append((beat, "Type3"))

    def _populate_sections(self):
        """Populate sections with test data using V1-style layout"""
        COLUMN_COUNT = 8  # V1's exact column count

        # Group beats by section
        section_beats = {}
        for beat, section_name in self.test_beats:
            if section_name not in section_beats:
                section_beats[section_name] = []
            section_beats[section_name].append(beat)

        # Add beats to sections
        for section_name, beats in section_beats.items():
            section = self.sections[section_name]

            for i, beat in enumerate(beats):
                row, col = divmod(i, COLUMN_COUNT)

                widget = SimplePictographWidget(beat)
                widget.clicked.connect(self._handle_pictograph_click)

                section.add_pictograph(widget, row, col)
                print(f"Added {beat.letter} to {section_name} at ({row}, {col})")

    def _handle_pictograph_click(self, beat_id: str):
        print(f"Clicked: {beat_id}")


class TestWindow(QMainWindow):
    """Test window for option picker"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Option Picker Test - V1 Style")
        self.setGeometry(100, 100, 800, 600)

        self.option_picker = TestOptionPicker()
        self.setCentralWidget(self.option_picker)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = TestWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
