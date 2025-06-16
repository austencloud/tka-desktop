import os
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QUrl, QTimer
from typing import TYPE_CHECKING, Optional
from base_widgets.pictograph.elements.views.beat_view import (
    LegacyBeatView,
)
from data.constants import GOLD
from utils.path_helpers import get_data_path
from PyQt6.QtMultimedia import QAudioOutput, QSoundEffect


if TYPE_CHECKING:
    from main_window.main_widget.sequence_recorder.SR_beat_frame import SR_BeatFrame


class SR_BeatSelectionManager(QWidget):
    def __init__(self, beat_frame: "SR_BeatFrame") -> None:
        super().__init__(beat_frame)
        self.beat_frame = beat_frame
        self.selected_beat: Optional[LegacyBeatView] = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_selection)
        self.current_index = 0
        self.audio_output = QAudioOutput()  # Create an audio output
        self.audio_output.setVolume(1.0)  # Set volume to 100%
        self.border_color = QColor(GOLD)
        self.border_width = 6
        path = get_data_path("audio/metronomes/")
        self.metronome_sounds = {
            "quartz": QSoundEffect(),
            "block": QSoundEffect(),
            "clap": QSoundEffect(),
        }
        for sound_name, sound_effect in self.metronome_sounds.items():
            file_path = os.path.abspath(f"{path}{sound_name}.wav")
            sound_effect.setSource(QUrl.fromLocalFile(file_path))
            sound_effect.setVolume(1.0)

        self.selected_metronome_sound = self.metronome_sounds["quartz"]

    def reset_selection(self) -> None:
        self.current_index = -1
        self.deselect_beat()
        self.move_selection()

    def handle_media_error(self, _error) -> None:
        pass

    def set_bpm(self, bpm) -> None:
        milliseconds_per_beat = 60000 / bpm
        self.timer.start(int(milliseconds_per_beat))

    def move_selection(self) -> None:
        self.selected_metronome_sound.play()

        # Deselect the previous beat
        if self.selected_beat:
            self.deselect_beat()

        next_index = (
            self.current_index + 1
            if self.current_index + 1 < len(self.beat_frame.beat_views)
            else 0
        )
        next_beat = self.beat_frame.beat_views[next_index]

        # Check if the next beat has something. If not, or if we're at the last beat, reset to the first beat with content
        if not next_beat.scene() or next_index == 0:
            for i, beat in enumerate(self.beat_frame.beat_views):
                if beat.scene():
                    self.current_index = i
                    break
        else:
            self.current_index = next_index

        # Now select the beat at current_index

        current_beat = self.beat_frame.beat_views[self.current_index]
        if current_beat.scene():
            self.select_beat(current_beat)

    def set_metronome_sound(self, sound_name) -> None:
        if sound_name in self.metronome_sounds:
            self.selected_metronome_sound = self.metronome_sounds[sound_name]
        else:
            print("Selected metronome sound does not exist, retaining previous choice.")

    def get_current_bpm(self) -> Optional[int]:
        if self.timer.isActive():
            return 60000 / self.timer.interval()
        else:
            return None

    # def select_beat(self, beat_view: BeatView) -> None:
    #     if self.selected_beat == beat_view:
    #         return
    #     else:
    #         if self.selected_beat:
    #             self.selected_beat.deselect()
    #         self.selected_beat = beat_view
    #         blue_turns = self.selected_beat.beat.blue_motion.state.turns
    #         red_turns = self.selected_beat.beat.red_motion.state.turns
    #         self.selected_beat.is_selected = True
    #         graph_editor = (
    #             self.selected_beat.beat_frame.main_widget.sequence_workbench.graph_editor
    #         )
    #         graph_editor.update_GE_pictograph(self.selected_beat.beat)

    #         graph_editor.adjustment_panel.update_turns_panel(blue_turns, red_turns)
    #         graph_editor.adjustment_panel.update_adjustment_panel()

    #         # Set the orientations in the graph editor's orientation changer
    #         if isinstance(beat_view, StartPositionBeatView):
    #             start_pos_pictograph = beat_view.beat
    #             blue_start_pos_ori_picker = (
    #                 graph_editor.adjustment_panel.blue_ori_picker
    #             )
    #             red_start_pos_ori_picker = graph_editor.adjustment_panel.red_ori_picker

    #             blue_start_pos_ori_picker.ori_picker_widget.ori_display_frame.set_initial_orientation(
    #                 start_pos_pictograph, BLUE
    #             )
    #             red_start_pos_ori_picker.ori_picker_widget.ori_display_frame.set_initial_orientation(
    #                 start_pos_pictograph, RED
    #             )

    #         self.update()
    #         self.update_overlay_position()
    #         self.show()

    # def deselect_beat(self) -> None:
    #     if self.selected_beat:
    #         self.selected_beat.deselect()
    #     self.selected_beat = None
    #     self.hide()

    def update_overlay_position(self) -> None:
        if self.selected_beat:
            self.setGeometry(self.selected_beat.geometry())
            self.raise_()
            self.update()

    def get_selected_beat(self) -> Optional[LegacyBeatView]:
        return self.selected_beat

    def start_selection_movement(self) -> None:
        # Assuming you've already set the BPM using set_bpm method
        # If not, you can set a default BPM here or ensure set_bpm is called before starting
        self.timer.start()

    def stop_selection_movement(self) -> None:
        self.timer.stop()
        # Optionally, you might want to deselect the current beat when stopping
        self.deselect_beat()

    def paintEvent(self, _event) -> None:
        if not self.selected_beat:
            return

        painter = QPainter(self)
        pen = QPen(self.border_color, self.border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        rect = self.rect().adjusted(
            self.border_width // 2,
            self.border_width // 2,
            -self.border_width // 2,
            -self.border_width // 2,
        )
        painter.drawRect(rect)
        painter.end()
