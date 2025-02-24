from copy import deepcopy
from typing import TYPE_CHECKING

from Enums.Enums import Letter
from data.constants import LETTER


if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph


class PictographDataUpdater:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def update_data(self, pictograph_data: dict) -> None:
        for attr_name, attr_value in deepcopy(list(pictograph_data.items())):
            if attr_name == LETTER:
                attr_value = Letter.get_letter(attr_value)
                self.pictograph.state.letter = attr_value
            if attr_name in self.pictograph.state.pictograph_data:
                if attr_value or attr_value == 0:
                    if attr_name != "letter":
                        if (
                            attr_name == "blue_attributes"
                            or attr_name == "red_attributes"
                        ):
                            for k, v in attr_value.items():
                                self.pictograph.state.pictograph_data[attr_name][k] = v
                        else:
                            self.pictograph.state.pictograph_data[attr_name] = (
                                attr_value
                            )
            elif isinstance(attr_value, dict):
                for k, v in attr_value.items():
                    attr_name = k
                    attr_value = v
            if attr_value is not None:
                setattr(self.pictograph, attr_name, attr_value)
