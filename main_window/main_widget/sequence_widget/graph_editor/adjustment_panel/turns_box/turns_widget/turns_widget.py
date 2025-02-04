from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from data.constants import ANTI, FLOAT, PRO
from .motion_type_setter import MotionTypeSetter
from .direct_set_dialog.direct_set_turns_dialog import DirectSetTurnsDialog
from .turns_display_frame.turns_display_frame import TurnsDisplayFrame
from .turns_adjustment_manager import TurnsAdjustmentManager
from .turns_updater import TurnsUpdater
from .motion_type_label_widget import MotionTypeLabelWidget

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from ..turns_box import TurnsBox


class TurnsWidget(QWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self._setup_components()
        self._setup_layout()

    def _setup_components(self) -> None:
        self.adjustment_manager = TurnsAdjustmentManager(self)
        self.turns_updater = TurnsUpdater(self)
        self.turns_display_frame = TurnsDisplayFrame(self)
        self.direct_set_dialog = DirectSetTurnsDialog(self)
        self._setup_turns_text()
        self.motion_type_label = MotionTypeLabelWidget(self)
        self.motion_type_setter = MotionTypeSetter(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.turns_text)
        layout.addStretch(1)
        layout.addWidget(self.turns_display_frame)
        layout.addStretch(2)
        layout.addWidget(self.motion_type_label)
        layout.addStretch(2)

    def _setup_turns_text(self) -> None:
        self.turns_text = QLabel("Turns")
        self.turns_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def on_turns_label_clicked(self) -> None:
        self.direct_set_dialog.show_direct_set_dialog()

    def update_turns_display(self, motion: "Motion", new_turns: str) -> None:
        self.turns_box.matching_motion = motion
        display_value = "fl" if new_turns == "fl" else str(new_turns)
        self.turns_display_frame.turns_label.setText(display_value)

        if self.turns_box.matching_motion.motion_type in [PRO, ANTI, FLOAT]:
            self.turns_display_frame.decrement_button.setEnabled(
                new_turns not in ["fl"]
            )
        else:
            self.turns_display_frame.decrement_button.setEnabled(new_turns != 0)

        if display_value == "3":
            self.turns_display_frame.increment_button.setEnabled(False)
        else:
            self.turns_display_frame.increment_button.setEnabled(True)

        self.motion_type_label.update_display(motion.motion_type)

    def resizeEvent(self, event) -> None:
        font_size = self.turns_box.graph_editor.width() // 50
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.turns_text.setFont(font)

        self.motion_type_label.resize_buttons()
        super().resizeEvent(event)
