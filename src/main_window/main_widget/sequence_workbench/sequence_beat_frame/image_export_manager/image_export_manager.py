from datetime import datetime
from typing import TYPE_CHECKING
from settings_manager.global_settings.app_context import AppContext
from .image_export_layout_handler import ImageExportLayoutHandler
from .image_creator.image_creator import ImageCreator
from .image_export_beat_factory import ImageExportBeatFactory
from .image_saver import ImageSaver


if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )
    from base_widgets.base_beat_frame import BaseBeatFrame


from typing import TYPE_CHECKING


class ImageExportManager:
    last_save_directory = None
    include_start_pos: bool

    def __init__(
        self,
        beat_frame: "SequenceBeatFrame",
        beat_frame_class: type,
    ) -> None:
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget
        self.settings_manager = AppContext.settings_manager()

        if beat_frame_class.__name__ == "SequenceWorkbenchBeatFrame":
            self.sequence_workbench = beat_frame.sequence_workbench
        elif beat_frame_class.__name__ == "TempBeatFrame":
            self.dictionary_widget = beat_frame.browse_tab
        # Get the include_start_position setting from image export settings
        self.include_start_pos = (
            AppContext.settings_manager().image_export.get_image_export_setting(
                "include_start_position"
            )
        )
        # Initialize components
        self.layout_handler = ImageExportLayoutHandler(self)
        self.beat_factory = ImageExportBeatFactory(self, beat_frame_class)
        self.image_creator = ImageCreator(self)
        self.image_saver = ImageSaver(self)

    def export_image_directly(self, sequence=None):
        """Immediately exports the image using current settings and opens the save dialog."""
        sequence = (
            sequence
            or self.main_widget.json_manager.loader_saver.load_current_sequence()
        )

        # Check if the sequence is empty (no beats and no start position)
        include_start_pos = self.settings_manager.image_export.get_image_export_setting(
            "include_start_position"
        )

        # Check if the sequence has any beats (excluding the start position)
        has_beats = len(sequence) >= 3

        if not has_beats and not include_start_pos:
            # If there's no start position to show, inform the user and return
            self.main_widget.sequence_workbench.indicator_label.show_message(
                "The sequence is empty and 'Show Start Position' is disabled."
            )
            return
        elif not has_beats and include_start_pos:
            # If there's only a start position and it's enabled, we'll export just that
            self.main_widget.sequence_workbench.indicator_label.show_message(
                "Exporting only the start position."
            )

        # Retrieve the export settings
        settings_manager = self.main_widget.settings_manager
        options = settings_manager.image_export.get_all_image_export_options()

        options["user_name"] = settings_manager.users.get_current_user()
        options["export_date"] = datetime.now().strftime("%m-%d-%Y")

        # Generate the image
        image_creator = self.image_creator
        sequence_image = image_creator.create_sequence_image(
            sequence, options, dictionary=False, fullscreen_preview=False
        )

        # Save the image
        self.image_saver.save_image(sequence_image)
        # open the folder containing the image

        self.main_widget.sequence_workbench.indicator_label.show_message(
            "Image saved successfully!"
        )
