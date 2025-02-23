from typing import TYPE_CHECKING
from main_window.settings_manager.global_settings.app_context import AppContext
from PyQt6.QtWidgets import QFileDialog
from .image_export_layout_handler import ImageExportLayoutHandler
from .image_creator.image_creator import ImageCreator
from .image_export_beat_factory import ImageExportBeatFactory
from .image_export_dialog.image_export_dialog_executor import ImageExportDialogExecutor
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
        self.dialog_executor = ImageExportDialogExecutor(self)

# main_window/main_widget/sequence_workbench/sequence_beat_frame/image_export_manager.py
    def export_sequence_image(self):
        # Get all settings at once
        export_settings = self.main_widget.settings_manager.image_export.get_all_settings()
        
        # Create image with stored settings
        image = self.image_creator.create_sequence_image(
            AppContext.json_manager().loader_saver.load_current_sequence(),
            include_start_pos=export_settings["include_start_position"],
            options={
                "add_beat_numbers": export_settings["add_beat_numbers"],
                "add_reversal_symbols": export_settings["add_reversal_symbols"],
                "add_info": export_settings["add_info"],
                "add_word": export_settings["add_word"],
                "add_difficulty_level": export_settings["add_difficulty_level"]
            }
        )
        
        # Save and handle post-export actions
        file_path = self._get_save_path()
        if file_path:
            image.save(file_path)
            if export_settings["open_directory_on_export"]:
                self._open_export_directory(file_path)

    def _open_export_directory(self, file_path: str):
        import platform
        import subprocess
        if platform.system() == "Windows":
            subprocess.Popen(f'explorer /select,"{file_path}"')
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", "-R", file_path])
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", file_path])

    def _get_save_path(self):
        return QFileDialog.getSaveFileName(
            self.beat_frame,
            "Save Sequence Image",
            "",
            "PNG Images (*.png);;JPEG Images (*.jpg *.jpeg)"
        )[0]
