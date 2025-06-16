import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...legacy_pictograph import LegacyPictograph

logger = logging.getLogger(__name__)


class GlyphUpdater:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph

    def update(self) -> None:
        """
        Updates all glyph elements in the pictograph.
        """
        try:
            self.pictograph.elements.tka_glyph.update_tka_glyph()
            self.pictograph.elements.elemental_glyph.update_elemental_glyph()
            self.pictograph.elements.reversal_glyph.update_reversal_symbols()
            logger.debug("Glyphs updated successfully.")
        except Exception as e:
            logger.error(f"Error updating glyphs: {e}", exc_info=True)
