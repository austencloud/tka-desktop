from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.settings_dialog.ui.beat_layout.layout_controls.layout_controls import (
    LayoutControls,
)


from .layout_beat_frame.layout_beat_frame import LayoutBeatFrame

if TYPE_CHECKING:
    from legacy.src.main_window.main_widget.settings_dialog.legacy_settings_dialog import (
        LegacySettingsDialog,
    )


class BeatLayoutTab(QWidget):
    def __init__(self, settings_dialog: "LegacySettingsDialog"):
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget

        # Get layout_settings from dependency injection system
        try:
            settings_manager = self.main_widget.app_context.settings_manager
            self.layout_settings = settings_manager.sequence_layout
        except AttributeError:
            # Fallback for cases where app_context is not available during initialization
            self.layout_settings = None
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                "settings_manager not available during BeatLayoutTab initialization"
            )

        self.beat_frame = LayoutBeatFrame(self)
        self.controls = LayoutControls(self)
        self._connect_signals()
        self._setup_layout()

    def showEvent(self, a0):
        self.num_beats = self.main_widget.sequence_workbench.beat_frame.get.beat_count()
        default_layout = self.layout_settings.get_layout_setting(str(self.num_beats))
        self.beat_frame.current_layout = tuple(default_layout)
        self.controls.length_selector.num_beats_spinbox.setValue(self.num_beats)

        self.beat_frame.update_preview()
        return super().showEvent(a0)

    def _connect_signals(self):
        self.controls.layout_selected.connect(self._on_layout_selected)
        self.controls.sequence_length_changed.connect(self.on_sequence_length_changed)

    def _setup_layout(self):
        """Set up the layout with modern glassmorphism styling."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Controls container with glassmorphism background
        controls_container = QWidget()
        controls_container.setObjectName("controls_container")
        controls_container.setStyleSheet(
            """
            QWidget#controls_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(31, 41, 59, 0.1),
                    stop:1 rgba(55, 65, 81, 0.08));
                border: 1px solid rgba(75, 85, 99, 0.3);
                border-radius: 12px;
                padding: 16px;
            }
            """
        )

        controls_layout = QVBoxLayout(controls_container)
        controls_layout.setContentsMargins(16, 16, 16, 16)
        controls_layout.addWidget(self.controls)

        layout.addWidget(controls_container)

        # Beat frame container with glassmorphism background
        beat_frame_container = QWidget()
        beat_frame_container.setObjectName("beat_frame_container")
        beat_frame_container.setStyleSheet(
            """
            QWidget#beat_frame_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(31, 41, 59, 0.05),
                    stop:1 rgba(55, 65, 81, 0.03));
                border: 1px solid rgba(75, 85, 99, 0.15);
                border-radius: 16px;
                padding: 20px;
            }
            """
        )

        beat_frame_layout = QVBoxLayout(beat_frame_container)
        beat_frame_layout.setContentsMargins(20, 20, 20, 20)
        beat_frame_layout.addWidget(self.beat_frame)

        layout.addWidget(beat_frame_container, stretch=1)
        self.setLayout(layout)

    def _on_layout_selected(self, layout_text: str):
        if layout_text:
            rows, cols = map(int, layout_text.split(" x "))
            self.beat_frame.current_layout = (rows, cols)
            self.beat_frame.update_preview()

        # self.controls.default_layout_label.update_text(layout_text)

    def on_sequence_length_changed(self, new_length: int):
        self.controls = self.controls
        self.layout_dropdown = self.controls.layout_selector.layout_dropdown
        self.num_beats = new_length
        self.layout_dropdown.clear()
        layout_selector = self.controls.layout_selector
        layout_selector._update_valid_layouts(new_length)
        self.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in layout_selector.valid_layouts]
        )
        self.controls.layout_tab.beat_frame.current_layout = (
            self.layout_settings.get_layout_setting(str(self.num_beats))
        )
        layout_text = (
            f"{self.controls.layout_tab.beat_frame.current_layout[0]} x "
            f"{self.controls.layout_tab.beat_frame.current_layout[1]}"
        )
        self.layout_dropdown.setCurrentText(layout_text)

        self.controls.beat_frame.update_preview()
        self.controls.default_layout_label.setText(f"Default: {layout_text}")

    def update_beat_layout_tab(self):
        beat_count = (
            self.settings_dialog.main_widget.sequence_workbench.beat_frame.get.beat_count()
        )
        self.controls.layout_selector._update_valid_layouts(beat_count)
        self.controls.length_selector.num_beats_spinbox.setValue(beat_count)
