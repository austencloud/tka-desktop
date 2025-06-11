from typing import TYPE_CHECKING, Union
from data.constants import (
    ANTI,
    CCW_HANDPATH,
    CLOCK,
    COUNTER,
    CW_HANDPATH,
    DASH,
    PRO,
    STATIC,
    IN,
    OUT,
    FLOAT,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
)
from objects.motion.handpath_calculator import (
    HandpathCalculator,
)


if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionOriCalculator:
    """Calculates the end orientation of a motion."""

    def __init__(self, motion: "Motion") -> None:
        self.motion = motion
        self.hand_rot_dir_calculator = HandpathCalculator()


class MotionOriCalculator:
    """Calculates the end orientation of a motion."""

    def __init__(self, motion: "Motion") -> None:
        self.motion = motion
        self.hand_rot_dir_calculator = HandpathCalculator()

    def get_end_ori(self) -> str:
        """Determine the end orientation of a motion based on its type, turns, and handpath."""

        # Validate required attributes
        if self.motion.state.motion_type is None:
            raise ValueError("Motion type is not set!")

        if self.motion.state.turns is None:
            raise ValueError("Turns must be set before calculating orientation.")

        if self.motion.state.start_ori is None:
            raise ValueError("Start orientation is required!")

        # Handle float case separately
        if self.motion.state.motion_type == FLOAT:
            if not self.motion.state.start_loc or not self.motion.state.end_loc:
                raise ValueError("FLOAT motion requires both start_loc and end_loc.")
            handpath_direction = self.hand_rot_dir_calculator.get_hand_rot_dir(
                self.motion.state.start_loc, self.motion.state.end_loc
            )
            return self.calculate_float_orientation(
                self.motion.state.start_ori, handpath_direction
            )

        if self.motion.state.turns == "fl":
            raise ValueError(
                "You can't have the motion type not be FLOAT while the turns are set to fl."
            )

        # Handle invalid turns
        valid_turns = {0, 0.5, 1, 1.5, 2, 2.5, 3}
        if self.motion.state.turns not in valid_turns:
            raise ValueError(
                f"Invalid turns value: {self.motion.state.turns}. Must be one of {valid_turns}."
            )

        # Whole turn or half turn
        if self.motion.state.turns in {0, 1, 2, 3}:
            return self.calculate_whole_turn_orientation(
                self.motion.state.motion_type,
                self.motion.state.turns,
                self.motion.state.start_ori,
            )
        elif self.motion.state.turns in {0.5, 1.5, 2.5}:
            return self.calculate_half_turn_orientation(
                self.motion.state.motion_type,
                self.motion.state.turns,
                self.motion.state.start_ori,
            )

        # Should never reach here, but let's be explicit
        raise ValueError(
            f"Unhandled case in get_end_ori for turns={self.motion.state.turns}"
        )

    def switch_orientation(self, ori: str) -> str:
        return {IN: OUT, OUT: IN, CLOCK: COUNTER, COUNTER: CLOCK}.get(ori, ori)

    def calculate_whole_turn_orientation(
        self, motion_type: str, turns: int, start_ori: str
    ) -> str:
        if motion_type in [PRO, STATIC]:
            return start_ori if turns % 2 == 0 else self.switch_orientation(start_ori)
        elif motion_type in [ANTI, DASH]:
            return self.switch_orientation(start_ori) if turns % 2 == 0 else start_ori

    def calculate_half_turn_orientation(
        self, motion_type: str, turns: Union[str, int, float], start_ori: str
    ) -> str:
        if motion_type in [ANTI, DASH]:
            orientation_map = {
                (IN, CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (IN, COUNTER_CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (OUT, CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (OUT, COUNTER_CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (CLOCK, CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (CLOCK, COUNTER_CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (COUNTER, CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (COUNTER, COUNTER_CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
            }
        elif motion_type in [PRO, STATIC]:
            orientation_map = {
                (IN, CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (IN, COUNTER_CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (OUT, CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (OUT, COUNTER_CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (CLOCK, CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (CLOCK, COUNTER_CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (COUNTER, CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (COUNTER, COUNTER_CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
            }

        return orientation_map.get((start_ori, self.motion.state.prop_rot_dir))

    def calculate_float_orientation(
        self, start_ori: str, handpath_direction: str
    ) -> str:
        orientation_map = {
            (IN, CW_HANDPATH): CLOCK,
            (IN, CCW_HANDPATH): COUNTER,
            (OUT, CW_HANDPATH): COUNTER,
            (OUT, CCW_HANDPATH): CLOCK,
            (CLOCK, CW_HANDPATH): OUT,
            (CLOCK, CCW_HANDPATH): IN,
            (COUNTER, CW_HANDPATH): IN,
            (COUNTER, CCW_HANDPATH): OUT,
        }
        return orientation_map.get((start_ori, handpath_direction))
