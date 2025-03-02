from datetime import datetime
from typing import TYPE_CHECKING
from settings_manager.global_settings.app_context import AppContext
from .image_export_layout_handler import ImageExportLayoutHandler
from .image_creator.image_creator import ImageCreator
from .image_export_beat_factory import ImageExportBeatFactory
from .image_saver import ImageSaver


if TYPE_CHECKING:
    from base_widgets.base_beat_frame import BaseBeatFrame


from typing import TYPE_CHECKING


class ImageExportManager:
    last_save_directory = None
    include_start_pos: bool

    def __init__(
        self,
        beat_frame: "BaseBeatFrame",
        beat_frame_class: type,
    ) -> None:
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget
        self.settings_manager = AppContext.settings_manager()

        if beat_frame_class.__name__ == "SequenceWorkbenchBeatFrame":
            self.sequence_workbench = beat_frame.sequence_workbench
        elif beat_frame_class.__name__ == "TempBeatFrame":
            self.dictionary_widget = beat_frame.browse_tab
        self.include_start_pos = (
            AppContext.settings_manager().image_export.get_image_export_setting(
                "include_start_position"
            )
        )
        self.layout_handler = ImageExportLayoutHandler(self)
        self.beat_factory = ImageExportBeatFactory(self, beat_frame_class)
        self.image_creator = ImageCreator(self)
        self.image_saver = ImageSaver(self)

    def export_image_directly(self, sequence = None):
        """Immediately exports the image using current settings and opens the save dialog."""
        sequence = sequence or self.main_widget.json_manager.loader_saver.load_current_sequence()

        if len(sequence) < 3:
            self.main_widget.sequence_workbench.indicator_label.show_message(
                "The sequence is empty."
            )
            return

        # Retrieve the export settings
        settings_manager = self.main_widget.settings_manager
        options = settings_manager.image_export.get_all_image_export_options()

        options["user_name"] = settings_manager.users.get_current_user()
        options["notes"] = settings_manager.users.get_current_note()
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
