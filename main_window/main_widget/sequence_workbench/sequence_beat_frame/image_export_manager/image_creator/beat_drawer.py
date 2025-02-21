from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QImage, QPixmap
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_workbench.sequence_beat_frame.beat_view import (
    BeatView,
)


if TYPE_CHECKING:
    from ..image_creator.image_creator import ImageCreator


class BeatDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator
        self.beat_frame = image_creator.export_manager.beat_frame

    def draw_beats(
        self,
        image: QImage,
        filled_beats: list["BeatView"],
        column_count: int,
        row_count: int,
        include_start_pos: bool,
        additional_height_top: int,
        add_beat_numbers: bool,
    ) -> None:

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

        if include_start_pos:
            start_pos_pixmap = self._grab_pixmap(
                self.beat_frame.start_pos_view, beat_size, beat_size
            )
            painter.drawPixmap(0, additional_height_top, start_pos_pixmap)
            start_col = 1
        else:
            start_col = 0

        for row in range(row_count + 1):
            for col in range(start_col, column_count):
                if beat_number < len(filled_beats):
                    beat_view = filled_beats[beat_number]

                    beat_pixmap = self._grab_pixmap(beat_view, beat_size, beat_size)
                    target_x = col * beat_size
                    target_y = row * beat_size + additional_height_top
                    painter.drawPixmap(target_x, target_y, beat_pixmap)
                    beat_number += 1

        painter.end()

    def _grab_pixmap(self, view: "BeatView", width: int, height: int) -> QPixmap:
        return view.beat.grabber.grab().scaled(
            width,
            height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
