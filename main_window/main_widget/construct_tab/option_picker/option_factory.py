from typing import TYPE_CHECKING, Callable, List
from PyQt6.QtCore import QSize
from base_widgets.pictograph.pictograph_scene import PictographScene
from .option_view import OptionView
if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_picker import OptionPicker
class OptionFactory:
    MAX_PICTOGRAPHS = 36

    def __init__(self, option_picker: "OptionPicker", mw_size_provider: Callable[[], QSize]) -> None:
        self.option_picker = option_picker
        self.mw_size_provider = mw_size_provider
        # Build the option pool upon instantiation.
        self.option_picker.option_pool = self.create_options()

    def create_options(self) -> List[PictographScene]:
        options: List[PictographScene] = []
        for _ in range(self.MAX_PICTOGRAPHS):
            opt = PictographScene()
            # Construct the view using OptionView, passing the picker and size provider.
            opt.view = OptionView(self.option_picker, opt, self.mw_size_provider)
            options.append(opt)
        return options
