"""
Manages the generation and manipulation of turns patterns.
"""

import logging
from typing import TYPE_CHECKING, Dict, Any

from objects.arrow.arrow import Arrow
from data.constants import BLUE_ATTRS, RED_ATTRS, TURNS

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph


class TurnsPatternManager:
    """
    Manages the generation and mirroring of turns patterns.
    Provides functionality to create consistent representations of turns patterns
    for both normal and mirrored entries.
    """

    def generate_turns_tuple(self, pictograph: "Pictograph") -> str:
        """
        Generate a standardized representation of the turns pattern for a pictograph.

        Args:
            pictograph: The pictograph to generate the turns pattern for

        Returns:
            A string representation of the turns pattern
        """
        try:
            blue_motion = pictograph.elements.blue_motion
            red_motion = pictograph.elements.red_motion

            blue_turns = blue_motion.state.turns
            red_turns = red_motion.state.turns

            if isinstance(blue_turns, (int, float)) and isinstance(
                red_turns, (int, float)
            ):
                return f"{blue_turns}_{red_turns}"
            elif blue_turns == "fl" and isinstance(red_turns, (int, float)):
                return f"fl_{red_turns}"
            elif isinstance(blue_turns, (int, float)) and red_turns == "fl":
                return f"{blue_turns}_fl"
            elif blue_turns == "fl" and red_turns == "fl":
                return "fl_fl"
            else:
                logger.warning(
                    f"Unexpected turns types: blue={blue_turns}, red={red_turns}"
                )
                return f"{blue_turns}_{red_turns}"
        except Exception as e:
            logger.error(f"Failed to generate turns tuple: {str(e)}", exc_info=True)
            raise

    def generate_mirrored_tuple(self, arrow: Arrow) -> str:
        """
        Generate the mirrored version of the turns pattern for the given arrow.

        Args:
            arrow: The arrow to generate the mirrored turns pattern for

        Returns:
            A string representation of the mirrored turns pattern
        """
        try:
            pictograph = arrow.pictograph
            blue_motion = pictograph.elements.blue_motion
            red_motion = pictograph.elements.red_motion

            # Get current turns values
            blue_turns = blue_motion.state.turns
            red_turns = red_motion.state.turns

            # Swap the turns values
            mirrored_blue_turns = red_turns
            mirrored_red_turns = blue_turns

            # Return the mirrored pattern
            if isinstance(mirrored_blue_turns, (int, float)) and isinstance(
                mirrored_red_turns, (int, float)
            ):
                return f"{mirrored_blue_turns}_{mirrored_red_turns}"
            elif mirrored_blue_turns == "fl" and isinstance(
                mirrored_red_turns, (int, float)
            ):
                return f"fl_{mirrored_red_turns}"
            elif (
                isinstance(mirrored_blue_turns, (int, float))
                and mirrored_red_turns == "fl"
            ):
                return f"{mirrored_blue_turns}_fl"
            elif mirrored_blue_turns == "fl" and mirrored_red_turns == "fl":
                return "fl_fl"
            else:
                logger.warning(
                    f"Unexpected mirrored turns types: blue={mirrored_blue_turns}, red={mirrored_red_turns}"
                )
                return f"{mirrored_blue_turns}_{mirrored_red_turns}"
        except Exception as e:
            logger.error(
                f"Failed to generate mirrored turns tuple: {str(e)}", exc_info=True
            )
            raise

    def extract_turns_from_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract turns values from pictograph data.

        Args:
            data: The pictograph data to extract turns from

        Returns:
            A dictionary mapping color attributes to turns values
        """
        try:
            result = {}
            if BLUE_ATTRS in data and TURNS in data[BLUE_ATTRS]:
                result[BLUE_ATTRS] = data[BLUE_ATTRS][TURNS]
            if RED_ATTRS in data and TURNS in data[RED_ATTRS]:
                result[RED_ATTRS] = data[RED_ATTRS][TURNS]
            return result
        except Exception as e:
            logger.error(f"Failed to extract turns from data: {str(e)}", exc_info=True)
            return {}
