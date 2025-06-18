"""
Prop renderer for pictograph components.

Handles rendering of prop elements with positioning and rotation.
"""

import os
import re
from typing import TYPE_CHECKING, Any
from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from domain.models.core_models import MotionData, Location

from presentation.components.pictograph.asset_utils import get_image_path

from domain.models.core_models import Orientation
from application.services.positioning.prop_management_service import (
    PropManagementService,
)

if TYPE_CHECKING:
    from presentation.components.pictograph.pictograph_scene import PictographScene


class PropRenderer:
    """Handles prop rendering for pictographs."""

    def __init__(self, scene: "PictographScene"):
        self.scene = scene
        self.CENTER_X = 475
        self.CENTER_Y = 475
        self.HAND_RADIUS = 143.1
        self.prop_management_service = PropManagementService()

        # Store rendered props for overlap detection
        self.rendered_props: dict[str, QGraphicsSvgItem] = {}

        self.location_coordinates = {
            Location.NORTH.value: (0, -self.HAND_RADIUS),
            Location.EAST.value: (self.HAND_RADIUS, 0),
            Location.SOUTH.value: (0, self.HAND_RADIUS),
            Location.WEST.value: (-self.HAND_RADIUS, 0),
            Location.NORTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHEAST.value: (
                self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.SOUTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                self.HAND_RADIUS * 0.707,
            ),
            Location.NORTHWEST.value: (
                -self.HAND_RADIUS * 0.707,
                -self.HAND_RADIUS * 0.707,
            ),
        }

    def render_prop(self, color: str, motion_data: MotionData) -> None:
        """Render a prop using SVG files with exact scaling and rotation."""
        prop_svg_path = get_image_path("props/staff.svg")

        if not os.path.exists(prop_svg_path):
            print(f"Warning: Prop asset not found: {prop_svg_path}")
            return

        prop_item = QGraphicsSvgItem()
        svg_data = self._load_svg_file(prop_svg_path)
        colored_svg_data = self._apply_color_transformation(svg_data, color)

        renderer = QSvgRenderer(bytearray(colored_svg_data, encoding="utf-8"))
        if not renderer.isValid():
            print(f"Warning: Invalid SVG renderer for {prop_svg_path}")
            return

        prop_item.setSharedRenderer(renderer)

        # Get position with validation
        end_pos = self._get_location_position(motion_data.end_loc)
        if end_pos == (0, 0) and motion_data.end_loc != Location.NORTH:
            print(
                f"Warning: Invalid location {motion_data.end_loc}, using default position"
            )
            # Use a valid default position instead of center
            end_pos = self.location_coordinates[Location.NORTH.value]

        target_hand_point_x = self.CENTER_X + end_pos[0]
        target_hand_point_y = self.CENTER_Y + end_pos[1]

        prop_rotation = self._calculate_prop_rotation(motion_data)
        bounds = prop_item.boundingRect()
        prop_item.setTransformOriginPoint(bounds.center())
        prop_item.setRotation(prop_rotation)

        self._place_prop_at_hand_point(
            prop_item, target_hand_point_x, target_hand_point_y
        )

        # Store rendered prop for potential beta positioning
        self.rendered_props[color] = prop_item

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
        position = self.location_coordinates.get(location.value)
        if position is None:
            print(f"Warning: Unknown location {location}, using NORTH as fallback")
            return self.location_coordinates[Location.NORTH.value]
        return position

    def _calculate_prop_rotation(self, motion_data: MotionData) -> float:
        """Calculate prop rotation using orientation-based system."""
        # Use the orientation service to calculate the correct rotation angle
        # This follows the reference implementation's orientation calculation
        return self.prop_management_service.calculate_prop_rotation_angle(
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

    def apply_beta_positioning(self, beat_data: Any) -> None:
        """
        Apply beta prop positioning if conditions are met.

        This method should be called after both props are rendered
        to detect overlaps and apply separation offsets.

        Args:
            beat_data: BeatData containing motion information
        """
        # Import here to avoid circular imports
        from domain.models.core_models import BeatData

        if not isinstance(beat_data, BeatData):
            return  # Check if beta positioning should be applied
        if not self.prop_management_service.should_apply_beta_positioning(beat_data):
            return

        # Check if we have both props rendered
        if "blue" not in self.rendered_props or "red" not in self.rendered_props:
            return

        # Calculate separation offsets
        blue_offset, red_offset = (
            self.prop_management_service.calculate_separation_offsets(beat_data)
        )

        # Apply offsets to rendered props
        blue_prop = self.rendered_props["blue"]
        red_prop = self.rendered_props["red"]

        # Apply offsets to current positions
        blue_current_pos = blue_prop.pos()
        red_current_pos = red_prop.pos()

        new_blue_pos = blue_current_pos + blue_offset
        new_red_pos = red_current_pos + red_offset

        blue_prop.setPos(new_blue_pos)
        red_prop.setPos(new_red_pos)

    def clear_rendered_props(self) -> None:
        """Clear the rendered props cache."""
        self.rendered_props.clear()
