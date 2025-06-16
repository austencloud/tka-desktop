from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QImage, QPixmap
from PyQt6.QtCore import Qt

from base_widgets.pictograph.elements.views.beat_view import (
    LegacyBeatView,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.image_export_manager.image_creator.combined_grid_handler import (
    CombinedGridHandler,
)


if TYPE_CHECKING:
    from ..image_creator.image_creator import ImageCreator


class BeatDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator
        self.beat_frame = image_creator.export_manager.beat_frame
        self.combined_grid_handler = CombinedGridHandler(image_creator)

    def draw_beats(
        self,
        image: QImage,
        filled_beats: list["LegacyBeatView"],
        column_count: int,  # Number of columns in the image layout
        row_count: int,  # Number of rows in the image layout
        include_start_pos: bool,
        additional_height_top: int,
        add_beat_numbers: bool,
    ) -> None:
        """
        Draw beats onto the image using the specified layout.

        Parameters:
            column_count: Number of columns in the image layout
            row_count: Number of rows in the image layout
        """

        for beat_view in filled_beats:
            if add_beat_numbers:
                beat_view.beat.beat_number_item.setVisible(True)
            else:
                beat_view.beat.beat_number_item.setVisible(False)

        beat_size = int(
            self.beat_frame.start_pos_view.beat.width() * self.image_creator.beat_scale
        )
        painter = QPainter(image)
        beat_number = 0

        # Check if combined grids option is enabled
        use_combined_grids = self.image_creator.export_manager.settings_manager.image_export.get_image_export_setting(
            "combined_grids"
        )

        if include_start_pos:
            start_pos_pixmap = self._grab_pixmap(
                self.beat_frame.start_pos_view, beat_size, beat_size, use_combined_grids
            )
            painter.drawPixmap(0, additional_height_top, start_pos_pixmap)
            start_col = 1
        else:
            start_col = 0

        for row in range(row_count + 1):
            for col in range(start_col, column_count):
                if beat_number < len(filled_beats):
                    beat_view = filled_beats[beat_number]

                    beat_pixmap = self._grab_pixmap(
                        beat_view, beat_size, beat_size, use_combined_grids
                    )
                    # Add border_width to position to account for the border
                    target_x = col * beat_size
                    target_y = row * beat_size + additional_height_top
                    painter.drawPixmap(target_x, target_y, beat_pixmap)
                    beat_number += 1

        painter.end()

    def _grab_pixmap(
        self,
        view: "LegacyBeatView",
        width: int,
        height: int,
        use_combined_grids: bool = False,
    ) -> QPixmap:
        if use_combined_grids:
            return self.combined_grid_handler.process_beat_for_combined_grids(
                view, width
            )
        else:
            return view.beat.grabber.grab().scaled(
                width,
                height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
