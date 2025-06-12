"""
Motion orientation calculation service.

This service calculates the end orientation of motions based on motion type,
turns, start orientation, and prop rotation direction, following the exact
algorithms from the reference implementation.
"""

from enum import Enum
from typing import Union

from src.domain.models.core_models import MotionData, MotionType, RotationDirection


class Orientation(Enum):
    """Motion orientations."""

    IN = "in"
    OUT = "out"
    CLOCK = "clock"
    COUNTER = "counter"


class MotionOrientationService:
    """Service for calculating motion orientations."""

    def calculate_end_orientation(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> Orientation:
        """
        Calculate the end orientation of a motion.

        Args:
            motion_data: The motion data
            start_orientation: The starting orientation (defaults to IN)

        Returns:
            The calculated end orientation
        """
        motion_type = motion_data.motion_type
        turns = motion_data.turns
        prop_rot_dir = motion_data.prop_rot_dir

        # Handle float motions separately (not implemented yet)
        if motion_type == MotionType.FLOAT:
            # For now, return start orientation
            # TODO: Implement float orientation calculation
            return start_orientation

        # Validate turns
        valid_turns = {0, 0.5, 1, 1.5, 2, 2.5, 3}
        if turns not in valid_turns:
            return start_orientation

        # Calculate based on turn type
        if turns in {0, 1, 2, 3}:
            return self._calculate_whole_turn_orientation(
                motion_type, int(turns), start_orientation
            )
        elif turns in {0.5, 1.5, 2.5}:
            return self._calculate_half_turn_orientation(
                motion_type, turns, start_orientation, prop_rot_dir
            )

        return start_orientation

    def _calculate_whole_turn_orientation(
        self, motion_type: MotionType, turns: int, start_ori: Orientation
    ) -> Orientation:
        """Calculate orientation for whole turn motions."""
        if motion_type in [MotionType.PRO, MotionType.STATIC]:
            return start_ori if turns % 2 == 0 else self._switch_orientation(start_ori)
        elif motion_type in [MotionType.ANTI, MotionType.DASH]:
            return self._switch_orientation(start_ori) if turns % 2 == 0 else start_ori

        return start_ori

    def _calculate_half_turn_orientation(
        self,
        motion_type: MotionType,
        turns: float,
        start_ori: Orientation,
        prop_rot_dir: RotationDirection,
    ) -> Orientation:
        """Calculate orientation for half turn motions."""
        if motion_type in [MotionType.ANTI, MotionType.DASH]:
            orientation_map = {
                (Orientation.IN, RotationDirection.CLOCKWISE): (
                    Orientation.CLOCK if turns % 2 == 0.5 else Orientation.COUNTER
                ),
                (Orientation.IN, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.COUNTER if turns % 2 == 0.5 else Orientation.CLOCK
                ),
                (Orientation.OUT, RotationDirection.CLOCKWISE): (
                    Orientation.COUNTER if turns % 2 == 0.5 else Orientation.CLOCK
                ),
                (Orientation.OUT, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.CLOCK if turns % 2 == 0.5 else Orientation.COUNTER
                ),
                (Orientation.CLOCK, RotationDirection.CLOCKWISE): (
                    Orientation.OUT if turns % 2 == 0.5 else Orientation.IN
                ),
                (Orientation.CLOCK, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.IN if turns % 2 == 0.5 else Orientation.OUT
                ),
                (Orientation.COUNTER, RotationDirection.CLOCKWISE): (
                    Orientation.IN if turns % 2 == 0.5 else Orientation.OUT
                ),
                (Orientation.COUNTER, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.OUT if turns % 2 == 0.5 else Orientation.IN
                ),
            }
        elif motion_type in [MotionType.PRO, MotionType.STATIC]:
            orientation_map = {
                (Orientation.IN, RotationDirection.CLOCKWISE): (
                    Orientation.COUNTER if turns % 2 == 0.5 else Orientation.CLOCK
                ),
                (Orientation.IN, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.CLOCK if turns % 2 == 0.5 else Orientation.COUNTER
                ),
                (Orientation.OUT, RotationDirection.CLOCKWISE): (
                    Orientation.CLOCK if turns % 2 == 0.5 else Orientation.COUNTER
                ),
                (Orientation.OUT, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.COUNTER if turns % 2 == 0.5 else Orientation.CLOCK
                ),
                (Orientation.CLOCK, RotationDirection.CLOCKWISE): (
                    Orientation.IN if turns % 2 == 0.5 else Orientation.OUT
                ),
                (Orientation.CLOCK, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.OUT if turns % 2 == 0.5 else Orientation.IN
                ),
                (Orientation.COUNTER, RotationDirection.CLOCKWISE): (
                    Orientation.OUT if turns % 2 == 0.5 else Orientation.IN
                ),
                (Orientation.COUNTER, RotationDirection.COUNTER_CLOCKWISE): (
                    Orientation.IN if turns % 2 == 0.5 else Orientation.OUT
                ),
            }
        else:
            return start_ori

        return orientation_map.get((start_ori, prop_rot_dir), start_ori)

    def _switch_orientation(self, ori: Orientation) -> Orientation:
        """Switch orientation to its opposite."""
        switch_map = {
            Orientation.IN: Orientation.OUT,
            Orientation.OUT: Orientation.IN,
            Orientation.CLOCK: Orientation.COUNTER,
            Orientation.COUNTER: Orientation.CLOCK,
        }
        return switch_map.get(ori, ori)

    def get_prop_rotation_angle(
        self, motion_data: MotionData, start_orientation: Orientation = Orientation.IN
    ) -> float:
        """
        Calculate prop rotation angle based on end orientation and location.

        Args:
            motion_data: The motion data
            start_orientation: The starting orientation (defaults to IN)

        Returns:
            The rotation angle in degrees
        """
        # Calculate end orientation
        end_orientation = self.calculate_end_orientation(motion_data, start_orientation)

        # Get location (use end_loc for props)
        location = motion_data.end_loc

        # Determine grid mode based on location
        if location.value in ["n", "s", "e", "w"]:
            grid_mode = "DIAMOND"
        else:
            grid_mode = "BOX"

        # Convert location enum to string for lookup
        location_str = location.value

        # Get rotation angle based on orientation and location
        if grid_mode == "DIAMOND":
            angle_map = {
                Orientation.IN: {
                    "n": 90,
                    "s": 270,
                    "w": 0,
                    "e": 180,
                },
                Orientation.OUT: {
                    "n": 270,
                    "s": 90,
                    "w": 180,
                    "e": 0,
                },
                Orientation.CLOCK: {
                    "n": 0,
                    "s": 180,
                    "w": 270,
                    "e": 90,
                },
                Orientation.COUNTER: {
                    "n": 180,
                    "s": 0,
                    "w": 90,
                    "e": 270,
                },
            }
        else:  # BOX mode
            angle_map = {
                Orientation.IN: {
                    "ne": 135,
                    "nw": 45,
                    "sw": 315,
                    "se": 225,
                },
                Orientation.OUT: {
                    "ne": 315,
                    "nw": 225,
                    "sw": 135,
                    "se": 45,
                },
                Orientation.CLOCK: {
                    "ne": 45,
                    "nw": 315,
                    "sw": 225,
                    "se": 135,
                },
                Orientation.COUNTER: {
                    "ne": 225,
                    "nw": 135,
                    "sw": 45,
                    "se": 315,
                },
            }

        rotation_angle = angle_map.get(end_orientation, {}).get(location_str, 0)
        return float(rotation_angle)
