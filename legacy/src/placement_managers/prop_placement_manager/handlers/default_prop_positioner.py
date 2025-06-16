# default_prop_positioner.py

from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING
from objects.prop.prop import Prop
import logging
from functools import lru_cache

if TYPE_CHECKING:
    from base_widgets.pictograph.grid.grid_point import GridPoint
    from ..prop_placement_manager import PropPlacementManager
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph

logger = logging.getLogger(__name__)


class DefaultPropPositioner:
    def __init__(self, prop_placement_manager: "PropPlacementManager") -> None:
        self.pictograph: "LegacyPictograph" = prop_placement_manager.pictograph
        self.prop_placement_manager = prop_placement_manager

    def set_prop_to_default_loc(self, prop: Prop) -> None:
        """
        Sets the prop to its default location based on its `loc` attribute.
        """
        strict = self.pictograph.managers.check.has_strict_placed_props()

        point_suffix = "_strict" if strict else ""

        point_name = f"{prop.state.loc}_{prop.pictograph.state.grid_mode}_hand_point{point_suffix}"

        grid_point = self.get_grid_point(point_name, strict)

        if grid_point and grid_point.coordinates:
            self.place_prop_at_hand_point(prop, grid_point.coordinates)
        else:
            logger.warning(
                f"Hand point '{point_name}' not found or has no coordinates."
            )

    # default_prop_positioner.py

    def place_prop_at_hand_point(self, prop: Prop, hand_point: QPointF) -> None:
        """
        Align the prop's center to the hand point using either:
        - The 'centerPoint' from the SVG (for normal SVG props), or
        - The boundingRect's center (for Chicken's PNG).
        """
        # 1) Decide which center method to call
        if prop.prop_type_str == "Chicken":
            center_point_in_local_coords = self.get_png_center_point(prop)
        else:
            center_point_in_local_coords = self.get_svg_center_point(prop)

        # 2) Convert that local coordinate to scene coords
        center_point_in_scene = prop.mapToScene(center_point_in_local_coords)

        # 3) Calculate how far we need to shift to place it at 'hand_point'
        offset = hand_point - center_point_in_scene
        new_position = prop.pos() + offset

        # 4) Move the prop
        prop.setPos(new_position)

    def _get_grid_mode_from_prop_loc(self, prop: "Prop") -> str:
        if prop.state.loc in ["ne", "nw", "se", "sw"]:
            grid_mode = BOX
        elif prop.state.loc in ["n", "s", "e", "w"]:
            grid_mode = DIAMOND
        return grid_mode

    def get_png_center_point(self, prop: Prop) -> QPointF:
        """
        For PNG-based props (like Chicken), compute the center
        by looking at the boundingRect, i.e. half the width/height.
        """
        bounding_rect = prop.boundingRect()
        return bounding_rect.center()

    def get_svg_center_point(self, prop: Prop) -> QPointF:
        """
        Retrieve the 'centerPoint' from the SVG.
        """
        element_bounding_box = prop.renderer.boundsOnElement("centerPoint")
        center_point_in_svg = element_bounding_box.center()

        return center_point_in_svg

    @lru_cache(maxsize=128)
    def get_grid_point(self, point_name: str, strict: bool) -> "GridPoint | None":
        """
        Returns a grid point by name, using a cache.
        """
        location_points = (
            self.pictograph.elements.grid.grid_data.all_hand_points_strict
            if strict
            else self.pictograph.elements.grid.grid_data.all_hand_points_normal
        )
        return location_points.get(point_name)
