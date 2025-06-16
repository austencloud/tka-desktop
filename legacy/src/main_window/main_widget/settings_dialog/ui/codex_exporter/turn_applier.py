"""
Applies turns to pictographs.
"""

from typing import TYPE_CHECKING
from data.constants import RED, BLUE
from objects.motion.motion import MotionOriCalculator

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class TurnApplier:
    """Applies turns to pictographs."""

    @staticmethod
    def apply_turns_to_pictograph(
        pictograph: "LegacyPictograph",
        red_turns: float = 0.0,
        blue_turns: float = 0.0,
    ) -> None:
        """Apply the specified turns to a pictograph.

        Args:
            pictograph: The pictograph to update
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
        """
        # Get the motion objects
        blue_motion = pictograph.elements.motion_set.get(BLUE)
        red_motion = pictograph.elements.motion_set.get(RED)

        # Update the pictograph data directly
        pictograph_data = pictograph.state.pictograph_data.copy()

        if blue_turns in [0.0, 1.0, 2.0, 3.0]:
            blue_turns = int(blue_turns)
        if red_turns in [0.0, 1.0, 2.0, 3.0]:
            red_turns = int(red_turns)
        # Update blue motion data
        if blue_motion and BLUE + "_attributes" in pictograph_data:
            # Only update the turns value, preserve everything else
            pictograph_data[BLUE + "_attributes"]["turns"] = blue_turns
            pictograph_data[BLUE + "_attributes"]["end_ori"] = MotionOriCalculator(
                pictograph.elements.motion_set.get(BLUE)
            ).get_end_ori()
            blue_motion.state.turns = blue_turns

        # Update red motion data
        if red_motion and RED + "_attributes" in pictograph_data:
            # Only update the turns value, preserve everything else
            pictograph_data[RED + "_attributes"]["turns"] = red_turns
            pictograph_data[RED + "_attributes"]["end_ori"] = MotionOriCalculator(
                pictograph.elements.motion_set.get(RED)
            ).get_end_ori()
            #  clean up the turns - if it's a float that could be an int like 1.0, 2.0, 0.0, 3.0, turn it into an int. Otherwise keep it a float.
            red_motion.state.turns = red_turns

        pictograph.elements.motion_set.get(RED).updater.update_motion()
        pictograph.elements.motion_set.get(BLUE).updater.update_motion()

        # Apply the updated data to the pictograph
        pictograph.managers.updater.update_pictograph(pictograph_data)

        # Also set turns directly on the motion objects for good measure
        if blue_motion:
            # Only update the turns value, preserve everything else
            blue_motion.state.turns = blue_turns

        if red_motion:
            # Only update the turns value, preserve everything else
            red_motion.state.turns = red_turns

        # Update the pictograph's turns tuple
        if hasattr(pictograph.managers, "get") and hasattr(
            pictograph.managers.get, "turns_tuple"
        ):
            try:
                # This will update the turns tuple based on the new turns
                pictograph.state.turns_tuple = pictograph.managers.get.turns_tuple()
            except Exception as e:
                print(f"Error updating turns tuple: {e}")

        # Make sure the arrows are updated to reflect the turns
        if hasattr(pictograph.elements, "arrows"):
            for _, arrow in pictograph.elements.arrows.items():
                arrow.setup_components()

        # Update the pictograph
        pictograph.update()
