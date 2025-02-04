from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QSlider,
    QVBoxLayout,
    QFrame,
    QComboBox,
    QPushButton,
    QLabel,
    QHBoxLayout,
)


if TYPE_CHECKING:
    from main_window.main_widget.sequence_recorder.SR_main_control_frame import SR_MainControlFrame


class SR_BeatControlPanel(QFrame):
    def __init__(self, control_frame: "SR_MainControlFrame") -> None:
        super().__init__(control_frame)
        self.control_frame = control_frame
        self.sequence_recorder = self.control_frame.sequence_recorder
        self.capture_frame = self.sequence_recorder.capture_frame
        self.beat_frame = self.capture_frame.SR_beat_frame
        self.selection_manager = self.beat_frame.selection_manager
        self.init_ui()
        self.setObjectName("SR_BeatControlPanel")
        self.setStyleSheet("#SR_BeatControlPanel { border: 1px solid black; }")

    def init_ui(self) -> None:
        self._setup_bpm_slider()
        self._setup_metronome_sound_selector()
        self._setup_play_button()
        self._setup_bpm_display_and_controls()
        self._setup_layout()

    def _setup_play_button(self):
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.toggle_play)
        self.is_playing = False  # Track the play state

    def toggle_play(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_button.setText("Pause")

            # Check if a BPM has been explicitly set; if not, use the slider's value
            current_bpm = (
                self.selection_manager.get_current_bpm()
            )  # Assuming such a method exists
            if not current_bpm:
                # Default to the slider's value if no BPM is set
                current_bpm = self.bpm_slider.value()
                self.selection_manager.set_bpm(current_bpm)
                self.bpm_display.setText(f"BPM: {current_bpm}")

            # Reset the selection manager to the beginning of the array
            self.selection_manager.reset_selection()
            self.selection_manager.start_selection_movement()
        else:
            self.play_button.setText("Play")
            self.selection_manager.stop_selection_movement()

    def _setup_metronome_sound_selector(self):
        self.metronome_sound_selector = QComboBox()
        self.metronome_sound_selector.addItems(["quartz", "block", "clap"])
        self.metronome_sound_selector.currentTextChanged.connect(
            self.selection_manager.set_metronome_sound
        )

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.metronome_sound_selector)
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.bpm_slider)
        self.layout.addLayout(self.bpm_control_layout)

    def _setup_bpm_display_and_controls(self):
        self.bpm_display = QLabel("BPM: 60")  # Initial BPM display
        self.bpm_plus_button = QPushButton("+")
        self.bpm_minus_button = QPushButton("-")

        self.bpm_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Connect buttons to methods for incrementing/decrementing BPM
        self.bpm_plus_button.clicked.connect(lambda: self.change_bpm(1))
        self.bpm_minus_button.clicked.connect(lambda: self.change_bpm(-1))

        # Layout for BPM controls
        self.bpm_control_layout = QHBoxLayout()
        self.bpm_control_layout.addWidget(self.bpm_minus_button)
        self.bpm_control_layout.addWidget(self.bpm_display)
        self.bpm_control_layout.addWidget(self.bpm_plus_button)

    def change_bpm(self, increment):
        current_bpm = self.bpm_slider.value()
        new_bpm = current_bpm + increment
        if 60 <= new_bpm <= 180:
            self.bpm_slider.setValue(new_bpm)
            self.adjust_bpm(new_bpm)
        self.bpm_display.setText(f"BPM: {new_bpm}")

    def _setup_bpm_slider(self) -> None:
        self.bpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.bpm_slider.setMinimum(60)
        self.bpm_slider.setMaximum(180)
        self.bpm_slider.setValue(60)  # Set an initial value if needed
        self.bpm_slider.valueChanged.connect(self.adjust_bpm)

    def adjust_bpm(self, bpm):
        self.selection_manager.set_bpm(bpm)
        self.bpm_display.setText(f"BPM: {bpm}")

    def resize_beat_control_frame(self) -> None:
        width = self.beat_frame.width()
        height = width // 4
        self.setFixedWidth(width)
