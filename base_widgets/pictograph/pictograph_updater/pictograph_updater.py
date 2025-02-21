import logging
from typing import TYPE_CHECKING

from data.constants import LEADING, TRAILING
from main_window.main_widget.grid_mode_checker import GridModeChecker
from .arrow_data_updater import ArrowDataUpdater
from .attribute_updater import AttributeUpdater
from .glyph_updater import GlyphUpdater
from .motion_data_updater import MotionDataUpdater
from .placement_updater import PlacementUpdater

if TYPE_CHECKING:
    from ..pictograph import Pictograph

logger = logging.getLogger(__name__)


class PictographUpdater:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.attr_updater = AttributeUpdater(pictograph)
        self.motion_updater = MotionDataUpdater(pictograph)
        self.arrow_updater = ArrowDataUpdater(pictograph)
        self.glyph_updater = GlyphUpdater(pictograph)
        self.placement_updater = PlacementUpdater(pictograph)

    def update_pictograph(self, pictograph_data: dict = None) -> None:
        try:
            if not self.pictograph.managers.get.is_initialized:
                self.pictograph.managers.get.initiallize_getter()
                logger.debug("Pictograph getters initialized.")
        except Exception as e:
            logger.error(f"Error during initialization: {e}", exc_info=True)
            return

        if pictograph_data:
            if pictograph_data.get("is_placeholder"):
                logger.debug("Placeholder data provided; update skipped.")
                return

            try:
                if self.pictograph.managers.check.is_pictograph_data_complete(
                    pictograph_data
                ):
                    self._apply_complete_update(pictograph_data)
                else:
                    self._apply_partial_update(pictograph_data)
            except Exception as e:
                logger.error(
                    f"Error applying attribute and motion updates: {e}", exc_info=True
                )

        try:
            self.glyph_updater.update()
            self.placement_updater.update()
        except Exception as e:
            logger.error(f"Error updating glyphs or layout: {e}", exc_info=True)

    def _apply_complete_update(self, pictograph_data: dict) -> None:
        try:
            self.pictograph.state.pictograph_data = pictograph_data
            self.pictograph.state.grid_mode = GridModeChecker.get_grid_mode(
                pictograph_data
            )
            self.pictograph.elements.grid.update_grid_mode()
            self._apply_attribute_and_motion_updates(pictograph_data)
            self.pictograph.elements.vtg_glyph.set_vtg_mode()
            self.pictograph.elements.elemental_glyph.set_elemental_glyph()
            self.pictograph.elements.start_to_end_pos_glyph.set_start_to_end_pos_glyph()
            logger.debug("Complete update applied.")
        except Exception as e:
            logger.error(f"Error in complete update: {e}", exc_info=True)

    def _apply_partial_update(self, data: dict) -> None:
        self._apply_attribute_and_motion_updates(data)

    def _apply_attribute_and_motion_updates(self, data: dict) -> None:
        try:
            self.attr_updater.update(data)
            self.motion_updater.update(data)
            self.arrow_updater.update(data)
            self._update_lead_states()
            self.pictograph.elements.tka_glyph.update_tka_glyph()
            self.pictograph.elements.elemental_glyph.update_elemental_glyph()
            self.pictograph.elements.reversal_glyph.update_reversal_symbols()
            logger.debug("Attribute and motion updates applied.")
        except Exception as e:
            logger.error(
                f"Error applying attribute and motion updates: {e}", exc_info=True
            )

    def _update_lead_states(self) -> None:
        try:
            if self.pictograph.state.letter.value in ["S", "T", "U", "V"]:
                self.pictograph.managers.get.leading_motion().lead_state = LEADING
                self.pictograph.managers.get.trailing_motion().lead_state = TRAILING
                logger.debug("Lead states set for letters S, T, U, V.")
            else:
                for motion in self.pictograph.elements.motions.values():
                    motion.lead_state = None
        except Exception as e:
            logger.error(f"Error updating lead states: {e}", exc_info=True)

    def update_dict_from_attributes(self) -> dict:
        """
        Synchronizes pictograph_data with current attributes and returns the updated dictionary.
        """
        try:
            data = self.pictograph.managers.get.pictograph_data()
            self.pictograph.state.pictograph_data = data
            return data
        except Exception as e:
            logger.error(
                f"Error updating dictionary from attributes: {e}", exc_info=True
            )
            return {}
