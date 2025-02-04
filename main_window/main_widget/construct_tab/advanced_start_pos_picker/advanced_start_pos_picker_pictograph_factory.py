from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter

from Enums.Enums import LetterType


from base_widgets.base_pictograph.base_pictograph import BasePictograph


if TYPE_CHECKING:
    from ..components.start_pos_picker.start_pos_picker import StartPosPicker


class AdvancedStartPosPickerPictographFactory:
    def __init__(
        self,
        advanced_start_pos_picker: "StartPosPicker",
        advanced_start_pos_cache: dict[str, BasePictograph],
    ) -> None:
        self.advanced_start_pos_picker = advanced_start_pos_picker
        self.advanced_start_pos_cache = advanced_start_pos_cache

    def get_or_create_pictograph(
        self, pictograph_key: str, pictograph_dict=None
    ) -> BasePictograph:
        letter_str = pictograph_key.split("_")[0]
        letter = Letter.get_letter(letter_str)

        if pictograph_key in self.advanced_start_pos_cache.get(letter, {}):
            return self.advanced_start_pos_cache[letter][pictograph_key]

        if pictograph_dict is not None:
            pictograph = self.create_pictograph()
            pictograph.updater.update_pictograph(pictograph_dict)

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

        raise ValueError("Pictograph dict is required for creating a new pictograph.")

    def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
        keys_to_remove = [
            key
            for key in self.advanced_start_pos_cache
            if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            pictograph = self.advanced_start_pos_cache.pop(key)
            pictograph.view.setParent(None)

    def get_pictograph(self, pictograph_key) -> BasePictograph:
        return self.advanced_start_pos_cache[pictograph_key]

    def create_pictograph(self) -> BasePictograph:
        pictograph = BasePictograph(
            self.advanced_start_pos_picker.main_widget,
        )
        return pictograph
