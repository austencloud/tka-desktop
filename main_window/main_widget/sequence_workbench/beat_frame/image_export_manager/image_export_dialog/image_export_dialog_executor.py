import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from .image_export_dialog import ImageExportDialog

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.beat_frame.beat_view import (
        BeatView,
    )
    from ..image_export_manager import ImageExportManager


class ImageExportDialogExecutor:
    def __init__(self, export_manager: "ImageExportManager"):
        self.export_manager = export_manager
        self.beat_frame = export_manager.beat_frame

        self.settings_manager = export_manager.settings_manager
        self.layout_manager = export_manager.layout_handler
        self.image_creator = export_manager.image_creator
        self.image_saver = export_manager.image_saver

    def exec_dialog(self, sequence: list[dict]) -> None:
        """Execute the image export dialog and handle user options.

        This method loads the current sequence, processes the beats, and opens the image export dialog.
        If the user confirms the dialog, the image is created and saved based on the selected options.
        """

        self.indicator_label = (
            self.export_manager.main_widget.sequence_workbench.indicator_label
        )
        if len(sequence) < 3:
            self.indicator_label.show_message("The sequence is empty.")
            return
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        filled_beats = self.export_manager.beat_factory.process_sequence_to_beats(
            sequence
        )

        self._clear_beat_selection(filled_beats)

        dialog = ImageExportDialog(self.export_manager, sequence)
        QApplication.restoreOverrideCursor()
        if dialog.exec():
            options = dialog.get_export_options()
            self.export_manager.include_start_pos = options.get(
                "include_start_position", self.export_manager.include_start_pos
            )
            self.settings_manager.image_export.set_image_export_setting(
                "include_start_position", self.export_manager.include_start_pos
            )

            sequence_image = self.image_creator.create_sequence_image(
                sequence, self.export_manager.include_start_pos, options
            )
            file_name = self.image_saver.save_image(sequence_image)
            if file_name and options.get("open_directory", False):
                self._open_directory(file_name)
            print(
                "Image created with start position included:",
                self.export_manager.include_start_pos,
            )

    def _clear_beat_selection(self, filled_beats: list["BeatView"]):
        for beat in filled_beats:
            beat.scene().clearSelection()

    def _open_directory(self, file_path: str):
        directory = os.path.dirname(file_path)
        try:
            if os.name == "nt":  # Windows
                os.startfile(directory)
            elif os.name == "posix":  # macOS, Linux
                subprocess.run(
                    ["open" if sys.platform == "darwin" else "xdg-open", directory]
                )
        except Exception as e:
            self.indicator_label.show_message(f"Failed to open directory: {str(e)}")
