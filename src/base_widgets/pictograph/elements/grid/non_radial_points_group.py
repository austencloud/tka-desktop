import os
import xml.etree.ElementTree as ET
from PyQt6.QtWidgets import QGraphicsItemGroup

from utils.path_helpers import get_data_path, get_image_path
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
        try:
            # Get the image path and try to parse the SVG file
            image_path = get_image_path(path)

            # Check if the file exists
            if not os.path.exists(image_path):
                print(f"Warning: SVG file not found at {image_path}")
                self._create_default_points()
                return

            # Parse the SVG file
            tree = ET.parse(image_path)
            root = tree.getroot()
            namespace = {"": "http://www.w3.org/2000/svg"}

            # Find the non-radial points group
            non_radial_group = root.find(".//*[@id='non_radial_points']", namespace)
            if non_radial_group is None:
                print(f"Warning: No 'non_radial_points' group found in {image_path}")
                self._create_default_points()
                return

            # Create points from the SVG circles
            for circle in non_radial_group.findall("circle", namespace):
                cx = float(circle.attrib.get("cx", 0))
                cy = float(circle.attrib.get("cy", 0))
                r = float(circle.attrib.get("r", 0))
                point_id = circle.attrib.get("id", "unknown_point")
                point = NonRadialGridPoint(cx, cy, r, point_id)
                point.setParentItem(self)  # Add point to the group
                self.child_points.append(point)

        except Exception as e:
            print(f"Error parsing SVG file {path}: {e}")
            self._create_default_points()

    def _create_default_points(self):
        """Create default points when the SVG file cannot be loaded."""
        print("Creating default non-radial points")

        # Create a set of default points in a grid pattern
        for x in range(-2, 3):
            for y in range(-2, 3):
                # Skip the center point (0,0) as it's usually covered by the radial points
                if x == 0 and y == 0:
                    continue

                # Calculate position (scale by 50 to space them out)
                cx = x * 50
                cy = y * 50
                r = 5  # Default radius
                point_id = f"default_point_{x}_{y}"

                # Create and add the point
                point = NonRadialGridPoint(cx, cy, r, point_id)
                point.setParentItem(self)
                self.child_points.append(point)
