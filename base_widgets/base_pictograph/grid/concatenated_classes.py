# From grid.py
from typing import TYPE_CHECKING

from .grid_data import GridData
from .grid_item import GridItem
from .non_radial_points_group import NonRadialPointsGroup

if TYPE_CHECKING:
    from ..pictograph import Pictograph

GRID_DIR = "images/grid/"


class Grid:
    def __init__(self, pictograph: "Pictograph", grid_data: GridData, grid_mode: str):

        self.pictograph = pictograph
        self.grid_data = grid_data
        self.grid_mode = grid_mode
        self.items: dict[str, GridItem] = {}
        self.center = self.grid_data.center_points.get(grid_mode)

        self._create_grid_items()

    def _create_grid_items(self):
        paths = {
            "diamond": f"{GRID_DIR}diamond_grid.svg",
            "box": f"{GRID_DIR}box_grid.svg",
        }

        for mode, path in paths.items():
            grid_item = GridItem(path)
            self.pictograph.addItem(grid_item)
            grid_item.setVisible(mode == self.grid_mode)
            self.items[mode] = grid_item

        non_radial_paths = {
            "diamond": f"{GRID_DIR}diamond_nonradial_points.svg",
            "box": f"{GRID_DIR}box_nonradial_points.svg",
        }

        non_radial_path = non_radial_paths.get(self.grid_mode)
        if non_radial_path:
            non_radial_points = NonRadialPointsGroup(non_radial_path)
            self.pictograph.addItem(non_radial_points)
            is_visible = (
                self.pictograph.main_widget.settings_manager.visibility.get_non_radial_visibility()
            )
            non_radial_points.setVisible(is_visible)
            self.items[f"{self.grid_mode}_nonradial"] = non_radial_points

    def toggle_non_radial_points(self, visible: bool):
        non_radial_key = f"{self.grid_mode}_nonradial"
        self.items[non_radial_key].setVisible(visible)

    def hide(self):
        for item in self.items.values():
            item.setVisible(False)

    def update_grid_mode(self):
        grid_mode = self.pictograph.main_widget.grid_mode_checker.get_grid_mode(
            self.pictograph.pictograph_data
        )
        self.pictograph.grid.hide()
        self.pictograph.grid.__init__(
            self.pictograph, self.pictograph.grid.grid_data, grid_mode
        )


# From grid_data.py
from typing import Optional
from PyQt6.QtCore import QPointF
from .grid_layer import GridLayer
from .grid_point import GridPoint


class GridData:
    def __init__(self, data: dict[str, dict[str, dict[str, str]]]) -> None:
        self.all_layer2_points: dict[str, GridPoint] = {}
        self.all_hand_points_normal: dict[str, GridPoint] = {}
        self.all_hand_points_strict: dict[str, GridPoint] = {}
        self.all_layer2_points_strict: dict[str, GridPoint] = {}
        self.all_outer_points: dict[str, GridPoint] = {}
        self.center_points: dict[str, QPointF] = {}

        for mode, mode_data in data.items():
            layer2_normal = GridLayer(mode_data["layer2_points"]["normal"])
            self.all_layer2_points.update(layer2_normal.points)

            layer2_strict = GridLayer(mode_data["layer2_points"]["strict"])
            self.all_layer2_points_strict.update(layer2_strict.points)

            hand_normal = GridLayer(mode_data["hand_points"]["normal"])
            self.all_hand_points_normal.update(hand_normal.points)

            hand_strict = GridLayer(mode_data["hand_points"]["strict"])
            self.all_hand_points_strict.update(hand_strict.points)

            outer_points = GridLayer(mode_data["outer_points"])
            self.all_outer_points.update(outer_points.points)

            center_coords = mode_data.get("center_point", "None")
            if center_coords != "None":
                try:
                    x, y = map(float, center_coords.strip("()").split(", "))
                    self.center_points[mode] = QPointF(x, y)
                except ValueError:
                    self.center_points[mode] = QPointF(0, 0)
            else:
                self.center_points[mode] = QPointF(0, 0)

    def get_shift_coord(self, point_name: str) -> Optional[QPointF]:
        point = self.all_layer2_points.get(point_name)
        if point and point.coordinates:
            return point.coordinates
        else:

            return None

    def get_static_coord(self, point_name: str) -> Optional[QPointF]:
        point = self.all_hand_points_normal.get(point_name)
        if point and point.coordinates:
            return point.coordinates
        else:

            return None

    def get_point(
        self, layer: dict[str, GridPoint], pos: QPointF
    ) -> Optional[GridPoint]:
        min_distance = float("inf")
        closest_point = None
        for point in layer.values():
            if point.coordinates:
                distance = (pos - point.coordinates).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point

        return closest_point


