"""
Prop renderer for pictograph components.

Handles rendering of prop elements with positioning and rotation.
"""

import os
import re
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from .asset_utils import get_image_path
from ...domain.models.core_models import (
    MotionData,
    Location,
)
from ...application.services.motion_orientation_service import (
    MotionOrientationService,
    Orientation,
)


class PropRenderer:
    """Handles prop rendering for pictographs."""

    def __init__(self, scene):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.HAND_RADIUS = 143.1
        self.orientation_service = MotionOrientationService()

        self.location_coordinates = {
            Location.NORTH: (0, -self.HAND_RADIUS),
            Location.EAST: (self.HAND_RADIUS, 0),
            Location.SOUTH: (0, self.HAND_RADIUS),
            Location.WEST: (-self.HAND_RADIUS, 0),
            Location.NORTHEAST: (self.HAND_RADIUS * 0.707, -self.HAND_RADIUS * 0.707),
            Location.SOUTHEAST: (self.HAND_RADIUS * 0.707, self.HAND_RADIUS * 0.707),
            Location.SOUTHWEST: (-self.HAND_RADIUS * 0.707, self.HAND_RADIUS * 0.707),
            Location.NORTHWEST: (-self.HAND_RADIUS * 0.707, -self.HAND_RADIUS * 0.707),
        }

    def render_prop(self, color: str, motion_data: MotionData) -> None:
        """Render a prop using SVG files with exact scaling and rotation."""
        prop_svg_path = get_image_path("props/staff.svg")

        if os.path.exists(prop_svg_path):
            prop_item = QGraphicsSvgItem()

            # Apply color transformation to SVG data
            svg_data = self._load_svg_file(prop_svg_path)
            colored_svg_data = self._apply_color_transformation(svg_data, color)

            renderer = QSvgRenderer(bytearray(colored_svg_data, encoding="utf-8"))
            if renderer.isValid():
                prop_item.setSharedRenderer(renderer)

                # NO INDIVIDUAL SCALING - positioning service assumes full-size scene
                # All scaling will be applied to the entire scene as final step

                end_pos = self._get_location_position(motion_data.end_loc)
                target_hand_point_x = self.CENTER_X + end_pos[0]
                target_hand_point_y = self.CENTER_Y + end_pos[1]

                prop_rotation = self._calculate_prop_rotation(motion_data)
                bounds = prop_item.boundingRect()
                prop_item.setTransformOriginPoint(bounds.center())
                prop_item.setRotation(prop_rotation)

                self._place_prop_at_hand_point(
                    prop_item, target_hand_point_x, target_hand_point_y
                )

                self.scene.addItem(prop_item)

    def _place_prop_at_hand_point(
        self, prop_item: QGraphicsSvgItem, target_x: float, target_y: float
    ) -> None:
        """Position prop using coordinate system approach."""
        bounds = prop_item.boundingRect()
        center_point_in_local_coords = bounds.center()
        center_point_in_scene = prop_item.mapToScene(center_point_in_local_coords)
        target_hand_point = QPointF(target_x, target_y)
        offset = target_hand_point - center_point_in_scene
        new_position = prop_item.pos() + offset
        prop_item.setPos(new_position)

    def _get_location_position(self, location: Location) -> tuple[float, float]:
        """Get the coordinate position for a location."""
        return self.location_coordinates.get(location, (0, 0))

    def _calculate_prop_rotation(self, motion_data: MotionData) -> float:
        """Calculate prop rotation using orientation-based system."""
        # Use the orientation service to calculate the correct rotation angle
        # This follows the reference implementation's orientation calculation
        return self.orientation_service.get_prop_rotation_angle(
            motion_data, Orientation.IN
        )

    def _load_svg_file(self, file_path: str) -> str:
        """Load SVG file content as string."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            print(f"Error loading SVG file {file_path}: {e}")
            return ""

    def _apply_color_transformation(self, svg_data: str, color: str) -> str:
        """Apply color transformation to SVG data based on prop color."""
        if not svg_data:
            return svg_data

        # Color mapping based on reference implementation
        COLOR_MAP = {
            "blue": "#2E3192",  # Reference blue color
            "red": "#ED1C24",  # Reference red color
        }

        target_color = COLOR_MAP.get(color.lower(), "#2E3192")  # Default to blue

        # Pattern to match CSS fill properties in SVG
        # This matches both fill attributes and CSS style properties
        patterns = [
            # CSS fill property: fill="#color"
            re.compile(r'(fill=")([^"]*)(")'),
            # CSS style attribute: fill: #color;
            re.compile(r"(fill:\s*)([^;]*)(;)"),
            # Class definition: .st0 { fill: #color; }
            re.compile(r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)([^;}]*)([^}]*?\})"),
        ]

        # Apply color transformation using all patterns
        for pattern in patterns:
            svg_data = pattern.sub(
                lambda m: m.group(1) + target_color + m.group(len(m.groups())), svg_data
            )

        return svg_data
