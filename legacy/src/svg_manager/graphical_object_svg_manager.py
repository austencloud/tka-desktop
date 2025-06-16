from typing import TYPE_CHECKING
from utils.path_helpers import get_data_path
from .arrow_svg_manager import ArrowSvgManager
from .prop_svg_manager import PropSvgManager
from ....svg_manager.svg_color_manager import SvgColorManager

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SvgManager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

        self.color_manager = SvgColorManager(self)
        self.arrow_manager = ArrowSvgManager(self)
        self.prop_manager = PropSvgManager(self)

    def load_svg_file(self, svg_path: str) -> str:
        with open(get_data_path(svg_path), "r") as file:
            svg_data = file.read()
        return svg_data
