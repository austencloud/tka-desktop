from typing import TYPE_CHECKING, Callable
from base_widgets.pictograph.pictograph_scene import PictographScene
from .option_view import OptionView
from PyQt6.QtCore import QSize

if TYPE_CHECKING:
    from .option_picker import OptionPicker


class OptionFactory:
    MAX_PICTOGRAPHS = 36

    def __init__(
        self, op: "OptionPicker", mw_size_provider: Callable[[], QSize] = None
    ):
        self.option_picker = op
        self.mw_size_provider = mw_size_provider
        self.create_options()

    def create_options(self) -> list[PictographScene]:
        opts = []
        for _ in range(self.MAX_PICTOGRAPHS):
            opt = PictographScene()
            opt.view = OptionView(self.option_picker, opt, self.mw_size_provider)
            opts.append(opt)
        self.option_picker.option_pool = opts
        return opts
