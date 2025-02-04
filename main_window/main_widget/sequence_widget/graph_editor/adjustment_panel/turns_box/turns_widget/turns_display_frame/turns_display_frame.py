from PyQt6.QtWidgets import QFrame, QHBoxLayout
from typing import TYPE_CHECKING

from .adjust_turns_button import AdjustTurnsButton
from .turns_label import GE_TurnsLabel
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from ..turns_widget import TurnsWidget


class TurnsDisplayFrame(QFrame):
    """This is the frame that contains the turns label and the buttons to adjust the turns."""

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.adjustment_manager = turns_widget.adjustment_manager
        self._setup_components()
        self._attach_listeners()
        self._setup_layout()

    def _setup_components(self) -> None:
        plus_path = get_images_and_data_path("images/icons/plus.svg")
        minus_path = get_images_and_data_path("images/icons/minus.svg")
        self.increment_button = AdjustTurnsButton(plus_path, self)
        self.decrement_button = AdjustTurnsButton(minus_path, self)
        self.turns_label = GE_TurnsLabel(self)

    def _setup_layout(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.decrement_button)
        layout.addWidget(self.turns_label)
        layout.addWidget(self.increment_button)

    def _attach_listeners(self):
        self.increment_button.clicked.connect(
            lambda: self.adjustment_manager.adjust_turns(1)
        )
        self.decrement_button.clicked.connect(
            lambda: self.adjustment_manager.adjust_turns(-1)
        )
        self.decrement_button.customContextMenuRequested.connect(
            lambda: self.adjustment_manager.adjust_turns(-0.5)
        )
        self.increment_button.customContextMenuRequested.connect(
            lambda: self.adjustment_manager.adjust_turns(0.5)
        )
        self.turns_label.clicked.connect(self.turns_widget.on_turns_label_clicked)

