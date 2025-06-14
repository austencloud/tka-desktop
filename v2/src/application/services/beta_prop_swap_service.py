"""
Beta Prop Swap Service for V2 Kinetic Constructor

Implements V1's beta prop swap override system that allows manual overrides
of the algorithmic beta prop separation directions using stored JSON data.
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

from domain.models.core_models import BeatData, MotionData


class BetaPropSwapService:
    """
    Service for handling beta prop swap overrides.

    Replicates V1's SwapBetaHandler logic:
    1. Loads override data from JSON files
    2. Generates override keys for specific pictograph configurations
    3. Checks if manual swap overrides should be applied
    4. Provides swap flags to override algorithmic direction calculation
    """

    def __init__(self):
        self._special_placements: Optional[Dict[str, Any]] = None
        self._load_special_placements()

    def _load_special_placements(self) -> None:
        """Load special placement data from V1-compatible JSON files."""
        try:
            # Get the data directory
            data_dir = Path(__file__).parent.parent.parent / "data" / "arrow_placement"

            self._special_placements = {}

            # Load both diamond and box grid modes
            for grid_mode in ["diamond", "box"]:
                self._special_placements[grid_mode] = {}

                # Load all subfolder categories
                subfolders = [
                    "from_layer1",
                    "from_layer2",
                    "from_layer3_blue2_red1",
                    "from_layer3_blue1_red2",
                ]

                for subfolder in subfolders:
                    self._special_placements[grid_mode][subfolder] = {}

                    subfolder_path = data_dir / grid_mode / "special" / subfolder
                    if not subfolder_path.exists():
                        continue

                    # Load all placement JSON files
                    for json_file in subfolder_path.glob("*_placements.json"):
                        try:
                            with open(json_file, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                self._special_placements[grid_mode][subfolder].update(
                                    data
                                )
                        except Exception as e:
                            print(f"⚠️ Error loading {json_file}: {e}")

        except Exception as e:
            print(f"❌ Error loading special placements: {e}")
            self._special_placements = {"diamond": {}, "box": {}}

    def should_swap_beta_props(
        self, beat_data: BeatData, grid_mode: str = "diamond"
    ) -> bool:
        """
        Check if beta props should be swapped based on override data.

        Args:
            beat_data: Beat data containing motion information
            grid_mode: Grid mode ("diamond" or "box")

        Returns:
            True if props should be swapped (override directions)
        """
        if (
            not self._special_placements
            or not beat_data.blue_motion
            or not beat_data.red_motion
        ):
            return False

        # Generate the override key using V1 logic
        override_key = self._generate_override_key(beat_data, grid_mode)
        if not override_key:
            return False

        # Generate orientation key (simplified for V2)
        ori_key = self._generate_ori_key(beat_data)
        if not ori_key:
            return False

        # Generate turns tuple (simplified for V2)
        turns_tuple = self._generate_turns_tuple(beat_data)

        # Look up override data in the special placements structure
        try:
            grid_data = self._special_placements.get(grid_mode, {})
            ori_data = grid_data.get(ori_key, {})
            letter_data = ori_data.get(beat_data.letter, {})
            turn_data = letter_data.get(turns_tuple, {})

            # Check if the override flag is set to True
            swap_flag = turn_data.get(override_key, False)

            if swap_flag:
                return True

        except Exception as e:
            print(f"⚠️ Error checking swap override: {e}")

        return False

    def _generate_override_key(
        self, beat_data: BeatData, grid_mode: str
    ) -> Optional[str]:
        """
        Generate override key using V1's format.

        Format: swap_beta_{prop_loc}_{beta_ori}_blue_{blue_motion_type}_{blue_arrow_loc}_red_{red_motion_type}_{red_arrow_loc}

        Args:
            beat_data: Beat data containing motion information
            grid_mode: Grid mode for determining prop location

        Returns:
            Override key string or None if cannot be generated
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return None

        # Get prop location (use blue prop end location)
        prop_loc = beat_data.blue_motion.end_loc.value

        # Determine beta orientation (radial vs nonradial)
        # V1 logic: RADIAL = IN/OUT, NONRADIAL = CLOCK/COUNTER
        blue_ori = beat_data.blue_motion.end_ori
        red_ori = beat_data.red_motion.end_ori

        # Check if both props have same orientation type
        blue_is_radial = blue_ori in ["in", "out"]
        red_is_radial = red_ori in ["in", "out"]

        if blue_is_radial and red_is_radial:
            beta_ori = "radial"
        elif not blue_is_radial and not red_is_radial:
            beta_ori = "nonradial"
        else:
            # Mixed orientations - no beta positioning
            return None

        # Get motion types and arrow locations
        blue_motion_type = beat_data.blue_motion.motion_type.value
        red_motion_type = beat_data.red_motion.motion_type.value
        blue_arrow_loc = beat_data.blue_motion.end_loc.value
        red_arrow_loc = beat_data.red_motion.end_loc.value

        # Generate override key
        override_key = (
            f"swap_beta_{prop_loc}_{beta_ori}_"
            f"blue_{blue_motion_type}_{blue_arrow_loc}_"
            f"red_{red_motion_type}_{red_arrow_loc}"
        )

        return override_key

    def _generate_ori_key(self, beat_data: BeatData) -> Optional[str]:
        """
        Generate orientation key for special placement lookup.

        This is a simplified version of V1's ori_key_generator.
        In V1, this depends on complex motion analysis.
        For V2, we'll use a simplified approach based on motion data.

        Args:
            beat_data: Beat data containing motion information

        Returns:
            Orientation key string or None
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return None

        # Simplified ori key generation
        # In V1, this is much more complex and depends on motion analysis
        # For now, we'll use a basic approach based on motion types and orientations

        blue_motion = beat_data.blue_motion
        red_motion = beat_data.red_motion

        # Check for layer classification (simplified)
        blue_is_radial = blue_motion.end_ori in ["in", "out"]
        red_is_radial = red_motion.end_ori in ["in", "out"]

        if blue_is_radial == red_is_radial:
            if blue_is_radial:
                # Both radial - layer 1
                ori_key = "from_layer1"
            else:
                # Both nonradial - layer 2
                ori_key = "from_layer2"
        else:
            # Mixed orientations - layer 3
            if blue_is_radial and not red_is_radial:
                ori_key = "from_layer3_blue1_red2"
            else:
                ori_key = "from_layer3_blue2_red1"

        return ori_key

    def _generate_turns_tuple(self, beat_data: BeatData) -> str:
        """
        Generate turns tuple for special placement lookup.

        This is a simplified version of V1's TurnsTupleGenerator.
        In V1, this generates complex tuples based on motion analysis.
        For V2, we'll use a basic approach.

        Args:
            beat_data: Beat data containing motion information

        Returns:
            Turns tuple string
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return "(s, 1, 1)"  # Default tuple

        # Simplified turns tuple generation
        # In V1, this is much more complex
        # For now, use basic motion data

        blue_turns = beat_data.blue_motion.turns
        red_turns = beat_data.red_motion.turns

        # Use end orientation as a simple proxy for the complex V1 logic
        blue_ori = beat_data.blue_motion.end_ori
        red_ori = beat_data.red_motion.end_ori

        # Generate a basic tuple format that matches V1 patterns
        if blue_ori == "in" and red_ori == "in":
            return "(s, 1, 1)"
        elif blue_ori == "out" and red_ori == "out":
            return "(o, 1, 1)"
        elif blue_ori in ["clock", "counter"]:
            if blue_ori == "clock":
                return "(cw, 1, 0)"
            else:
                return "(ccw, 1, 0)"
        else:
            return "(s, 1, 1)"  # Default

    def get_loaded_placements_info(self) -> Dict[str, Any]:
        """Get information about loaded special placements."""
        if not self._special_placements:
            return {"loaded": False}

        info = {"loaded": True, "grid_modes": {}}

        for grid_mode, grid_data in self._special_placements.items():
            info["grid_modes"][grid_mode] = {}
            for ori_key, ori_data in grid_data.items():
                letter_count = len(ori_data)
                info["grid_modes"][grid_mode][ori_key] = f"{letter_count} letters"

        return info
