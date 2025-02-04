from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton

from .layout_warning_dialog import LayoutWarningDialog
from .layout_options_beat_frame import LayoutOptionsBeatFrame
from .layout_options_panel import LayoutOptionsPanel


if TYPE_CHECKING:
    from ..sequence_widget import SequenceWorkbench


class LayoutOptionsDialog(QDialog):
    """The dialog allows the user to select the number of beats and the layout configuration in the sequence widget."""

    def __init__(self, sequence_widget: "SequenceWorkbench"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.settings_manager = (
            self.sequence_widget.main_widget.main_window.settings_manager
        )
        initial_state = self.sequence_widget.beat_frame.get.current_beat_frame_state()
        self.setWindowTitle("Layout Options")
        self._set_size()
        self.beat_frame = LayoutOptionsBeatFrame(self)
        self.panel = LayoutOptionsPanel(self)
        self._setup_cancel_button()
        self._setup_apply_button()
        self._setup_action_button_layout()
        self._setup_main_layout()

        if initial_state:
            self.panel.initialize_from_state(initial_state)
        else:
            self.panel.load_settings()

    def _setup_cancel_button(self):
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)

    def _setup_apply_button(self):
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)

    def _setup_action_button_layout(self):
        self.action_button_layout = QHBoxLayout()
        self.action_button_layout.addStretch(1)
        self.action_button_layout.addWidget(self.cancel_button)
        self.action_button_layout.addWidget(self.apply_button)

    def _set_size(self):
        main_widget_size = self.sequence_widget.main_widget.size()
        self.setFixedSize(
            int(main_widget_size.width() // 3), int(main_widget_size.height() // 2)
        )

    def _setup_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.panel, 3)  # Panel for settings
        self.main_layout.addWidget(self.beat_frame, 9)  # Frame for preview
        self.main_layout.addLayout(self.action_button_layout, 1)

    def apply_settings(self):
        grow_sequence = self.panel.sequence_growth_checkbox.isChecked()
        num_filled_beats = (
            self.sequence_widget.beat_frame.get.next_available_beat() - 1 or 0
        )
        if grow_sequence:
            self.settings_manager.global_settings.set_grow_sequence(True)
            self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
                num_filled_beats + 1
            )
        else:
            self.settings_manager.global_settings.set_grow_sequence(False)
            num_beats = int(self.panel.beats_combo_box.currentText())
            selected_layout = self.panel.layout_combo_box.currentText()
            cols, rows = map(int, selected_layout.split(" x "))
            if num_beats < num_filled_beats:
                if self.open_warning_dialog():
                    self.sequence_widget.layout_manager.apply_layout_options(
                        rows, cols, num_beats
                    )
                    for i in range(num_beats, num_filled_beats):
                        self.sequence_widget.beat_frame.beat_views[i].setScene(
                            self.sequence_widget.beat_frame.beat_views[i].blank_beat
                        )
                    selected_beat = (
                        self.sequence_widget.beat_frame.selection_overlay.selected_beat
                    )
                    if selected_beat:
                        selected_beat_index = selected_beat.number - 1
                        if (
                            selected_beat_index is not None
                            and selected_beat_index >= num_beats
                        ):
                            self.sequence_widget.beat_frame.selection_overlay.select_beat(
                                self.sequence_widget.beat_frame.beat_views[
                                    num_beats - 1
                                ]
                            )
                else:
                    return
            else:
                self.sequence_widget.layout_manager.apply_layout_options(
                    cols, rows, num_beats
                )
        self.accept()

    def open_warning_dialog(self):
        dialog = LayoutWarningDialog(self)
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted
