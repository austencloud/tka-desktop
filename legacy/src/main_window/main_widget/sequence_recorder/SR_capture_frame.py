from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy, QFrame, QApplication
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_recorder.SR_beat_frame import SR_BeatFrame
from main_window.main_widget.sequence_recorder.SR_video_combiner import SR_VideoCombiner
from main_window.main_widget.sequence_recorder.SR_video_display_frame import (
    SR_VideoDisplayFrame,
)
from utils.path_helpers import get_my_videos_path


if TYPE_CHECKING:
    from main_window.main_widget.sequence_recorder.sequence_recorder import (
        SequenceRecorder,
    )

from moviepy.editor import concatenate_videoclips, VideoFileClip


class SR_CaptureFrame(QFrame):
    def __init__(self, sequence_recorder: "SequenceRecorder") -> None:
        super().__init__()
        self.main_widget = sequence_recorder.main_widget
        self.sequence_recorder = sequence_recorder
        self.SR_beat_frame = SR_BeatFrame(self)
        self.video_display_frame = SR_VideoDisplayFrame(self)
        self.recording = False
        self.setObjectName("SR_CaptureFrame")
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.SR_beat_frame, 1)
        self.layout.addWidget(self.video_display_frame, 1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    def start_recording(self) -> None:
        self.recording = True
        self.SR_beat_frame.start_recording()
        self.video_display_frame.start_recording()
        self.setStyleSheet("#SR_CaptureFrame { border: 3px solid red; }")

    def stop_recording(self) -> None:
        # Stop capturing and save videos to files
        self.recording = False
        self.beat_video_path = self.SR_beat_frame.stop_recording()
        self.video_feed_path = self.video_display_frame.stop_recording()
        self.output_path = get_my_videos_path("combined_video.mp4")
        QApplication.processEvents()

        # Remove recording feedback
        self.setStyleSheet("")

        video_combiner = SR_VideoCombiner(
            self.beat_video_path, self.video_feed_path, self.output_path
        )

        video_combiner.combine_videos()

    def concatenate_videos(self, video_path_1, video_path_2):
        if video_path_1 is None or video_path_2 is None:
            return

        if not (
            isinstance(video_path_1, str) and video_path_1.endswith(".avi")
        ) or not (isinstance(video_path_2, str) and video_path_2.endswith(".avi")):
            return

        try:
            clip1 = VideoFileClip(video_path_1)
            clip2 = VideoFileClip(video_path_2)
            final_clip = concatenate_videoclips([clip1, clip2], method="compose")
            final_clip.write_videofile("combined_video.mp4")
        except Exception:
            pass

    def resize_capture_frame(self) -> None:
        size = int(self.sequence_recorder.height() * 0.8)
        self.SR_beat_frame.setFixedSize(size, size)
        self.SR_beat_frame.resize_beat_frame()
        self.video_display_frame.resize_video_display_frame()
        self.setFixedSize(size * 2, size)
