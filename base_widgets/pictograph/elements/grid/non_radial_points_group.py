import xml.etree.ElementTree as ET
from PyQt6.QtWidgets import QGraphicsItemGroup

from utilities.path_helpers import get_images_and_data_path
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
        tree = ET.parse(get_images_and_data_path(path))
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

