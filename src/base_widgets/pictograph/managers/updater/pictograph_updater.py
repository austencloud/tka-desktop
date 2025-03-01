import logging
from typing import TYPE_CHECKING

from data.constants import BLUE, LEADING, RED, TRAILING
from main_window.main_widget.grid_mode_checker import GridModeChecker
from settings_manager.global_settings.app_context import AppContext
from .arrow_data_updater import ArrowDataUpdater
from .glyph_updater import GlyphUpdater
from .motion_data_updater import MotionDataUpdater
from .placement_updater import PlacementUpdater

if TYPE_CHECKING:
    from ...pictograph import Pictograph

logger = logging.getLogger(__name__)


class PictographUpdater:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.motion_updater = MotionDataUpdater(pictograph)
        self.arrow_updater = ArrowDataUpdater(pictograph)
        self.glyph_updater = GlyphUpdater(pictograph)
        self.placement_updater = PlacementUpdater(pictograph)

    def update_pictograph(self, pictograph_data: dict = None) -> None:
        try:
            if not self.pictograph.managers.get.is_initialized:
                self.pictograph.managers.get.initiallize_getter()
        except Exception as e:
            logger.error(f"Error during initialization: {e}", exc_info=True)
            return

        try:
            self._apply_data_update(pictograph_data)
        except Exception as e:
            logger.error(f"Error applying data updates: {e}", exc_info=True)

        try:
            self.glyph_updater.update()
            self.placement_updater.update()
        except Exception as e:
            logger.error(f"Error updating glyphs or placements: {e}", exc_info=True)

    def _apply_data_update(self, pictograph_data: dict) -> None:
        if pictograph_data:
            self.pictograph.state.update_pictograph_state(pictograph_data)

        self.update_grid_mode_if_changed()

        self.motion_updater.update_motions(pictograph_data)
        self.arrow_updater.update_arrows(pictograph_data)

        self.pictograph.elements.grid.update_grid_mode()
        self.pictograph.elements.vtg_glyph.set_vtg_mode()
        self.pictograph.elements.elemental_glyph.set_elemental_glyph()
        self.pictograph.elements.start_to_end_pos_glyph.set_start_to_end_pos_glyph()

        self._update_lead_states()

        self.pictograph.elements.tka_glyph.update_tka_glyph()
        self.pictograph.elements.reversal_glyph.update_reversal_symbols()
        # if pictograph_data:
        #     for color in [RED, BLUE]:
        #         self.pictograph.elements.props[color].updater.update_prop(
        #             self.get_prop_data(pictograph_data, color)
        #         )

        logger.debug("Data update (partial or complete) applied successfully.")

    def get_prop_data(self, pictograph_data: dict, color: str) -> dict:
        motion = self.pictograph.managers.get.motion_by_color(color)
        return {
            "color": color,
            "loc": pictograph_data[f"{color}_attributes"]["end_loc"],
            "motion": motion,
            "prop_type": AppContext.settings_manager()
            .global_settings.get_prop_type()
            .name,
        }

    def update_grid_mode_if_changed(self):
        new_grid_mode = GridModeChecker.get_grid_mode(
            self.pictograph.state.pictograph_data
        )
        if new_grid_mode and new_grid_mode != self.pictograph.state.grid_mode:
            self.pictograph.state.grid_mode = new_grid_mode
            self.pictograph.elements.grid.update_grid_mode()

    def _update_lead_states(self) -> None:
        try:
            letter_obj = self.pictograph.state.letter
            if letter_obj and letter_obj.value in ["S", "T", "U", "V"]:
                self.pictograph.managers.get.leading_motion().state.lead_state = LEADING
                self.pictograph.managers.get.trailing_motion().state.lead_state = (
                    TRAILING
                )
                logger.debug("Lead states set for letters S, T, U, V.")
            else:
                for motion in self.pictograph.elements.motion_set.values():
                    motion.state.lead_state = None
        except Exception as e:
            logger.error(f"Error updating lead states: {e}", exc_info=True)

    def update_dict_from_attributes(self) -> dict:
        try:
            data = self.pictograph.managers.get.pictograph_data()
            self.pictograph.state.pictograph_data = data
            return data
        except Exception as e:
            logger.error(
                f"Error updating dictionary from attributes: {e}", exc_info=True
            )
            return {}
