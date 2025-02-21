# default_prop_positioner.py

from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING
from objects.prop.prop import Prop
import logging

if TYPE_CHECKING:
    from base_widgets.pictograph.grid.grid import GridPoint
    from ..prop_placement_manager import PropPlacementManager
    from base_widgets.pictograph.pictograph import Pictograph

logger = logging.getLogger(__name__)


class DefaultPropPositioner:
    def __init__(self, prop_placement_manager: "PropPlacementManager") -> None:
        self.pictograph: "Pictograph" = prop_placement_manager.pictograph
        self.prop_placement_manager = prop_placement_manager
        self.location_points_cache = {}

    def set_prop_to_default_loc(self, prop: Prop) -> None:
        """
        Sets the prop to its default location based on its `loc` attribute.
        """
        strict = self.pictograph.check.has_strictly_placed_props()

        point_suffix = "_strict" if strict else ""

        point_name = f"{prop.loc}_{prop.pictograph.grid_mode}_hand_point{point_suffix}"

        logger.debug(f"Attempting to place prop '{prop}' at point '{point_name}'.")

        grid_point = (
            self.pictograph.grid.grid_data.all_hand_points_strict.get(point_name)
            if strict
            else self.pictograph.grid.grid_data.all_hand_points_normal.get(point_name)
        )

        if grid_point and grid_point.coordinates:
            logger.debug(
                f"Found coordinates for '{point_name}': {grid_point.coordinates}."
            )
            self.place_prop_at_hand_point(prop, grid_point.coordinates)
        else:
            logger.warning(
                f"Hand point '{point_name}' not found or has no coordinates."
            )

    def place_prop_at_hand_point(self, prop: Prop, hand_point: QPointF) -> None:
        """
        Align the prop's center to the hand point using the 'centerPoint' defined in the SVG.
        """
        center_point_in_svg = self.get_svg_center_point(prop)
        center_point_in_scene = prop.mapToScene(center_point_in_svg)
        offset = hand_point - center_point_in_scene
        new_position = prop.pos() + offset
        prop.setPos(new_position)

    def _get_grid_mode_from_prop_loc(self, prop: "Prop") -> str:
        if prop.loc in ["ne", "nw", "se", "sw"]:
            grid_mode = "box"
        elif prop.loc in ["n", "s", "e", "w"]:
            grid_mode = "diamond"
        return grid_mode

    def get_svg_center_point(self, prop: Prop) -> QPointF:
        """
        Retrieve the 'centerPoint' from the SVG.
        """
        element_bounding_box = prop.renderer.boundsOnElement("centerPoint")
        center_point_in_svg = element_bounding_box.center()

        return center_point_in_svg

    def get_location_points(self, strict: bool) -> dict[str, "GridPoint"]:
        """
        Returns hand location points, depending on whether the props should be strictly placed.
        """
        location_points = (
            self.pictograph.grid.grid_data.all_hand_points_strict
            if strict
            else self.pictograph.grid.grid_data.all_hand_points_normal
        )
        return location_points
