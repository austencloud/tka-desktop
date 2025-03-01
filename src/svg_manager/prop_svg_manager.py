from typing import TYPE_CHECKING
from data.constants import BLUE, PROP_DIR
from enums.prop_type import PropType
from objects.prop.prop import Prop
from utils.path_helpers import get_images_and_data_path
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

        # If it's the chicken, skip SVG logic and do PNG logic
        if prop.prop_type_str == "Chicken":
            self._setup_prop_png_renderer(prop, image_file)
            return

        # Otherwise, do normal SVG logic
        svg_data = self.manager.load_svg_file(image_file)
        if prop.prop_type_str != "Hand":
            colored_svg_data = self.manager.color_manager.apply_color_transformations(
                svg_data, prop.color
            )
        else:
            colored_svg_data = svg_data
        self._setup_prop_svg_renderer(prop, colored_svg_data)

    def _get_prop_image_file(self, prop: "Prop") -> str:
        # same logic you had before
        if prop.prop_type_str == "Hand":
            return self._get_hand_svg_file(prop)
        elif prop.prop_type_str == "Chicken":
            return f"{PROP_DIR}{prop.prop_type_str}.png"
        else:
            return f"{PROP_DIR}{prop.prop_type_str}.svg"

    def _get_hand_svg_file(self, prop: "Prop") -> str:
        hand_color = "left" if prop.color == BLUE else "right"
        return get_images_and_data_path(f"images/hands/{hand_color}_hand.svg")

    def _setup_prop_svg_renderer(self, prop: "Prop", svg_data: str) -> None:
        # same as your original
        prop.renderer = QSvgRenderer()
        prop.renderer.load(svg_data.encode("utf-8"))
        prop.setSharedRenderer(prop.renderer)

    def _setup_prop_png_renderer(self, prop: "Prop", png_path: str) -> None:
        """
        Instead of an SVG, load the PNG into a QPixmap and attach it to 'prop'.
        Because 'prop' is presumably a QGraphicsItem (or QGraphicsSvgItem),
        we'll create a child QGraphicsPixmapItem to actually display the PNG.
        """
        full_path = get_images_and_data_path(png_path)
        pixmap = QPixmap(full_path)

        # Step A: Possibly hide or remove the old SVG renderer if it exists
        if hasattr(prop, "renderer") and prop.renderer:
            prop.renderer = None

        # Step B: Create or re-use a child QGraphicsPixmapItem
        if not hasattr(prop, "pixmap_item") or not prop.pixmap_item:
            # Create one the first time
            from PyQt6.QtWidgets import QGraphicsPixmapItem

            prop.pixmap_item = QGraphicsPixmapItem(pixmap, parent=prop)
        else:
            # Already exist? just update the pixmap
            prop.pixmap_item.setPixmap(pixmap)

        # Step C: Optionally adjust the anchor point or offset so
        #   that the center lines up with your expected "centerPoint"
        #   For instance:
        prop.pixmap_item.setOffset(-pixmap.width() / 2, -pixmap.height() / 2)

        # Step D: Make sure 'prop' paints no SVG
        prop.setFlag(prop.GraphicsItemFlag.ItemHasNoContents, True)
