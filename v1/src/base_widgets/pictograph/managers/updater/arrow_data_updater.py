import logging
from typing import TYPE_CHECKING, Tuple

from enums.letter.letter_type import LetterType
from data.constants import (
    BLUE_ATTRS,
    PROP_ROT_DIR,
    RED,
    BLUE,
    RED_ATTRS,
    TURNS,
)

if TYPE_CHECKING:
    from ...legacy_pictograph import LegacyPictograph

logger = logging.getLogger(__name__)


class ArrowDataUpdater:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph

    def update_arrows(self, pictograph_data: dict) -> None:
        """
        Extracts arrow dataset information from the data and updates arrow objects.
        """
        if not pictograph_data:
            return
        red_arrow_data, blue_arrow_data = (
            self._extract_arrow_datasets(pictograph_data)
            if pictograph_data
            else (None, None)
        )
        if self.pictograph.state.letter_type == LetterType.Type3:
            self.pictograph.managers.get.shift().arrow.updater.update_arrow()
            self.pictograph.managers.get.dash().arrow.updater.update_arrow()
        else:
            self.pictograph.elements.arrows.get(RED).updater.update_arrow(
                red_arrow_data
            )
            self.pictograph.elements.arrows.get(BLUE).updater.update_arrow(
                blue_arrow_data
            )

    def _extract_arrow_datasets(self, pictograph_data: dict) -> Tuple[dict, dict]:
        red_data = (
            self._get_arrow_data_from_pictograph_data(pictograph_data, RED)
            if pictograph_data.get(RED_ATTRS, {})
            else None
        )
        blue_data = (
            self._get_arrow_data_from_pictograph_data(pictograph_data, BLUE)
            if pictograph_data.get(BLUE_ATTRS, {})
            else None
        )
        return red_data, blue_data

    def _get_arrow_data_from_pictograph_data(
        self, pictograph_data: dict, color: str
    ) -> dict:
        attributes = pictograph_data[f"{color}_attributes"]
        arrow_data = {}
        if TURNS in attributes or attributes.get(TURNS) == 0:
            arrow_data[TURNS] = attributes[TURNS]
        elif attributes.get(PROP_ROT_DIR):
            arrow_data[PROP_ROT_DIR] = attributes[PROP_ROT_DIR]
        if attributes.get("loc"):
            arrow_data["loc"] = attributes["loc"]
        return arrow_data
