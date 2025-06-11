from typing import TYPE_CHECKING
from data.constants import BLUE, PROP_DIR
from enums.prop_type import PropType
from objects.prop.prop import Prop
from utils.path_helpers import get_data_path, get_image_path
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPixmap

if TYPE_CHECKING:
    from svg_manager.svg_manager import SvgManager
    from objects.prop.prop import Prop


class PropSvgManager:
    def __init__(self, manager: "SvgManager"):
        self.manager = manager

    def update_prop_image(self, prop: "Prop") -> None:
        image_file = self._get_prop_image_file(prop)
        if prop.prop_type_str == "Chicken":
            self._setup_prop_png_renderer(prop, image_file)
            return
        svg_data = self.manager.load_svg_file(image_file)
        if prop.prop_type_str != "Hand":
            colored_svg_data = self.manager.color_manager.apply_color_transformations(
                svg_data, prop.state.color
            )
        else:
            colored_svg_data = svg_data
        self._setup_prop_svg_renderer(prop, colored_svg_data)

    def _get_prop_image_file(self, prop: "Prop") -> str:
        if prop.prop_type_str == "Hand":
            return self._get_hand_svg_file(prop)
        elif prop.prop_type_str == "Chicken":
            return f"{PROP_DIR}{prop.prop_type_str.lower()}.png"
        elif prop.prop_type_str == "Simplestaff":
            return f"{PROP_DIR}simple_staff.svg"
        else:
            # Always use lowercase for file names to avoid case sensitivity issues
            return f"{PROP_DIR}{prop.prop_type_str.lower()}.svg"

    def _get_hand_svg_file(self, prop: "Prop") -> str:
        hand_color = "left" if prop.state.color == BLUE else "right"
        return get_image_path(f"hands/{hand_color}_hand.svg")

    def _setup_prop_svg_renderer(self, prop: "Prop", svg_data: str) -> None:
        prop.renderer = QSvgRenderer()
        prop.renderer.load(svg_data.encode("utf-8"))
        prop.setSharedRenderer(prop.renderer)

    def _setup_prop_png_renderer(self, prop: "Prop", png_path: str) -> None:
        full_path = get_image_path(png_path)
        pixmap = QPixmap(full_path)
        if hasattr(prop, "renderer") and prop.renderer:
            prop.renderer = None
        if not hasattr(prop, "pixmap_item") or not prop.pixmap_item:
            from PyQt6.QtWidgets import QGraphicsPixmapItem

            prop.pixmap_item = QGraphicsPixmapItem(pixmap, parent=prop)
        else:
            prop.pixmap_item.setPixmap(pixmap)
        prop.pixmap_item.setOffset(-pixmap.width() / 2, -pixmap.height() / 2)
        prop.setFlag(prop.GraphicsItemFlag.ItemHasNoContents, True)
