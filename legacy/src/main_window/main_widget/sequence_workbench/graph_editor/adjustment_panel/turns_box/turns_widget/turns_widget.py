from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal
from typing import TYPE_CHECKING

from ...turns_adjustment_manager.json_turns_repository import JsonTurnsRepository
from ...turns_adjustment_manager.turns_adjustment_manager import (
    TurnsAdjustmentManager,
)
from ...turns_adjustment_manager.turns_presenter import TurnsPresenter
from ...turns_adjustment_manager.turns_state import TurnsState
from ...turns_adjustment_manager.turns_value import TurnsValue
from ...turns_box.turns_widget.turns_display_frame.turns_display_frame import (
    TurnsDisplayFrame,
)

from .turns_text_label import TurnsTextLabel
from ...turns_adjustment_manager.motion_type_setter import MotionTypeSetter
from .direct_set_dialog.direct_set_turns_dialog import DirectSetTurnsDialog
from .motion_type_label import MotionTypeLabel
from src.legacy_settings_manager.global_settings.app_context import AppContext

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

        self.turns_box.graph_editor.pictograph_selected.connect(
            self.reset_state_for_new_pictograph
        )

    def _setup_components(self) -> None:
        initial_value = self._get_initial_turns_value()
        self.state = TurnsState(initial_value)

        self.repository = JsonTurnsRepository(AppContext.json_manager())
        self.motion_type_label = MotionTypeLabel(self)
        self.presenter = TurnsPresenter(self, self.motion_type_label)
        self.adjustment_manager = TurnsAdjustmentManager(
            self.state, self.repository, self.presenter, self.turns_box.color
        )
        self.display_frame = TurnsDisplayFrame(self)
        self.turns_text = TurnsTextLabel(self)
        self.motion_type_setter = MotionTypeSetter(self)
        self.direct_set_dialog = DirectSetTurnsDialog(self)

        self.adjustment_manager.connect_prop_rot_dir_btn_mngr(
            self.turns_box.prop_rot_dir_button_manager
        )
        self.adjustment_manager.connect_motion_type_setter(self.motion_type_setter)

        current_motion = self._get_current_motion()
        if current_motion:
            motion_type = current_motion.state.motion_type
            self.presenter.update_display(initial_value, motion_type)

    def _get_initial_turns_value(self) -> TurnsValue:
        try:
            current_motion = self._get_current_motion()
            if current_motion:
                turns_value = current_motion.state.turns
                return TurnsValue(turns_value)
        except (AttributeError, KeyError) as e:
            print(f"Error getting initial turns value: {e}")
        return TurnsValue(0)

    def _get_current_motion(self):
        try:
            current_beat = (
                self.turns_box.graph_editor.pictograph_container.GE_view.pictograph
            )
            return current_beat.elements.motion_set[self.turns_box.color]
        except (AttributeError, KeyError) as e:
            print(f"Error getting current motion: {e}")
            return None

    def reset_state_for_new_pictograph(self) -> None:
        try:
            current_motion = self._get_current_motion()
            if not current_motion:
                return

            new_value = current_motion.state.turns
            motion_type = current_motion.state.motion_type

            new_turns_value = TurnsValue(new_value)

            self.state.current = new_turns_value

            self.presenter.update_display(new_turns_value, motion_type)

            if new_value == "fl" and hasattr(
                self.adjustment_manager, "_prefloat_motion_type"
            ):

                beat_index = self.adjustment_manager._get_beat_index()
                if beat_index:
                    json_manager = AppContext.json_manager()

        except (AttributeError, KeyError) as e:
            print(f"Error resetting turns state: {e}")

    def _setup_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addWidget(self.turns_text, 1)
        layout.addWidget(self.display_frame, 3)
        layout.addWidget(self.motion_type_label, 1)

    def _connect_signals(self):
        self.state.turns_changed.connect(self._notify_external_components)

    def _notify_external_components(self):
        self.turns_adjusted.emit()

        # Update image export preview through the new dependency injection system
        try:
            main_widget = self.turns_box.adjustment_panel.graph_editor.main_widget
            settings_dialog = main_widget.widget_manager.get_widget("settings_dialog")
            if (
                settings_dialog
                and hasattr(settings_dialog, "ui")
                and hasattr(settings_dialog.ui, "image_export_tab")
            ):
                settings_dialog.ui.image_export_tab.update_preview()
        except AttributeError:
            # Fallback: settings dialog not available or not properly initialized
            pass
