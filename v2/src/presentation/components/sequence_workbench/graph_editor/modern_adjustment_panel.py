from typing import Optional, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QPushButton,
    QLabel,
    QButtonGroup,
    QFrame,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from .....domain.models.core_models import BeatData


class ModernAdjustmentPanel(QWidget):
    beat_modified = pyqtSignal(BeatData)
    turn_applied = pyqtSignal(str, float)  # arrow_color, turn_value
    orientation_applied = pyqtSignal(str, str)  # arrow_color, orientation

    def __init__(self, parent):
        super().__init__(parent)
        self._graph_editor = parent
        self._current_beat: Optional[BeatData] = None
        self._selected_arrow_id: Optional[str] = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        header = QLabel("Beat Adjustments")
        header.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        header.setStyleSheet("color: white; padding: 4px;")
        layout.addWidget(header)

        self._stacked_widget = QStackedWidget()

        # Turns adjustment panel
        self._turns_panel = self._create_turns_panel()
        self._stacked_widget.addWidget(self._turns_panel)

        # Orientation adjustment panel
        self._orientation_panel = self._create_orientation_panel()
        self._stacked_widget.addWidget(self._orientation_panel)

        layout.addWidget(self._stacked_widget)

        # Panel switcher
        switcher_layout = QHBoxLayout()
        self._turns_btn = QPushButton("Turns")
        self._ori_btn = QPushButton("Orientation")

        self._turns_btn.clicked.connect(lambda: self._switch_panel(0))
        self._ori_btn.clicked.connect(lambda: self._switch_panel(1))

        for btn in [self._turns_btn, self._ori_btn]:
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 4px;
                    color: white;
                    padding: 4px 8px;
                }
                QPushButton:checked {
                    background-color: rgba(100, 150, 255, 0.3);
                }
            """
            )
            btn.setCheckable(True)

        self._turns_btn.setChecked(True)

        switcher_layout.addWidget(self._turns_btn)
        switcher_layout.addWidget(self._ori_btn)
        layout.addLayout(switcher_layout)

    def _create_turns_panel(self) -> QWidget:
        panel = QFrame()
        layout = QVBoxLayout(panel)

        # Blue turns section
        blue_frame = self._create_color_section("Blue", "blue")
        layout.addWidget(blue_frame)

        # Red turns section
        red_frame = self._create_color_section("Red", "red")
        layout.addWidget(red_frame)

        layout.addStretch()
        return panel

    def _create_orientation_panel(self) -> QWidget:
        panel = QFrame()
        layout = QVBoxLayout(panel)

        # Blue orientation section
        blue_frame = self._create_orientation_section("Blue", "blue")
        layout.addWidget(blue_frame)

        # Red orientation section
        red_frame = self._create_orientation_section("Red", "red")
        layout.addWidget(red_frame)

        layout.addStretch()
        return panel

    def _create_color_section(self, color_name: str, color_key: str) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(
            f"""
            QFrame {{
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                background-color: rgba({
                    '100, 150, 255' if color_key == 'blue' else '255, 100, 100'
                }, 0.1);
                margin: 2px;
            }}
        """
        )

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(4, 4, 4, 4)

        label = QLabel(f"{color_name} Turns")
        label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(label)

        # Turn value buttons
        turns_layout = QHBoxLayout()
        turn_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

        button_group = QButtonGroup(frame)

        for turn_val in turn_values:
            btn = QPushButton(str(turn_val))
            btn.setCheckable(True)
            btn.clicked.connect(
                lambda checked, val=turn_val, color=color_key: self._apply_turn(
                    color, val
                )
            )
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    color: white;
                    padding: 2px 4px;
                    min-width: 30px;
                }
                QPushButton:checked {
                    background-color: rgba(255, 255, 255, 0.3);
                }
            """
            )

            button_group.addButton(btn)
            turns_layout.addWidget(btn)

        layout.addLayout(turns_layout)
        return frame

    def _create_orientation_section(self, color_name: str, color_key: str) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet(
            f"""
            QFrame {{
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                background-color: rgba({
                    '100, 150, 255' if color_key == 'blue' else '255, 100, 100'
                }, 0.1);
                margin: 2px;
            }}
        """
        )

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(4, 4, 4, 4)

        label = QLabel(f"{color_name} Orientation")
        label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(label)

        # Orientation buttons
        ori_layout = QHBoxLayout()
        orientations = ["in", "out", "clock", "counter"]

        button_group = QButtonGroup(frame)

        for ori in orientations:
            btn = QPushButton(ori.title())
            btn.setCheckable(True)
            btn.clicked.connect(
                lambda checked, orientation=ori, color=color_key: self._apply_orientation(
                    color, orientation
                )
            )
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    color: white;
                    padding: 4px 8px;
                }
                QPushButton:checked {
                    background-color: rgba(255, 255, 255, 0.3);
                }
            """
            )

            button_group.addButton(btn)
            ori_layout.addWidget(btn)

        layout.addLayout(ori_layout)
        return frame

    def _switch_panel(self, index: int):
        self._stacked_widget.setCurrentIndex(index)
        self._turns_btn.setChecked(index == 0)
        self._ori_btn.setChecked(index == 1)

    def _apply_turn(self, arrow_color: str, turn_value: float):
        self.turn_applied.emit(arrow_color, turn_value)

    def _apply_orientation(self, arrow_color: str, orientation: str):
        self.orientation_applied.emit(arrow_color, orientation)

    def set_beat(self, beat_data: Optional[BeatData]):
        self._current_beat = beat_data

    def set_selected_arrow(self, arrow_id: str):
        self._selected_arrow_id = arrow_id