# From grid_item.py
import logging
from typing import TYPE_CHECKING
from PyQt6.QtSvgWidgets import QGraphicsSvgItem


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    pass

GRID_DIR = "images/grid/"


class GridItem(QGraphicsSvgItem):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setZValue(100)

    def wheelEvent(self, event) -> None:
        event.ignore()

    def mousePressEvent(self, event) -> None:
        event.ignore()

    def mouseMoveEvent(self, event) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:
        event.ignore()


# From grid_layer.py
from PyQt6.QtCore import QPointF
from base_widgets.base_pictograph.grid.grid_point import GridPoint


class GridLayer:
    def __init__(self, points_data: dict[str, str]) -> None:
        self.points: dict[str, GridPoint] = {}
        for name, coords in points_data.items():
            if coords != "None":
                try:
                    x, y = map(float, coords.strip("()").split(", "))
                    self.points[name] = GridPoint(name, QPointF(x, y))
                except ValueError:
                    self.points[name] = GridPoint(name, None)
            else:
                self.points[name] = GridPoint(name, None)


# From grid_point.py
from typing import Optional
from PyQt6.QtCore import QPointF


class GridPoint:
    def __init__(self, name: str, coordinates: Optional[QPointF]) -> None:
        self.name = name
        self.coordinates = coordinates


# From non_radial_point.py
from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QBrush, QPen, QColor
from PyQt6.QtCore import QPointF, Qt


class NonRadialGridPoint(QGraphicsEllipseItem):
    def __init__(self, x, y, r, point_id):
        super().__init__(-r, -r, 2 * r, 2 * r)
        self.setBrush(QBrush(QColor("black")))
        self.setPen(QPen(Qt.PenStyle.NoPen))
        self.setPos(QPointF(x, y))
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)
        self.setToolTip(point_id)
        self.point_id = point_id
        self.setZValue(101)


# From non_radial_points_group.py
import xml.etree.ElementTree as ET
from PyQt6.QtWidgets import QGraphicsItemGroup
from .non_radial_point import NonRadialGridPoint


class NonRadialPointsGroup(QGraphicsItemGroup):
    """Manages a group of non-radial points."""

    name = "non_radial_points"

    def __init__(self, path: str):
        super().__init__()
        self.setFlag(self.GraphicsItemFlag.ItemHasNoContents, True)
        self.setFiltersChildEvents(False)
        self.child_points: list[NonRadialGridPoint] = []
        self._parse_svg(path)

    def _parse_svg(self, path: str):
        """Parse the SVG file and create child points."""
        tree = ET.parse(path)
        root = tree.getroot()
        namespace = {"": "http://www.w3.org/2000/svg"}

        non_radial_group = root.find(".//*[@id='non_radial_points']", namespace)
        if non_radial_group is None:
            return

        for circle in non_radial_group.findall("circle", namespace):
            cx = float(circle.attrib.get("cx", 0))
            cy = float(circle.attrib.get("cy", 0))
            r = float(circle.attrib.get("r", 0))
            point_id = circle.attrib.get("id", "unknown_point")
            point = NonRadialGridPoint(cx, cy, r, point_id)
            point.setParentItem(self)  # Add point to the group
            self.child_points.append(point)
