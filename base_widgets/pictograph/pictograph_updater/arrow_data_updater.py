import logging
from typing import TYPE_CHECKING, Tuple

from Enums.letters import LetterType
from data.constants import RED, BLUE

if TYPE_CHECKING:
    from ..pictograph_scene import PictographScene

logger = logging.getLogger(__name__)



class ArrowDataUpdater:
    def __init__(self, pictograph: "PictographScene") -> None:
        self.pictograph = pictograph

    def update(self, data: dict) -> None:
        """
        Extracts arrow dataset information from the data and updates arrow objects.
        """
        red_arrow_data, blue_arrow_data = self._extract_arrow_datasets(data)
        if self.pictograph.state.letter.get_letter_type() == LetterType.Type3:
            self.pictograph.managers.get.shift().arrow.updater.update_arrow()
            self.pictograph.managers.get.dash().arrow.updater.update_arrow()
        else:
            self.pictograph.elements.arrows.get(RED).updater.update_arrow(red_arrow_data)
            self.pictograph.elements.arrows.get(BLUE).updater.update_arrow(blue_arrow_data)

    def _extract_arrow_datasets(self, data: dict) -> Tuple[dict, dict]:
        red_data = data.get("red_attributes")
        blue_data = data.get("blue_attributes")
        red_arrow_data = blue_arrow_data = None
        if red_data and not blue_data:
            red_arrow_data = self._get_arrow_data(data, RED)
        elif blue_data and not red_data:
            blue_arrow_data = self._get_arrow_data(data, BLUE)
        elif red_data and blue_data:
            red_arrow_data = self._get_arrow_data(data, RED)
            blue_arrow_data = self._get_arrow_data(data, BLUE)
        return red_arrow_data, blue_arrow_data

    def _get_arrow_data(self, data: dict, color: str) -> dict:
        attributes = data[f"{color}_attributes"]
        arrow_data = {}
        if "turns" in attributes or attributes.get("turns") == 0:
            arrow_data["turns"] = attributes["turns"]
        elif attributes.get("prop_rot_dir"):
            arrow_data["prop_rot_dir"] = attributes["prop_rot_dir"]
        if attributes.get("loc"):
            arrow_data["loc"] = attributes["loc"]
        return arrow_data