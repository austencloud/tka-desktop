from typing import TYPE_CHECKING
import cv2
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QApplication,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap, QFont

from utils.path_helpers import get_my_videos_path

if TYPE_CHECKING:
    from main_window.main_widget.sequence_recorder.SR_capture_frame import (
        SR_CaptureFrame,
    )


class SR_VideoDisplayFrame(QFrame):
    init_webcam_requested = pyqtSignal()

    def __init__(self, capture_frame: "SR_CaptureFrame") -> None:
        super().__init__()
        self.capture_frame = capture_frame
        self.sequence_recorder = capture_frame.sequence_recorder

        self.capture = None
        self.recording = False
        self.recording_frames = []
        self.video_writer = None
        self.init_ui()
        self.init_webcam_requested.connect(self.init_webcam)

    def request_init_webcam(self):
        """Emit signal to initialize webcam in a thread-safe manner."""
        self.init_webcam_requested.emit()

    def init_ui(self) -> None:
        self.video_display = QLabel("Webcam Feed")
        self.video_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_display.setFont(QFont("Georgia", 12))
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_display)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def init_webcam(self) -> None:
        available_cameras = self.find_available_cameras()
        if available_cameras:
            self.capture = cv2.VideoCapture(available_cameras[0], cv2.CAP_MSMF)
            if not self.capture.isOpened():
                QMessageBox.warning(
                    self, "Webcam Error", "Unable to access the webcam."
                )
                return
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.video_frame_rate = self.capture.get(cv2.CAP_PROP_FPS)

            # self.video_timer = QTimer(self)
            # self.video_timer.timeout.connect(self.update_video_feed)
            self.update_timer_interval()
        print("Webcam initialized successfully.")

    def find_available_cameras(self) -> list[int]:
        available_cameras = []
        for i in range(1):  # Check first 5 indices.
            cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras

    def update_timer_interval(self) -> None:
        interval = int(1000 / self.video_frame_rate)
        self.video_timer.start(interval)

    def update_video_feed(self) -> None:
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, 1)
            if self.recording:
                self.recording_frames.append(frame)
            self.display_frame(frame)

    def display_frame(self, frame) -> None:
        h, w, _ = frame.shape
        startx = w // 2 - h // 2
        cropped_frame = frame[:, startx : startx + h]
        rgb_image = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
        convert_to_Qt_format = QImage(rgb_image.data, h, h, QImage.Format.Format_RGB888)
        p = QPixmap.fromImage(convert_to_Qt_format)
        self.video_display.setPixmap(
            p.scaled(self.video_display.size(), Qt.AspectRatioMode.KeepAspectRatio)
        )

    def start_recording(self) -> None:
        self.recording = not self.recording
        if self.recording:
            self.recording_frames = []
            QApplication.processEvents()  # Update UI
        else:
            self.stop_recording()

    def stop_recording(self) -> str:
        self.setStyleSheet("")
        return self.save_video_display_recording()

    def save_video_display_recording(self) -> str:
        output_path = get_my_videos_path("video_display_capture.avi")
        if self.recording_frames:
            height, width, _ = self.recording_frames[0].shape

            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(
                output_path, fourcc, self.video_frame_rate, (width, height)
            )
            for frame in self.recording_frames:
                out.write(frame)  # Write at original (maximum) resolution
            out.release()
            print("Video display recording saved successfully." + output_path)

        self.recording_frames = []  # Clear the frames after saving
        return output_path

    def closeEvent(self, event) -> None:
        if self.capture is not None:
            self.capture.release()

    def resize_video_display_frame(self) -> None:
        if not hasattr(self, "beat_frame"):
            self.beat_frame = self.capture_frame.SR_beat_frame

        height = self.beat_frame.height()
        self.setFixedHeight(height)
        self.video_display.setFixedHeight(height)
