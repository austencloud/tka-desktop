"""
Base class for the codex pictograph exporter.
"""

from typing import TYPE_CHECKING, Dict, Any, Optional
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage

from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from data.constants import RED, BLUE

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.ui.image_export.image_export_tab import (
        ImageExportTab,
    )


class BaseCodexExporter:
    """Base class for the codex pictograph exporter."""

    def __init__(self, image_export_tab: "ImageExportTab"):
        """Initialize the exporter.

        Args:
            image_export_tab: The parent image export tab
        """
        self.image_export_tab = image_export_tab
        self.main_widget = image_export_tab.main_widget

    def _create_pictograph_from_data(
        self, pictograph_data: Dict[str, Any], grid_mode: str
    ) -> LegacyPictograph:
        """Create a pictograph from the given data.

        Args:
            pictograph_data: The pictograph data
            grid_mode: The grid mode to use

        Returns:
            The created pictograph
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _create_pictograph_image(
        self, pictograph: LegacyPictograph, add_border: bool = False
    ) -> QImage:
        """Create a QImage from a pictograph.

        Args:
            pictograph: The pictograph to convert to an image
            add_border: Whether to add a border

        Returns:
            The created image
        """
        raise NotImplementedError("Subclasses must implement this method")

    def _get_export_directory(self) -> Optional[str]:
        """Ask the user for a directory to save the exported images.

        Returns:
            The selected directory, or None if the user canceled
        """
        directory = QFileDialog.getExistingDirectory(
            self.image_export_tab,
            "Select Directory to Save Pictographs",
            "",
            QFileDialog.Option.ShowDirsOnly,
        )
        return directory if directory else None

    def _apply_turns_to_pictograph(
        self,
        pictograph: LegacyPictograph,
        red_turns: float = 0.0,
        blue_turns: float = 0.0,
    ) -> None:
        """Apply the specified turns to a pictograph.

        Args:
            pictograph: The pictograph to update
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
        """
        # Get the motion objects
        blue_motion = pictograph.elements.motion_set.get(BLUE)
        red_motion = pictograph.elements.motion_set.get(RED)

        # Update the pictograph data directly
        pictograph_data = pictograph.state.pictograph_data.copy()

        # Update blue motion data
        if blue_motion and BLUE + "_attributes" in pictograph_data:
            # Only update the turns value, preserve everything else
            pictograph_data[BLUE + "_attributes"]["turns"] = blue_turns

        # Update red motion data
        if red_motion and RED + "_attributes" in pictograph_data:
            # Only update the turns value, preserve everything else
            pictograph_data[RED + "_attributes"]["turns"] = red_turns

        # Apply the updated data to the pictograph
        pictograph.managers.updater.update_pictograph(pictograph_data)

        # Also set turns directly on the motion objects for good measure
        if blue_motion:
            # Only update the turns value, preserve everything else
            blue_motion.state.turns = blue_turns

        if red_motion:
            # Only update the turns value, preserve everything else
            red_motion.state.turns = red_turns

        # Update the pictograph's turns tuple
        if hasattr(pictograph.managers, "get") and hasattr(
            pictograph.managers.get, "turns_tuple"
        ):
            try:
                # This will update the turns tuple based on the new turns
                pictograph.state.turns_tuple = pictograph.managers.get.turns_tuple()
            except Exception as e:
                print(f"Error updating turns tuple: {e}")

        # Make sure the arrows are updated to reflect the turns
        if hasattr(pictograph.elements, "arrows"):
            for _, arrow in pictograph.elements.arrows.items():
                arrow.setup_components()

        # Update the pictograph
        pictograph.update()
