from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QGridLayout, QFrame, QApplication
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QPixmap, QImage
import cv2
import numpy as np
from data.constants import (
    BLUE_ATTRS,
    END_ORI,
    END_POS,
    RED_ATTRS,
    SEQUENCE_START_POSITION,
    START_ORI,
    START_POS,
)
from main_window.main_widget.sequence_recorder.SR_beat_selection_manager import (
    SR_BeatSelectionManager,
)
from main_window.main_widget.sequence_workbench.legacy_beat_frame.beat import (
    Beat,
    LegacyBeatView,
)
from utils.path_helpers import get_my_videos_path


from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


if TYPE_CHECKING:
    from main_window.main_widget.sequence_recorder.SR_capture_frame import (
        SR_CaptureFrame,
    )
    from main_window.main_widget.main_widget import MainWidget


class SR_BeatFrame(QFrame):
    COLUMN_COUNT = 4
    ROW_COUNT = 4

    def __init__(self, capture_frame: "SR_CaptureFrame") -> None:
        super().__init__()
        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.capture_frame_state)
        self.is_recording = False
        self.frame_captures = []  # Store QPixmap captures here
        self.capture_frame = capture_frame
        self.main_widget: "MainWidget" = capture_frame.main_widget
        self.json_manager = self.main_widget.json_manager
        self.pictograph_cache: dict[str, Beat] = {}
        self.beat_views: list[LegacyBeatView] = []

        self._setup_components()
        self._setup_layout()
        self._populate_beat_frame_with_views()

    def start_recording(self):
        self.frame_captures.clear()
        self.is_recording = True
        self.capture_timer.start(100)  # Adjust as needed for fps

    def capture_frame_state(self):
        if not self.is_recording:
            return
        pixmap = self.grab()  # Grab the current state of the widget
        self.frame_captures.append(pixmap)

    def _populate_beat_frame_with_views(self) -> None:
        for j in range(self.ROW_COUNT):
            for i in range(self.COLUMN_COUNT):
                self._add_beat_to_layout(j, i)

    def _setup_components(self) -> None:

        self.selection_manager = SR_BeatSelectionManager(self)

    def _setup_layout(self) -> None:
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter
        )

    def _add_beat_to_layout(self, row: int, col: int) -> None:
        beat_view = LegacyBeatView(self)
        self.layout.addWidget(beat_view, row, col)
        self.beat_views.append(beat_view)

    def add_scene_to_sequence(self, new_beat: "LegacyPictograph") -> None:
        next_beat_index = self.find_next_available_beat()
        if next_beat_index is not None:
            self.beat_views[next_beat_index].set_beat(new_beat, next_beat_index + 2)

    def find_next_available_beat(self) -> int:
        for i, beat in enumerate(self.beat_views):
            if beat.scene() is None or beat.scene().items() == []:
                return i
        return None

    def get_last_filled_beat(self) -> LegacyBeatView:
        for beat_view in reversed(self.beat_views):
            if beat_view.is_filled:
                return beat_view
        return self.beat_views[0]

    def propogate_turn_adjustment(self, current_sequence_json) -> None:
        for i, entry in enumerate(current_sequence_json):
            if i == 0:
                self.update_start_pos_from_current_sequence_json(entry)
            else:
                beat = self.beat_views[i - 1].beat
                if beat:
                    if beat.state.pictograph_data != entry:
                        beat.managers.updater.update_pictograph(entry)
                        QApplication.processEvents()

    def update_start_pos_from_current_sequence_json(self, entry: dict) -> None:
        entry[RED_ATTRS][START_ORI] = entry[RED_ATTRS][END_ORI]
        entry[BLUE_ATTRS][START_ORI] = entry[BLUE_ATTRS][END_ORI]
        entry[START_POS] = entry[END_POS]

    def get_index_of_currently_selected_beat(self) -> int:
        for i, beat in enumerate(self.beat_views):
            if beat.is_selected:
                return i
        return 0

    def clear_beat_frame(self) -> None:
        for beat_view in self.beat_views:
            beat_view.setScene(None)
            beat_view.is_filled = False

    def populate_beat_frame_scenes_from_json(self) -> None:
        sequence_json = self.json_manager.loader_saver.load_current_sequence()
        self.clear_beat_frame()
        for pictograph_data in sequence_json:
            if pictograph_data.get(SEQUENCE_START_POSITION) or pictograph_data.get(
                "prop_type"
            ):
                continue
            beat = Beat(self)
            beat.managers.updater.update_pictograph(pictograph_data)
            self.add_scene_to_sequence(beat)
            # pictograph_key = (
            #     beat.main_widget.pictograph_key_generator.generate_pictograph_key(
            #         pictograph_data
            #     )
            # )
            # self.pictograph_cache[pictograph_key] = beat

    @staticmethod
    def pixmap_to_cvimg(pixmap: QPixmap) -> np.ndarray:
        """Convert QPixmap to an OpenCV image format."""
        size = pixmap.size()
        channels_count = 4
        image = pixmap.toImage()
        image = image.convertToFormat(QImage.Format.Format_RGBA8888)
        ptr = image.bits()
        ptr.setsize(image.sizeInBytes())
        arr = np.array(ptr).reshape(size.height(), size.width(), channels_count)
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)

    def stop_recording(self) -> str:
        self.is_recording = False
        self.capture_timer.stop()
        return self.save_beat_frame_recording()

    def save_beat_frame_recording(self) -> str:
        if not self.frame_captures:
            print("No frames captured.")
            return
        output_path = get_my_videos_path("beat_frame_capture.avi")

        height, width = (
            self.frame_captures[0].size().height(),
            self.frame_captures[0].size().width(),
        )
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(output_path, fourcc, 10.0, (width, height))

        for pixmap in self.frame_captures:
            frame = self.pixmap_to_cvimg(pixmap)
            out.write(frame)

        out.release()
        print("Beat frame recording saved successfully." + output_path)
        return output_path

    def resize_beat_frame(self) -> None:
        beat_view_size = int(self.width() / (self.COLUMN_COUNT))
        for view in self.beat_views:
            view.setFixedSize(QSize(beat_view_size))
            view.resetTransform()
            if view.scene():
                view.fitInView(
                    view.scene().sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
                )
