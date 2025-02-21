from typing import TYPE_CHECKING, Callable
from base_widgets.pictograph.pictograph import Pictograph
from .option_view import OptionView
from PyQt6.QtCore import QSize

if TYPE_CHECKING:
    from .option_picker import OptionPicker
    from base_widgets.pictograph.pictograph import Pictograph


class OptionFactory:
    MAX_PICTOGRAPHS = 36

    def __init__(
        self,
        option_picker: "OptionPicker",
        mw_size_provider: Callable[[], QSize] = None,
    ):
        self.option_picker = option_picker
        self.mw_size_provider = mw_size_provider
        self.create_options()

    def create_options(self) -> list[Pictograph]:
        options = []
        for _ in range(self.MAX_PICTOGRAPHS):
            option = Pictograph()
            option.view = OptionView(self.option_picker, option, self.mw_size_provider)
            options.append(option)
        self.option_picker.option_pool = options
