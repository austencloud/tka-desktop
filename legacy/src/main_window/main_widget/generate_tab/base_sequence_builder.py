# base_classes/base_sequence_builder.py

import random
from typing import TYPE_CHECKING, Any

from data.constants import (
    ANTI,
    BEAT,
    BLUE,
    BLUE_ATTRS,
    END_ORI,
    FLOAT,
    MOTION_TYPE,
    PREFLOAT_MOTION_TYPE,
    PREFLOAT_PROP_ROT_DIR,
    PRO,
    PROP_ROT_DIR,
    RED,
    DASH,
    RED_ATTRS,
    START_ORI,
    STATIC,
    NO_ROT,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    TURNS,
)

from .sequence_builder_start_position_manager import SequenceBuilderStartPosManager
from main_window.main_widget.sequence_workbench.sequence_workbench import (
    SequenceWorkbench,
)
from interfaces.json_manager_interface import IJsonManager

if TYPE_CHECKING:
    from .generate_tab import GenerateTab


class BaseSequenceBuilder:
    """
    BaseSequenceBuilder is responsible for initializing and updating the
    sequence for the generator. It loads the current sequence from storage,
    adds a starting position if necessary, and updates orientations and beat numbers.
    """

    def __init__(self, generate_tab: "GenerateTab"):
        self.generate_tab = generate_tab
        self.sequence_workbench: SequenceWorkbench = None

        self.main_widget = generate_tab.main_widget
        self.json_manager = generate_tab.json_manager
        self.validation_engine = self.json_manager.ori_validation_engine
        self.ori_calculator = self.json_manager.ori_calculator
        self.start_pos_manager = SequenceBuilderStartPosManager(self.main_widget)

    def initialize_sequence(self, length: int, CAP_type: str = "") -> None:
        if not self.sequence_workbench:
            # Get sequence workbench through the new widget manager system
            try:
                self.sequence_workbench = self.main_widget.widget_manager.get_widget(
                    "sequence_workbench"
                )
                if not self.sequence_workbench:
                    # Fallback: try direct access for backward compatibility
                    if hasattr(self.main_widget, "sequence_workbench"):
                        self.sequence_workbench = self.main_widget.sequence_workbench
                    else:
                        import logging

                        logger = logging.getLogger(__name__)
                        logger.warning(
                            "sequence_workbench not available in BaseSequenceBuilder"
                        )
                        return
            except AttributeError:
                # Fallback: try direct access for backward compatibility
                if hasattr(self.main_widget, "sequence_workbench"):
                    self.sequence_workbench = self.main_widget.sequence_workbench
                else:
                    import logging

                    logger = logging.getLogger(__name__)
                    logger.warning(
                        "sequence_workbench not available in BaseSequenceBuilder"
                    )
                    return
        self.sequence = self.json_manager.loader_saver.load_current_sequence()

        if len(self.sequence) == 1:
            self.start_pos_manager.add_start_position(CAP_type)
            self.sequence = self.json_manager.loader_saver.load_current_sequence()

        try:
            self.sequence_workbench.beat_frame.populator.modify_layout_for_chosen_number_of_beats(
                int(length)
            )
        except Exception:
            raise

    def update_start_orientations(
        self, next_data: dict[str, Any], last_data: dict[str, dict[str, str]]
    ) -> None:
        """
        Updates the start orientations of the next beat based on the end orientations of the last beat.
        Ensures no None values are assigned.
        """
        blue_end_ori = last_data[BLUE_ATTRS].get(END_ORI)
        red_end_ori = last_data[RED_ATTRS].get(END_ORI)

        if blue_end_ori is None or red_end_ori is None:
            raise ValueError(
                "End orientations cannot be None. Ensure the previous beat has valid orientations."
            )

        next_data[BLUE_ATTRS][START_ORI] = blue_end_ori
        next_data[RED_ATTRS][START_ORI] = red_end_ori

    def update_end_orientations(self, next_data: dict[str, Any]) -> None:
        """
        Updates the end orientations of the next beat using the orientation calculator.
        """
        blue_end_ori = self.ori_calculator.calculate_end_ori(next_data, BLUE)
        red_end_ori = self.ori_calculator.calculate_end_ori(next_data, RED)

        if blue_end_ori is None or red_end_ori is None:
            raise ValueError(
                "Calculated end orientations cannot be None. Please check the input data and orientation calculator."
            )

        next_data[BLUE_ATTRS][END_ORI] = blue_end_ori
        next_data[RED_ATTRS][END_ORI] = red_end_ori

    def update_dash_static_prop_rot_dirs(
        self,
        next_beat: dict[str, Any],
        prop_continuity: str,
        blue_rot_dir: str,
        red_rot_dir: str,
    ) -> None:
        """
        Updates the prop rotation directions for dash/static motion types.
        """

        def update_attr(color: str, rot_dir: str):
            motion_data = next_beat[f"{color}_attributes"]
            if motion_data.get(MOTION_TYPE) in [DASH, STATIC]:
                turns = motion_data.get(TURNS, 0)
                if prop_continuity == "continuous":
                    motion_data[PROP_ROT_DIR] = rot_dir if turns > 0 else NO_ROT
                else:
                    if turns > 0:
                        self._set_random_prop_rot_dir(next_beat, color)
                    else:
                        motion_data[PROP_ROT_DIR] = NO_ROT

                if motion_data[PROP_ROT_DIR] == NO_ROT and turns > 0:
                    raise ValueError(
                        f"{color.capitalize()} prop rotation direction cannot be {NO_ROT} when turns are greater than 0."
                    )

        update_attr(BLUE, blue_rot_dir)
        update_attr(RED, red_rot_dir)

    def _set_random_prop_rot_dir(self, next_data: dict[str, Any], color: str) -> None:
        """Randomly sets the prop rotation direction for the specified color."""
        if color == BLUE:
            next_data[BLUE_ATTRS][PROP_ROT_DIR] = random.choice(
                [CLOCKWISE, COUNTER_CLOCKWISE]
            )
        elif color == RED:
            next_data[RED_ATTRS][PROP_ROT_DIR] = random.choice(
                [CLOCKWISE, COUNTER_CLOCKWISE]
            )

    def update_beat_number(
        self, next_data: dict[str, Any], sequence: list
    ) -> dict[str, Any]:
        """Sets the beat number based on the sequence length."""
        next_data[BEAT] = len(sequence) - 1
        return next_data

    def filter_options_by_rotation(
        self, options: list[dict[str, Any]], blue_rot: str, red_rot: str
    ) -> list[dict[str, Any]]:
        """Filters options to match the given rotation directions."""
        return [
            opt
            for opt in options
            if (
                opt[BLUE_ATTRS].get(PROP_ROT_DIR) in [blue_rot, NO_ROT]
                and opt[RED_ATTRS].get(PROP_ROT_DIR) in [red_rot, NO_ROT]
            )
        ] or options

    def _set_float_turns(self, next_beat: dict[str, Any], color: str) -> None:
        """
        Handles cases where turns are 'fl', adjusting motion type and rotation properties.
        """
        attr = next_beat[f"{color}_attributes"]
        if attr.get(MOTION_TYPE) in [PRO, ANTI]:
            attr[TURNS] = "fl"
            attr[PREFLOAT_MOTION_TYPE] = attr[MOTION_TYPE]
            attr[PREFLOAT_PROP_ROT_DIR] = attr[PROP_ROT_DIR]
            attr[MOTION_TYPE] = FLOAT
            attr[PROP_ROT_DIR] = NO_ROT
        else:
            attr[TURNS] = 0

    def set_turns(
        self, next_beat: dict[str, Any], turn_blue: float, turn_red: float
    ) -> dict[str, Any]:
        """
        Sets the number of turns for both blue and red attributes.
        Adjusts motion types if special flag 'fl' is present.
        """
        if turn_blue == "fl":
            self._set_float_turns(next_beat, BLUE)
        else:
            next_beat[BLUE_ATTRS][TURNS] = turn_blue

        if turn_red == "fl":
            self._set_float_turns(next_beat, RED)
        else:
            next_beat[RED_ATTRS][TURNS] = turn_red

        return next_beat
