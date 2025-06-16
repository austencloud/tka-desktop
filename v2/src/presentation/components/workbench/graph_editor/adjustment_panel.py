from typing import Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QCursor, QMouseEvent

from domain.models.core_models import BeatData, MotionType
from .turn_selection_dialog import TurnSelectionDialog


class TurnAdjustButton(QPushButton):
    """Custom button that handles left/right click for different turn adjustments."""

    turn_adjusted = pyqtSignal(float)

    def __init__(self, text: str, left_click_amount: float, right_click_amount: float):
        super().__init__(text)
        self._left_click_amount = left_click_amount
        self._right_click_amount = right_click_amount
        self.setToolTip(
            f"Left click: {left_click_amount:+.2f} turn, Right click: {right_click_amount:+.2f} turn"
        )

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events for left/right click behavior."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.turn_adjusted.emit(self._left_click_amount)
        elif event.button() == Qt.MouseButton.RightButton:
            self.turn_adjusted.emit(self._right_click_amount)

        # Call parent to maintain button visual feedback
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)


class AdjustmentPanel(QWidget):
    """Legacy-exact adjustment panel implementation for graph editor."""

    beat_modified = pyqtSignal(BeatData)
    turn_applied = pyqtSignal(str, float)  # arrow_color, turn_value

    def __init__(self, parent, side: str = "right"):
        super().__init__(parent)
        self._graph_editor = parent
        self._side = side  # "left" or "right" to match Legacy's left_stack/right_stack
        self._current_beat: Optional[BeatData] = None
        self._selected_arrow_id: Optional[str] = None

        # Determine arrow color based on side
        self._arrow_color = "blue" if side == "left" else "red"

        # UI components
        self._hand_indicator: Optional[QLabel] = None
        self._turn_display: Optional[QPushButton] = None
        self._decrement_button: Optional[QPushButton] = None
        self._increment_button: Optional[QPushButton] = None
        self._motion_type_label: Optional[QLabel] = None

        self._setup_ui()

    def _setup_ui(self):
        """Setup Legacy-exact UI structure: Hand Indicator, Turn Display, +/- Buttons, Motion Type."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # 1. Hand Indicator - simple text label
        hand_text = "Left" if self._side == "left" else "Right"
        self._hand_indicator = QLabel(hand_text)
        self._hand_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hand_indicator.setStyleSheet("color: white; font-size: 12px;")
        layout.addWidget(self._hand_indicator)

        # 2. Turn Display - white background, colored border, clickable
        self._turn_display = QPushButton("0.0")
        self._turn_display.setFixedHeight(40)
        self._turn_display.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._turn_display.clicked.connect(self._on_turn_display_clicked)

        # Set Legacy-exact colors
        border_color = "#6496FF" if self._arrow_color == "blue" else "#FF6464"
        self._turn_display.setStyleSheet(
            f"""
            QPushButton {{
                background-color: white;
                border: 2px solid {border_color};
                border-radius: 4px;
                color: black;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
            QPushButton:pressed {{
                background-color: #e0e0e0;
            }}
        """
        )
        layout.addWidget(self._turn_display)

        # 3. Increment/Decrement Buttons - horizontal layout
        buttons_layout = QHBoxLayout()

        # Decrement button (-) with custom mouse event handling
        self._decrement_button = TurnAdjustButton("-", -1.0, -0.5)
        self._decrement_button.setFixedSize(40, 30)
        self._decrement_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._decrement_button.turn_adjusted.connect(self._adjust_turn)

        # Increment button (+) with custom mouse event handling
        self._increment_button = TurnAdjustButton("+", 1.0, 0.5)
        self._increment_button.setFixedSize(40, 30)
        self._increment_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._increment_button.turn_adjusted.connect(self._adjust_turn)

        # Style both buttons
        button_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:disabled {
                background-color: rgba(100, 100, 100, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }
        """
        self._decrement_button.setStyleSheet(button_style)
        self._increment_button.setStyleSheet(button_style)

        buttons_layout.addWidget(self._decrement_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self._increment_button)
        layout.addLayout(buttons_layout)

        # 4. Motion Type Display - simple text label
        self._motion_type_label = QLabel("Static")
        self._motion_type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._motion_type_label.setStyleSheet("color: white; font-size: 12px;")
        layout.addWidget(self._motion_type_label)

        layout.addStretch()

    def _on_turn_display_clicked(self):
        """Handle turn display click to open turn selection dialog."""
        current_turn = self._get_current_turn_value(self._arrow_color)

        # Get the position of the turn display widget for dialog positioning
        widget_pos = self._turn_display.mapToGlobal(self._turn_display.rect().center())

        selected_turn = TurnSelectionDialog.get_turn_value(
            parent=self,
            current_turn=current_turn,
            arrow_color=self._arrow_color,
            position=widget_pos,
        )

        if selected_turn is not None:
            self._apply_turn(self._arrow_color, selected_turn)
            self._update_turn_display_value(selected_turn)

    def _adjust_turn(self, amount: float):
        """Adjust turn value by the specified amount (Legacy-exact behavior)."""
        current_turn = self._get_current_turn_value(self._arrow_color)
        new_turn = max(0.0, min(3.0, current_turn + amount))  # Clamp to 0.0-3.0 range

        if new_turn != current_turn:
            self._apply_turn(self._arrow_color, new_turn)
            self._update_turn_display_value(new_turn)
            self._update_button_states(new_turn)

    def _update_button_states(self, turn_value: float):
        """Update increment/decrement button enabled states based on turn value."""
        # Disable decrement at minimum (0.0)
        self._decrement_button.setEnabled(turn_value > 0.0)

        # Disable increment at maximum (3.0)
        self._increment_button.setEnabled(turn_value < 3.0)

    def _update_turn_display_value(self, turn_value: float):
        """Update the turn display with new value."""
        # Format like Legacy: show "fl" for float, otherwise show number
        if turn_value == float("inf"):
            display_text = "fl"
        else:
            display_text = str(turn_value)

        self._turn_display.setText(display_text)

    def _update_motion_type_display(self):
        """Update motion type label based on current beat data."""
        if not self._current_beat:
            self._motion_type_label.setText("Static")
            return

        motion = None
        if self._arrow_color == "blue" and self._current_beat.blue_motion:
            motion = self._current_beat.blue_motion
        elif self._arrow_color == "red" and self._current_beat.red_motion:
            motion = self._current_beat.red_motion

        if motion and hasattr(motion, "motion_type"):
            motion_type = motion.motion_type
            if isinstance(motion_type, MotionType):
                display_text = motion_type.value.capitalize()
            else:
                display_text = str(motion_type).capitalize()
        else:
            display_text = "Static"

        self._motion_type_label.setText(display_text)

    def _get_current_turn_value(self, arrow_color: str) -> float:
        """Get current turn value for the specified arrow color."""
        if not self._current_beat:
            return 0.0

        if arrow_color == "blue" and self._current_beat.blue_motion:
            return getattr(self._current_beat.blue_motion, "turns", 0.0)
        elif arrow_color == "red" and self._current_beat.red_motion:
            return getattr(self._current_beat.red_motion, "turns", 0.0)

        return 0.0

    def _apply_turn(self, arrow_color: str, turn_value: float):
        """Apply turn value to selected arrow through graph editor service."""
        if hasattr(self._graph_editor, "_graph_service"):
            success = self._graph_editor._graph_service.apply_turn_adjustment(
                arrow_color, turn_value
            )
            if success:
                self.turn_applied.emit(arrow_color, turn_value)
                # Update the beat data if available
                if self._current_beat:
                    self.beat_modified.emit(self._current_beat)

    def set_beat(self, beat_data: Optional[BeatData]):
        """Set beat data and update all UI elements."""
        self._current_beat = beat_data
        self._update_ui_for_beat()

    def set_selected_arrow(self, arrow_id: str):
        """Set selected arrow and update UI highlighting."""
        self._selected_arrow_id = arrow_id

    def _update_ui_for_beat(self):
        """Update UI elements based on current beat data."""
        if not self._current_beat:
            self._turn_display.setText("0.0")
            self._motion_type_label.setText("Static")
            self._update_button_states(0.0)
            return

        # Update turn display for this panel's arrow color
        current_turn = self._get_current_turn_value(self._arrow_color)
        self._update_turn_display_value(current_turn)
        self._update_button_states(current_turn)

        # Update motion type display
        self._update_motion_type_display()
