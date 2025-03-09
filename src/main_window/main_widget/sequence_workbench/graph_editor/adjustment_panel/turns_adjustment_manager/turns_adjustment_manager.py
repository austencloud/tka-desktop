from PyQt6.QtCore import QObject

from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_button_manager import (
    PropRotDirButtonManager,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.motion_type_setter import (
    MotionTypeSetter,
)
from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat import Beat
from data.constants import FLOAT, NO_ROT
from objects.motion.motion import Motion

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
        self._prefloat_motion_type = None
        self._prefloat_prop_rot_dir = None

        self._state.turns_changed.connect(self._on_turns_changed)
        self._state.validation_error.connect(self._presenter.show_error)

    def connect_prop_rot_dir_btn_mngr(self, manager: "PropRotDirButtonManager"):
        self._prop_rot_manager = manager

    def connect_motion_type_setter(self, setter: "MotionTypeSetter"):
        self._motion_type_setter = setter

    def adjust(self, delta: float):
        current_motion = self._current_motion()
        if current_motion and delta < 0 and self._state.current.raw_value == 0:
            self._store_prefloat_state(current_motion)

        command = AdjustTurnsCommand(self._state, delta, self._color)
        self._execute_command(command)
        AppContext.option_picker().updater.refresh_options()

    def direct_set(self, value: TurnsValue):
        current_motion = self._current_motion()
        if (
            current_motion
            and self._state.current.raw_value != "fl"
            and value.raw_value == "fl"
        ):
            self._store_prefloat_state(current_motion)

        command = SetTurnsCommand(self._state, value, self._color)
        self._execute_command(command)

    def _store_prefloat_state(self, motion: "Motion"):
        self._prefloat_motion_type = motion.state.motion_type
        self._prefloat_prop_rot_dir = motion.state.prop_rot_dir

        beat_index = self._get_beat_index()
        if beat_index:
            self._update_prefloat_state_in_json(beat_index)

    def _update_prefloat_state_in_json(self, beat_index: int):
        json_manager = AppContext.json_manager()
        json_manager.updater.motion_type_updater.update_prefloat_motion_type_in_json(
            beat_index, self._color, self._prefloat_motion_type
        )
        json_manager.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            beat_index, self._color, self._prefloat_prop_rot_dir
        )

    def _restore_prefloat_state(self, motion: "Motion"):
        beat_index = self._get_beat_index()
        if beat_index:
            self._load_prefloat_state_from_json(beat_index)

        if self._prefloat_motion_type:
            motion.state.motion_type = self._prefloat_motion_type
            if self._motion_type_setter:
                self._motion_type_setter.set_motion_type(
                    motion, self._prefloat_motion_type
                )

        if self._prefloat_prop_rot_dir and self._prop_rot_manager:
            motion.state.prop_rot_dir = self._prefloat_prop_rot_dir
            self._prop_rot_manager.update_buttons_for_prop_rot_dir(
                self._prefloat_prop_rot_dir
            )

    def _load_prefloat_state_from_json(self, beat_index: int):
        json_manager = AppContext.json_manager()
        prefloat_motion_type = json_manager.loader_saver.get_json_prefloat_motion_type(
            beat_index, self._color
        )
        prefloat_prop_rot_dir = (
            json_manager.loader_saver.get_json_prefloat_prop_rot_dir(
                beat_index, self._color
            )
        )

        if prefloat_motion_type:
            self._prefloat_motion_type = prefloat_motion_type
        if prefloat_prop_rot_dir:
            self._prefloat_prop_rot_dir = prefloat_prop_rot_dir

    def _get_beat_index(self) -> int:
        beat_frame = AppContext.sequence_beat_frame()
        current_beat = beat_frame.get.beat_number_of_currently_selected_beat()
        duration = beat_frame.get.duration_of_currently_selected_beat()
        return current_beat + duration

    def _execute_command(self, command: "TurnsCommand"):
        try:
            previous_value = self._state.current
            command.execute()
            current_motion = self._current_motion()
            if current_motion:
                self._handle_motion_state_change(previous_value, current_motion)

                # Add this explicit update
                current_motion.pictograph.managers.updater.update_pictograph()
                current_motion.pictograph.managers.arrow_placement_manager.update_arrow_placements()

                # Update letter if needed
                self._update_pictograph_letter(current_motion.pictograph)

            self._repo.save(self._state.current, self._color)
            self._sync_external_state()
        except Exception as e:
            self._presenter.show_error(str(e))

    def _update_pictograph_letter(self, pictograph):
        """Update the letter of the pictograph if needed"""
        if self._prop_rot_manager:
            self._prop_rot_manager.update_pictograph_letter(pictograph)

    def _handle_motion_state_change(
        self, previous_value: TurnsValue, current_motion: "Motion"
    ):
        from data.constants import STATIC, DASH, FLOAT

        if previous_value.raw_value != "fl" and self._state.current.raw_value == "fl":
            self._set_motion_to_float(current_motion)
        elif previous_value.raw_value == "fl" and self._state.current.raw_value != "fl":
            self._restore_prefloat_state(current_motion)
            self._update_motion_state_in_json()

        # Add static motion handling
        if current_motion.state.motion_type in [STATIC, DASH]:
            self._handle_static_motion_update(current_motion)

    def _handle_static_motion_update(self, motion: "Motion"):
        """Ensure proper updates for static motions"""
        from data.constants import CLOCKWISE, NO_ROT

        # Set a default prop rotation direction if needed
        if motion.state.prop_rot_dir == NO_ROT and motion.state.turns > 0:
            motion.state.prop_rot_dir = CLOCKWISE
            # Update UI
            if self._prop_rot_manager:
                self._prop_rot_manager.update_buttons_for_prop_rot_dir(CLOCKWISE)

        # Force a complete pictograph update
        motion.pictograph.managers.updater.update_pictograph()

        # Update arrow placements explicitly
        motion.pictograph.managers.arrow_placement_manager.update_arrow_placements()

        # Update JSON data
        beat_index = self._get_beat_index()
        if beat_index:
            json_manager = AppContext.json_manager()
            json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                beat_index, self._color, motion.state.prop_rot_dir
            )

    def _set_motion_to_float(self, motion: "Motion"):
        json_manager = AppContext.json_manager()
        motion.state.motion_type = FLOAT
        motion.state.prop_rot_dir = NO_ROT
        beat_index = self._get_beat_index()
        if beat_index:
            json_manager.updater.motion_type_updater.update_motion_type_in_json(
                beat_index, self._color, FLOAT
            )
            json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                beat_index, self._color, NO_ROT
            )
        self._update_pictograph_data(motion, FLOAT, NO_ROT)
        self._prop_rot_manager.turns_box.header.update_turns_box_header()
        self._prop_rot_manager.turns_box.header.hide_prop_rot_dir_buttons()
        self._prop_rot_manager.turns_box.header.unpress_prop_rot_dir_buttons()
        self._prop_rot_manager.update_pictograph_letter(motion.pictograph)

    def _update_motion_state_in_json(self):
        beat_index = self._get_beat_index()
        if beat_index and self._prefloat_motion_type and self._prefloat_prop_rot_dir:
            json_manager = AppContext.json_manager()
            json_manager.updater.motion_type_updater.update_motion_type_in_json(
                beat_index, self._color, self._prefloat_motion_type
            )
            json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                beat_index, self._color, self._prefloat_prop_rot_dir
            )

    def _update_pictograph_data(
        self, motion: "Motion", motion_type: str, prop_rot_dir: str
    ):
        motion.pictograph.state.pictograph_data[f"{self._color}_attributes"][
            "motion_type"
        ] = motion_type
        motion.pictograph.state.pictograph_data[f"{self._color}_attributes"][
            "prop_rot_dir"
        ] = prop_rot_dir

    def _on_turns_changed(self, new_value: TurnsValue):
        motion_type = self._determine_motion_type(new_value)
        self._presenter.update_display(new_value, motion_type)
        self._update_related_components(new_value)

    def _current_motion(self):
        current_beat = self._current_beat()
        if current_beat:
            return current_beat.elements.motion_set.get(self._color)
        return None

    def _update_related_components(self, value: TurnsValue):
        if self._prop_rot_manager:
            self._prop_rot_manager.update_for_turns_change(value)

        if self._motion_type_setter:
            motion_type = self._determine_motion_type(value)
            current_motion = self._current_motion()
            if current_motion:
                self._motion_type_setter.set_motion_type(current_motion, motion_type)

    def _determine_motion_type(self, value: TurnsValue) -> str:
        if value.raw_value == "fl":
            return FLOAT

        current_motion = self._current_motion()
        if current_motion:
            return current_motion.state.motion_type
        return "standard"

    def _sync_external_state(self):
        sequence = AppContext.json_manager().loader_saver.load_current_sequence()
        AppContext.sequence_beat_frame().updater.update_beats_from(sequence)

        # Update all pictographs with the same letter
        current_motion = self._current_motion()
        if current_motion:
            letter = current_motion.pictograph.state.letter
            for (
                pictograph
            ) in (
                AppContext.main_widget().pictograph_collector.collect_all_pictographs()
            ):
                if pictograph.state.letter == letter:
                    pictograph.managers.updater.update_pictograph()
                    pictograph.managers.arrow_placement_manager.update_arrow_placements()

    def _current_beat(self) -> Beat:
        selected_beat_view = (
            AppContext.sequence_beat_frame().get.currently_selected_beat_view()
        )
        if selected_beat_view:
            return selected_beat_view.beat
        return None
