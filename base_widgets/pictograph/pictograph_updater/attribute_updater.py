import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..pictograph import Pictograph

logger = logging.getLogger(__name__)


class AttributeUpdater:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def update(self, data: dict) -> None:
        """
        Loads attributes from the provided data into the pictograph state.
        """
        try:
            self.pictograph.managers.attr_manager.load_from_dict(data)
            logger.debug("Attributes successfully updated.")
        except Exception as e:
            logger.error(f"Error updating attributes: {e}", exc_info=True)
