from typing import TYPE_CHECKING
from objects.arrow.arrow_svg_manager import ArrowSvgManager
from objects.graphical_object.svg_manager.svg_color_handler import SvgColorHandler
from objects.prop.prop_svg_manager import PropSvgManager
from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from base_widgets.base_pictograph.pictograph import Pictograph
    from main_window.main_widget.main_widget import MainWidget


class SvgManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

        self.color_manager = SvgColorHandler(self)
        self.arrow_manager = ArrowSvgManager(self)
        self.prop_manager = PropSvgManager(self)

    def load_svg_file(self, svg_path: str) -> str:
        with open(get_images_and_data_path(svg_path), "r") as file:
            svg_data = file.read()
        return svg_data
