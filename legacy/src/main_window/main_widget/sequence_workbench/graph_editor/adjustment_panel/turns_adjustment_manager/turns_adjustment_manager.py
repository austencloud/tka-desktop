from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject

from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager.prop_rot_dir_button_manager import (
    PropRotDirButtonManager,
)
from main_window.main_widget.sequence_workbench.graph_editor.adjustment_panel.turns_adjustment_manager.motion_type_setter import (
    MotionTypeSetter,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import Beat
from data.constants import CLOCKWISE, DASH, DASH, FLOAT, NO_ROT, STATIC
from objects.motion.motion import Motion

from .turns_value import TurnsValue
from .turns_command import AdjustTurnsCommand, SetTurnsCommand, TurnsCommand
from src.legacy_settings_manager.global_settings.app_context import AppContext

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
            json_manager = AppContext.json_manager()
            prefloat_motion_type = (
                json_manager.loader_saver.get_json_prefloat_motion_type(
                    beat_index, self._color
                )
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

    def _get_beat_index(self) -> int:
        beat_frame = self._get_sequence_beat_frame()
        if not beat_frame:
            return 0  # Graceful fallback
        current_beat = beat_frame.get.beat_number_of_currently_selected_beat()
        duration = beat_frame.get.duration_of_currently_selected_beat()
        return current_beat + duration

    def _execute_command(self, command: "TurnsCommand"):
        try:
            previous_value = self._state.current

            command.execute()

            current_motion = self._current_motion()
            if current_motion:
                if (
                    previous_value.raw_value != "fl"
                    and self._state.current.raw_value == "fl"
                ):
                    json_manager = AppContext.json_manager()

                    current_motion.state.motion_type = FLOAT
                    current_motion.state.prop_rot_dir = NO_ROT

                    beat_index = self._get_beat_index()
                    if beat_index:
                        json_manager.updater.motion_type_updater.update_motion_type_in_json(
                            beat_index, self._color, FLOAT
                        )
                        json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                            beat_index, self._color, NO_ROT
                        )

                    current_motion.pictograph.state.pictograph_data[
                        f"{self._color}_attributes"
                    ]["motion_type"] = FLOAT
                    current_motion.pictograph.state.pictograph_data[
                        f"{self._color}_attributes"
                    ]["prop_rot_dir"] = NO_ROT

                    self._prop_rot_manager.turns_box.header.update_turns_box_header()
                    self._prop_rot_manager.turns_box.header.hide_prop_rot_dir_buttons()
                    self._prop_rot_manager.turns_box.header.unpress_prop_rot_dir_buttons()
                    self._prop_rot_manager.update_pictograph_letter(
                        current_motion.pictograph
                    )
                elif (
                    previous_value.raw_value == "fl"
                    and self._state.current.raw_value != "fl"
                ):
                    self._restore_prefloat_state(current_motion)

                    beat_index = self._get_beat_index()
                    if (
                        beat_index
                        and self._prefloat_motion_type
                        and self._prefloat_prop_rot_dir
                    ):
                        json_manager = AppContext.json_manager()
                        json_manager.updater.motion_type_updater.update_motion_type_in_json(
                            beat_index, self._color, self._prefloat_motion_type
                        )
                        json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                            beat_index, self._color, self._prefloat_prop_rot_dir
                        )

                    if self._prefloat_motion_type:
                        current_motion.pictograph.state.pictograph_data[
                            f"{self._color}_attributes"
                        ]["motion_type"] = self._prefloat_motion_type
                    if self._prefloat_prop_rot_dir:
                        current_motion.pictograph.state.pictograph_data[
                            f"{self._color}_attributes"
                        ]["prop_rot_dir"] = self._prefloat_prop_rot_dir
                elif current_motion.state.motion_type in [STATIC, DASH]:
                    if (
                        previous_value.raw_value == 0
                        and self._state.current.raw_value != 0
                    ):
                        beat_index = self._get_beat_index()
                        previous_beat_index = beat_index - 1
                        if previous_beat_index >= 0:
                            beat_frame = self._get_sequence_beat_frame()
                            if beat_frame:
                                previous_beat_view = beat_frame.get.beat_view_by_number(
                                    previous_beat_index
                                )
                                previous_motion = (
                                    previous_beat_view.beat.elements.motion_set.get(
                                        self._color
                                    )
                                )
                                if previous_motion:
                                    last_prop_rot_dir = self._get_previous_prop_rot_dir(
                                        previous_beat_index - 1
                                    )

                                    current_motion.state.prop_rot_dir = (
                                        last_prop_rot_dir
                                    )
                                    json_manager = AppContext.json_manager()
                                    json_manager.updater.prop_rot_dir_updater.update_prop_rot_dir_in_json(
                                        beat_index,
                                        self._color,
                                        current_motion.state.prop_rot_dir,
                                    )
                                    current_motion.pictograph.state.pictograph_data[
                                        f"{self._color}_attributes"
                                    ][
                                        "prop_rot_dir"
                                    ] = current_motion.state.prop_rot_dir

            self._repo.save(self._state.current, self._color)
            self._sync_external_state()
        except Exception as e:
            self._presenter.show_error(str(e))

    def _get_previous_prop_rot_dir(self, previous_beat_index):
        beat_frame = self._get_sequence_beat_frame()
        if not beat_frame:
            return CLOCKWISE  # Graceful fallback

        previous_beat_view = beat_frame.get.beat_view_by_number(previous_beat_index)
        if not previous_beat_view:
            return CLOCKWISE
        previous_motion = previous_beat_view.beat.elements.motion_set.get(self._color)

        if previous_motion:
            if previous_motion.state.prop_rot_dir:
                previous_rot_dir = previous_motion.state.prop_rot_dir
                return previous_rot_dir if previous_rot_dir != NO_ROT else CLOCKWISE
            else:
                return self._get_previous_prop_rot_dir(previous_beat_index - 1)
        return CLOCKWISE

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
        AppContext.main_widget().json_manager.ori_validation_engine.run(True)
        sequence = AppContext.json_manager().loader_saver.load_current_sequence()

        beat_frame = self._get_sequence_beat_frame()
        if beat_frame:
            beat_frame.updater.update_beats_from(sequence)

        # Update construct tab options using the new MainWidgetCoordinator architecture
        self._update_construct_tab_options()

    def _current_beat(self) -> Beat:
        beat_frame = self._get_sequence_beat_frame()
        if not beat_frame:
            return None  # Graceful fallback

        selected_beat_view = beat_frame.get.currently_selected_beat_view()
        if selected_beat_view:
            return selected_beat_view.beat
        return None

    def _update_construct_tab_options(self):
        """Update construct tab options using the new MainWidgetCoordinator architecture with graceful fallbacks."""
        try:
            # Try to get main widget through AppContext
            main_widget = AppContext.main_widget()
            if not main_widget:
                import logging

                logger = logging.getLogger(__name__)
                logger.warning(
                    "Main widget not available for construct tab options update"
                )
                return

            # Get construct tab through the new widget manager system
            construct_tab = main_widget.get_tab_widget("construct")
            if not construct_tab:
                # Fallback: try direct access for backward compatibility
                construct_tab = getattr(main_widget, "construct_tab", None)

            if construct_tab and hasattr(construct_tab, "option_picker"):
                if hasattr(construct_tab.option_picker, "updater"):
                    construct_tab.option_picker.updater.update_options()
                else:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.debug("Construct tab option picker has no updater")
            else:
                import logging

                logger = logging.getLogger(__name__)
                logger.debug(
                    "Construct tab not available for options update - this is normal during initialization or when tab hasn't been created yet"
                )

        except AttributeError as e:
            # Handle cases where the MainWidgetCoordinator doesn't have the expected methods
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(
                f"Could not update construct tab options due to architecture change: {e}"
            )
        except Exception as e:
            # Handle any other unexpected errors
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Unexpected error updating construct tab options: {e}")

    def _get_sequence_beat_frame(self):
        """Get the sequence beat frame using graceful fallbacks for the MainWidgetCoordinator refactoring."""
        try:
            # Try to get sequence beat frame through AppContext
            return AppContext.sequence_beat_frame()
        except RuntimeError:
            # AppContext.sequence_beat_frame() not initialized yet
            # This can happen during MainWidgetCoordinator initialization
            import logging

            logger = logging.getLogger(__name__)
            logger.debug(
                "AppContext.sequence_beat_frame() not available yet - this is normal during initialization"
            )
            return None
        except Exception as e:
            # Other unexpected errors
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(f"Unexpected error accessing sequence beat frame: {e}")
            return None
