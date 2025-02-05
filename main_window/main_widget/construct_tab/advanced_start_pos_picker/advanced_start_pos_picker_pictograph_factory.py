from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter

from Enums.Enums import LetterType


from base_widgets.base_pictograph.pictograph import Pictograph


if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.start_pos_picker.start_pos_picker import (
        StartPosPicker,
    )


class AdvancedStartPosPickerPictographFactory:
    def __init__(
        self,
        advanced_start_pos_picker: "StartPosPicker",
        advanced_start_pos_cache: dict[str, Pictograph],
    ) -> None:
        self.advanced_start_pos_picker = advanced_start_pos_picker
        self.advanced_start_pos_cache = advanced_start_pos_cache

    def get_or_create_pictograph(
        self, pictograph_key: str, pictograph_data=None
    ) -> Pictograph:
        letter_str = pictograph_key.split("_")[0]
        letter = Letter.get_letter(letter_str)

        if pictograph_key in self.advanced_start_pos_cache.get(letter, {}):
            return self.advanced_start_pos_cache[letter][pictograph_key]

        if pictograph_data is not None:
            pictograph = self.create_pictograph()
            pictograph.updater.update_pictograph(pictograph_data)

            if letter not in self.advanced_start_pos_cache:
                self.advanced_start_pos_cache[letter] = {}
            self.advanced_start_pos_cache[letter][pictograph_key] = pictograph
            self.advanced_start_pos_picker.main_widget.pictograph_cache[letter][
                pictograph_key
            ] = pictograph
            letter_type = LetterType.get_letter_type(letter)
            for letter_type in LetterType:
                if letter in letter_type.letters:
                    letter_type = letter_type
                    break

            return pictograph

        raise ValueError(
            "BasePictograph dict is required for creating a new pictograph."
        )

    def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
        keys_to_remove = [
            key
            for key in self.advanced_start_pos_cache
            if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            pictograph = self.advanced_start_pos_cache.pop(key)
            pictograph.view.setParent(None)

    def get_pictograph(self, pictograph_key) -> Pictograph:
        return self.advanced_start_pos_cache[pictograph_key]

    def create_pictograph(self) -> Pictograph:
        pictograph = Pictograph(
            self.advanced_start_pos_picker.main_widget,
        )
        return pictograph
