from typing import TYPE_CHECKING
from objects.arrow.arrow_svg_manager import ArrowSvgManager
from svg_manager.svg_color_handler import SvgColorHandler
from svg_manager.prop_svg_manager import PropSvgManager
from utils.path_helpers import get_data_path, get_image_path

if TYPE_CHECKING:
    from base_widgets.pictograph.pictograph import Pictograph


class SvgManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

        self.color_manager = SvgColorHandler(self)
        self.arrow_manager = ArrowSvgManager(self)
        self.prop_manager = PropSvgManager(self)

    def load_svg_file(self, svg_path: str) -> str:
        with open(get_image_path(svg_path), "r") as file:
            svg_data = file.read()
        return svg_data
