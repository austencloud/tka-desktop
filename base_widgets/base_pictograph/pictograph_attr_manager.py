from typing import TYPE_CHECKING

from Enums.Enums import Letter
from data.constants import LETTER


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographAttrManager:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph

    def update_attributes(self, pictograph_dict: dict) -> None:
        for attr_name, attr_value in pictograph_dict.items():
            if attr_name == LETTER:
                attr_value = Letter.get_letter(attr_value)
                self.pictograph.letter = attr_value
            elif isinstance(attr_value, dict):
                for k, v in attr_value.items():
                    attr_name = k
                    attr_value = v
            if attr_value is not None:
                setattr(self.pictograph, attr_name, attr_value)
