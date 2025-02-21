import json
from typing import TYPE_CHECKING
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtWidgets import QGraphicsTextItem
from data.prop_class_mapping import prop_class_mapping
from .glyphs.reversal_glyph import (
    ReversalGlyph,
)
from objects.arrow.arrow import Arrow
from .grid.grid import Grid, GridData
from objects.motion.motion import Motion
from objects.prop.prop import Prop
from objects.prop.prop_classes import *
from data.constants import *
from settings_provider import SettingsProvider
from utilities.path_helpers import get_images_and_data_path
from .prop_factory import PropFactory
from .glyphs.elemental_glyph.elemental_glyph import ElementalGlyph
from .glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import StartToEndPosGlyph
from .glyphs.tka_glyph.tka_glyph import TKA_Glyph
from .glyphs.vtg_glyph.vtg_glyph import VTG_Glyph

if TYPE_CHECKING:
    from .pictograph_scene import PictographScene


# pictograph_initializer.py

import json
from utilities.path_helpers import get_images_and_data_path
from .grid.grid import Grid, GridData
import logging

logger = logging.getLogger(__name__)


class PictographInitializer:
    default_grid_mode = DIAMOND

    def __init__(self, pictograph: "PictographScene") -> None:
        self.pictograph = pictograph
        self.settings = SettingsProvider.get_settings()
        self.pictograph.setSceneRect(0, 0, 950, 950)
        self.pictograph.setBackgroundBrush(Qt.GlobalColor.white)
        self.prop_factory = PropFactory()
        self.grid_initialized = False
        self.init_all_components()

    ### INIT ###

    def init_all_components(self) -> None:
        self.pictograph.elements.grid = self.init_grid(self.default_grid_mode)
        self.pictograph.elements.locations = self.init_quadrant_boundaries(
            self.pictograph.elements.grid
        )
        self.pictograph.elements.motions = self.init_motions()
        self.pictograph.elements.arrows = self.init_arrows()
        self.pictograph.elements.props = self.init_props()
        self.pictograph.elements.tka_glyph = self.init_tka_glyph()
        self.pictograph.elements.vtg_glyph = self.init_vtg_glyph()
        self.pictograph.elements.elemental_glyph = self.init_elemental_glyph()
        self.pictograph.elements.start_to_end_pos_glyph = (
            self.init_start_to_end_pos_glyph()
        )
        self.init_reversal_symbols()

        self.set_nonradial_points_visibility(
            self.settings.value("global/show_non_radial_points", False)
        )

    def init_reversal_symbols(self) -> tuple[QGraphicsTextItem, QGraphicsTextItem]:
        self.reversal_symbol_manager = ReversalGlyph(self.pictograph)
        # self.reversal_symbol_manager.update_reversal_symbols()

    def set_nonradial_points_visibility(self, visible: bool) -> None:
        self.pictograph.elements.grid.toggle_non_radial_points(visible)

    def init_grid(self, grid_mode: str) -> Grid:
        if not self.grid_initialized:
            try:
                json_path = get_images_and_data_path("data/circle_coords.json")
                with open(json_path, "r") as file:
                    data = json.load(file)

                # Create GridData instance
                grid_data = GridData(data)

                # Initialize Grid with GridData and grid_mode
                grid = Grid(self.pictograph, grid_data, grid_mode)
                self.grid_initialized = True
                return grid
            except FileNotFoundError:
                logger.error(f"Grid data file '{json_path}' not found.")
                raise
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from '{json_path}': {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error initializing grid: {e}")
                raise
        else:
            logger.warning("Grid already initialized.")
            return self.pictograph.elements.grid

    def init_motions(self) -> dict[str, Motion]:
        motions: dict[str, Motion] = {}
        for color in [RED, BLUE]:
            motions[color] = self._create_motion(color)
        self.pictograph.elements.red_motion, self.pictograph.elements.blue_motion = (
            motions[RED],
            motions[BLUE],
        )
        for motion in motions.values():
            motion.start_ori = None
            motion.end_ori = None
        return motions

    def init_arrows(self) -> dict[str, Arrow]:
        arrows = {}
        for color in [BLUE, RED]:
            arrows[color] = self._create_arrow(color)
        self.pictograph.elements.red_arrow, self.pictograph.elements.blue_arrow = (
            arrows[RED],
            arrows[BLUE],
        )
        return arrows

    def init_props(self) -> dict[str, Prop]:
        props: dict[str, Prop] = {}
        prop_type = self.settings.value("global/prop_type", "Staff")
        for color in [RED, BLUE]:
            initial_prop_attributes = {
                COLOR: color,
                PROP_TYPE: prop_type,
                LOC: None,
                ORI: None,
            }
            initial_prop_class = prop_class_mapping.get(prop_type)
            if initial_prop_class is None:
                raise ValueError(f"Invalid prop_type: {prop_type}")
            initial_prop = Prop(
                self.pictograph, initial_prop_attributes, None, initial_prop_class
            )
            props[color] = self.prop_factory.create_prop_of_type(
                initial_prop, prop_type
            )
            self.pictograph.elements.motions[color].prop = props[color]
            props[color].motion = self.pictograph.elements.motions[color]

            props[color].arrow = self.pictograph.elements.motions[color].arrow
            self.pictograph.elements.motions[color].arrow.motion.prop = props[color]
            self.pictograph.addItem(props[color])
            props[color].hide()

        self.pictograph.elements.red_prop, self.pictograph.elements.blue_prop = (
            props[RED],
            props[BLUE],
        )
        return props

    def init_tka_glyph(self) -> TKA_Glyph:
        tka_glyph = TKA_Glyph(self.pictograph)
        self.pictograph.addItem(tka_glyph)
        return tka_glyph

    def init_vtg_glyph(self) -> VTG_Glyph:
        vtg_glyph = VTG_Glyph(self.pictograph)
        return vtg_glyph

    def init_elemental_glyph(self) -> ElementalGlyph:
        elemental_glyph = ElementalGlyph(self.pictograph)
        return elemental_glyph

    def init_start_to_end_pos_glyph(self) -> StartToEndPosGlyph:
        start_to_end_glyph = StartToEndPosGlyph(self.pictograph)

        return start_to_end_glyph

    def init_quadrant_boundaries(
        self, grid: Grid
    ) -> dict[str, tuple[int, int, int, int]]:
        grid_center: QPoint = grid.center.toPoint()

        grid_center_x = grid_center.x()
        grid_center_y = grid_center.y()

        ne_boundary = (
            grid_center_x,
            0,
            self.pictograph.width(),
            grid_center_y,
        )
        se_boundary = (
            grid_center_x,
            grid_center_y,
            self.pictograph.width(),
            self.pictograph.height(),
        )
        sw_boundary = (0, grid_center_y, grid_center_x, self.pictograph.height())
        nw_boundary = (
            0,
            0,
            grid_center_x,
            grid_center_y,
        )
        locations = {
            NORTHEAST: ne_boundary,
            SOUTHEAST: se_boundary,
            SOUTHWEST: sw_boundary,
            NORTHWEST: nw_boundary,
        }
        return locations

    ### CREATE ###

    def _create_arrow(self, color: str) -> Arrow:
        arrow_attributes = {
            COLOR: color,
            TURNS: 0,
        }
        arrow = Arrow(self.pictograph, arrow_attributes)
        self.pictograph.elements.motions[color].arrow = arrow
        arrow.motion = self.pictograph.elements.motions[color]
        self.pictograph.addItem(arrow)
        arrow.hide()
        return arrow

    def _create_motion(self, color: str) -> Motion:
        motion_data = {
            COLOR: color,
            ARROW: None,
            PROP: None,
            MOTION_TYPE: None,
            PROP_ROT_DIR: None,
            TURNS: 0,
            START_LOC: None,
            END_LOC: None,
            START_ORI: None,
        }
        return Motion(self.pictograph, motion_data)
