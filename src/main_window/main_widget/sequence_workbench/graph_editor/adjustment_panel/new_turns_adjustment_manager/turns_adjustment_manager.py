from PyQt6.QtCore import QObject

from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_button_manager import (
    PropRotDirButtonManager,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.turns_widget.motion_type_setter import (
    MotionTypeSetter,
)
from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat


from .turns_value import TurnsValue
from main_window.main_window import TYPE_CHECKING
from .turns_command import AdjustTurnsCommand, SetTurnsCommand, TurnsCommand
from settings_manager.global_settings.app_context import AppContext

if TYPE_CHECKING:
    from .turns_state import TurnsState
    from .json_turns_repository import JsonTurnsRepository
    from .turns_presenter import TurnsPresenter


class TurnsAdjustmentManager(QObject):
    def __init__(
        self,
        state: "TurnsState",
        repository: "JsonTurnsRepository",
        presenter: "TurnsPresenter",
        color: str,
    ):
        super().__init__()
        self._state = state
        self._repo = repository
        self._presenter = presenter
        self._prop_rot_manager = None
        self._motion_type_setter = None
        self._color = color

        self._state.turns_changed.connect(self._on_turns_changed)
        self._state.validation_error.connect(self._presenter.show_error)

    def connect_prop_rotation(self, manager: "PropRotDirButtonManager"):
        """Connect to existing prop rotation manager"""
        self._prop_rot_manager = manager

    def connect_motion_type(self, setter: "MotionTypeSetter"):
        """Connect to motion type setter"""
        self._motion_type_setter = setter

    def adjust(self, delta: float):
        """Adjust turns for the motion associated with the given color."""
        command = AdjustTurnsCommand(self._state, delta, self._color)
        self._execute_command(command)

    def direct_set(self, value: TurnsValue):
        """Directly set turns for the motion associated with the given color."""
        command = SetTurnsCommand(self._state, value, self._color)
        self._execute_command(command)

    def _execute_command(self, command: "TurnsCommand"):
        try:
            command.execute()
            self._repo.save(self._state.current, self._color)
            self._sync_external_state()
        except Exception as e:
            self._presenter.show_error(str(e))

    def _on_turns_changed(self, new_value: TurnsValue):
        self._presenter.update_display(new_value)
        self._update_related_components(new_value)

    def _current_motion(self):
        """Retrieve the motion based on the stored color."""
        current_beat = self._current_beat()
        return current_beat.elements.motion_set[self._color]

    def _update_related_components(self, value: TurnsValue):

        if self._prop_rot_manager:
            self._prop_rot_manager.update_for_turns_change(value)

        if self._motion_type_setter:
            motion_type = self._determine_motion_type(value)
            current_motion = self._current_motion()
            self._motion_type_setter.set_motion_type(current_motion, motion_type)

    def _determine_motion_type(self, value: TurnsValue) -> str:
        if value.raw_value == "fl":
            return "float"
        current_beat = self._current_beat()
        motion_set = current_beat.elements.motion_set
        return motion_set[self._color].state.motion_type

    def _sync_external_state(self):
        """Sync with existing beat frame updates"""
        sequence = AppContext.json_manager().loader_saver.load_current_sequence()
        AppContext.sequence_beat_frame().updater.update_beats_from(sequence)

    def _current_beat(self) -> Beat:
        return AppContext.sequence_beat_frame().get.currently_selected_beat_view().beat
