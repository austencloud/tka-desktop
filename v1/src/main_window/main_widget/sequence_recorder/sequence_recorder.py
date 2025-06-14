from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .SR_capture_frame import SR_CaptureFrame
from .SR_main_control_frame import SR_MainControlFrame

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceRecorder(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.capture_frame = SR_CaptureFrame(self)
        self.video_control_frame = SR_MainControlFrame(self)
        self.initialized = False
        self._setup_layout()
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )
        self.gradient_shift = 0
        self.color_shift = 0
        self.background_manager = None

    def animate_background(self) -> None:
        self.gradient_shift += 0.05
        self.color_shift += 1
        if self.color_shift > 360:
            self.color_shift = 0
        self.update()


    def _setup_layout(self) -> None:
        capture_layout_hbox = QHBoxLayout()
        capture_layout_hbox.addWidget(self.capture_frame)

        video_control_hbox = QHBoxLayout()
        video_control_hbox.addWidget(self.video_control_frame)

        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self.main_layout.addLayout(capture_layout_hbox)
        self.main_layout.addLayout(video_control_hbox)
        self.main_layout.addStretch(1)

    def resize_sequence_recorder(self) -> None:
        self.capture_frame.resize_capture_frame()
        self.video_control_frame.resize_control_frame()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        if not self.initialized:
            self.setCursor(Qt.CursorShape.WaitCursor)
            self.resize_sequence_recorder()
            self.initialized = True
            self.setCursor(Qt.CursorShape.ArrowCursor)