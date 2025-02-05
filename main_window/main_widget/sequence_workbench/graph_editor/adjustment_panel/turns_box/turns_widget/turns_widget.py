from PyQt6.QtWidgets import QVBoxLayout, QWidget
from typing import TYPE_CHECKING

from data.constants import ANTI, FLOAT, PRO
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.turns_widget.turns_display_frame.turns_display_frame import (
    TurnsDisplayFrame,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.turns_widget.turns_updater import (
    TurnsUpdater,
)
from objects.motion.motion import Motion

from .turns_text_label import TurnsTextLabel
from .motion_type_setter import MotionTypeSetter
from .direct_set_dialog.direct_set_turns_dialog import DirectSetTurnsDialog
from .turns_adjustment_manager import TurnsAdjustmentManager
from .motion_type_label_widget import MotionTypeLabel

if TYPE_CHECKING:
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

        self.display_frame = TurnsDisplayFrame(self)
        self.direct_set_dialog = DirectSetTurnsDialog(self)
        self.turns_text = TurnsTextLabel(self)
        self.motion_type_label = MotionTypeLabel(self)
        self.motion_type_setter = MotionTypeSetter(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.turns_text)
        layout.addStretch(1)
        layout.addWidget(self.display_frame)
        layout.addStretch(2)
        layout.addWidget(self.motion_type_label)
        layout.addStretch(2)

    def update_turns_display(self, motion: "Motion", new_turns: str) -> None:
        self.turns_box.matching_motion = motion
        display_value = "fl" if new_turns == "fl" else str(new_turns)
        self.display_frame.turns_label.setText(display_value)

        if self.turns_box.matching_motion.motion_type in [PRO, ANTI, FLOAT]:
            self.display_frame.decrement_button.setEnabled(new_turns not in ["fl"])
        else:
            self.display_frame.decrement_button.setEnabled(new_turns != 0)

        if display_value == "3":
            self.display_frame.increment_button.setEnabled(False)
        else:
            self.display_frame.increment_button.setEnabled(True)

        self.motion_type_label.update_display(motion.motion_type)
