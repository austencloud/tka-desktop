"""
Manages the generation and manipulation of turns patterns.
"""

import logging
from typing import TYPE_CHECKING, Dict, Any

from objects.arrow.arrow import Arrow
from data.constants import BLUE_ATTRS, RED_ATTRS, TURNS

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class TurnsPatternManager:
    """
    Manages the generation and mirroring of turns patterns.
    Provides functionality to create consistent representations of turns patterns
    for both normal and mirrored entries.
    """

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
