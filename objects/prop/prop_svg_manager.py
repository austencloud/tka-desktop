from typing import TYPE_CHECKING
from data.constants import BLUE, PROP_DIR
from Enums.PropTypes import PropType

if TYPE_CHECKING:
    from objects.prop.prop import Prop
    from base_widgets.base_pictograph.svg_manager import SvgManager
from utilities.path_helpers import get_images_and_data_path

from typing import TYPE_CHECKING
from PyQt6.QtSvg import QSvgRenderer
from objects.prop.prop import Prop
from Enums.PropTypes import PropType
from data.constants import BLUE, PROP_DIR

if TYPE_CHECKING:
    from base_widgets.base_pictograph.svg_manager import (
        SvgManager,
    )


class PropSvgManager:
    def __init__(self, manager: "SvgManager"):
        self.manager = manager

    def update_prop_svg(self, prop: "Prop") -> None:
        svg_file = self._get_prop_svg_file(prop)
        svg_data = self.manager.load_svg_file(svg_file)
        if prop.prop_type != PropType.Hand:
            colored_svg_data = self.manager.color_manager.apply_color_transformations(
                svg_data, prop.color
            )
        else:
            colored_svg_data = svg_data
        self._setup_prop_svg_renderer(prop, colored_svg_data)

    def _get_prop_svg_file(self, prop: "Prop") -> str:
        prop_type_str = prop.prop_type.name.lower()
        if prop.prop_type == PropType.Hand:
            return self._get_hand_svg_file(prop)

        return f"{PROP_DIR}{prop_type_str}.svg"

    def _get_hand_svg_file(self, prop: "Prop") -> str:
        hand_color = "left" if prop.color == BLUE else "right"
        return get_images_and_data_path(f"images/hands/{hand_color}_hand.svg")

    def _setup_prop_svg_renderer(self, prop: "Prop", svg_data: str) -> None:
        prop.renderer = QSvgRenderer()
        prop.renderer.load(svg_data.encode("utf-8"))
        prop.setSharedRenderer(prop.renderer)
