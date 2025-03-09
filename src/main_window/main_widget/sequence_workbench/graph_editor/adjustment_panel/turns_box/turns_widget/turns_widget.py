from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from typing import TYPE_CHECKING

from ...new_turns_adjustment_manager.json_turns_repository import JsonTurnsRepository
from ...new_turns_adjustment_manager.turns_adjustment_manager import (
    TurnsAdjustmentManager,
)
from ...new_turns_adjustment_manager.turns_presenter import TurnsPresenter
from ...new_turns_adjustment_manager.turns_state import TurnsState
from ...new_turns_adjustment_manager.turns_value import TurnsValue
from ...turns_box.turns_widget.turns_display_frame.turns_display_frame import (
    TurnsDisplayFrame,
)

from .turns_text_label import TurnsTextLabel
from .motion_type_setter import MotionTypeSetter
from .direct_set_dialog.direct_set_turns_dialog import DirectSetTurnsDialog
from .motion_type_label import MotionTypeLabel
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class TurnsWidget(QWidget):
    turns_adjusted = pyqtSignal()

    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self._setup_components()
        self._setup_layout()
        self._connect_signals()

    def _setup_components(self) -> None:
        initial_value = TurnsValue(self._get_initial_turns())
        self.state = TurnsState(initial_value)
        self.repository = JsonTurnsRepository(AppContext.json_manager())
        self.motion_type_label = MotionTypeLabel(self)
        self.presenter = TurnsPresenter(self, self.motion_type_label)
        self.adjustment_manager = TurnsAdjustmentManager(
            self.state,
            self.repository,
            self.presenter,
            self.turns_box.color, 
        )
        self.display_frame = TurnsDisplayFrame(self)
        self.turns_text = TurnsTextLabel(self)
        self.motion_type_setter = MotionTypeSetter(self)
        self.direct_set_dialog = DirectSetTurnsDialog(self)

        self.adjustment_manager.connect_prop_rotation(
            self.turns_box.prop_rot_dir_button_manager
        )
        self.adjustment_manager.connect_motion_type(self.motion_type_setter)

    def _get_initial_turns(self):
        current_beat = (
            self.turns_box.graph_editor.pictograph_container.GE_view.pictograph
        )

        return current_beat.elements.motion_set[self.turns_box.color].state.turns

    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.turns_text, 1)
        layout.addWidget(self.display_frame, 3)
        layout.addWidget(self.motion_type_label, 1)

    def _connect_signals(self):
        self.display_frame.increment_button.clicked.connect(
            lambda: self.adjustment_manager.adjust(0.5)
        )
        self.display_frame.decrement_button.clicked.connect(
            lambda: self.adjustment_manager.adjust(-0.5)
        )

        self.state.turns_changed.connect(self._notify_external_components)

    def _handle_direct_set(self):
        current = self.state.current
        options = [TurnsValue(v) for v in [0, 0.5, 1, 1.5, 2, 2.5, 3, "fl"]]
        value = self.direct_set_dialog.get_value(options, current)
        if value:
            self.adjustment_manager.direct_set(value)

    def _notify_external_components(self):
        self.turns_adjusted.emit()
        self.turns_box.adjustment_panel.graph_editor.main_widget.settings_dialog.ui.image_export_tab.update_preview()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.display_frame.resizeEvent(event)
        self.turns_text.resizeEvent(event)
        self.motion_type_label.resizeEvent(event)
        self.direct_set_dialog.resizeEvent(event)
