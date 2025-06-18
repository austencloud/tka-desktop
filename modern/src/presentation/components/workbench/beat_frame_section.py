from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

from .button_panel import ModernSequenceWorkbenchButtonPanel
from domain.models.core_models import SequenceData, BeatData
from core.interfaces.core_services import ILayoutService
from .sequence_beat_frame.sequence_beat_frame import SequenceBeatFrame

if TYPE_CHECKING:
    pass


class WorkbenchBeatFrameSection(QWidget):
    """Beat frame section component combining beat frame and button panel"""

    # Signals for parent workbench
    beat_selected = pyqtSignal(int)
    beat_modified = pyqtSignal(int, object)
    sequence_modified = pyqtSignal(object)  # SequenceData object
    layout_changed = pyqtSignal(int, int)

    # Button panel signals
    add_to_dictionary_requested = pyqtSignal()
    save_image_requested = pyqtSignal()
    view_fullscreen_requested = pyqtSignal()
    mirror_sequence_requested = pyqtSignal()
    swap_colors_requested = pyqtSignal()
    rotate_sequence_requested = pyqtSignal()
    copy_json_requested = pyqtSignal()
    delete_beat_requested = pyqtSignal()
    clear_sequence_requested = pyqtSignal()

    def __init__(
        self, layout_service: ILayoutService, parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._layout_service = layout_service
        self._current_sequence: Optional[SequenceData] = None
        self._start_position_data: Optional[BeatData] = None

        # Components
        self._beat_frame: Optional[SequenceBeatFrame] = None
        self._button_panel: Optional[ModernSequenceWorkbenchButtonPanel] = None

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Setup beat frame + button panel layout matching Legacy's structure"""
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create beat frame (left side)
        self._beat_frame = SequenceBeatFrame(
            layout_service=self._layout_service, parent=self
        )
        self._beat_frame.setMinimumHeight(400)

        # Create button panel (right side)
        self._button_panel = ModernSequenceWorkbenchButtonPanel(self)

        # Add with proper proportions (10:1 ratio like Legacy)
        layout.addWidget(self._beat_frame, 10)
        layout.addWidget(self._button_panel, 1)

    def _connect_signals(self):
        """Connect internal component signals"""
        if self._beat_frame:
            self._beat_frame.beat_selected.connect(self.beat_selected)
            self._beat_frame.beat_modified.connect(self.beat_modified)
            self._beat_frame.sequence_modified.connect(self.sequence_modified)
            self._beat_frame.layout_changed.connect(self.layout_changed)

        if self._button_panel:
            # Dictionary & Export operations
            self._button_panel.add_to_dictionary_requested.connect(
                self.add_to_dictionary_requested
            )
            self._button_panel.save_image_requested.connect(self.save_image_requested)
            self._button_panel.view_fullscreen_requested.connect(
                self.view_fullscreen_requested
            )

            # Transform operations
            self._button_panel.mirror_sequence_requested.connect(
                self.mirror_sequence_requested
            )
            self._button_panel.swap_colors_requested.connect(self.swap_colors_requested)
            self._button_panel.rotate_sequence_requested.connect(
                self.rotate_sequence_requested
            )

            # Sequence management operations
            self._button_panel.copy_json_requested.connect(self.copy_json_requested)
            self._button_panel.delete_beat_requested.connect(self.delete_beat_requested)
            self._button_panel.clear_sequence_requested.connect(
                self.clear_sequence_requested
            )

    def set_sequence(self, sequence: Optional[SequenceData]):
        """Set the current sequence"""
        self._current_sequence = sequence
        if self._beat_frame:
            self._beat_frame.set_sequence(sequence)
        self._update_button_states()

    def set_start_position(self, start_position_data: BeatData):
        """Set the start position"""
        self._start_position_data = start_position_data
        if self._beat_frame:
            self._beat_frame.set_start_position(start_position_data)

    def get_selected_beat_index(self) -> Optional[int]:
        """Get selected beat index from beat frame"""
        return self._beat_frame.get_selected_beat_index() if self._beat_frame else None

    def set_button_enabled(self, button_name: str, enabled: bool):
        """Enable/disable specific button"""
        if self._button_panel:
            self._button_panel.set_button_enabled(button_name, enabled)

    def show_button_message(self, button_name: str, message: str, duration: int = 2000):
        """Show message tooltip on button"""
        if self._button_panel:
            self._button_panel.show_message_tooltip(button_name, message, duration)

    def _update_button_states(self):
        """Update button enabled states based on current sequence"""
        if not self._button_panel:
            return

        has_sequence = (
            self._current_sequence is not None and self._current_sequence.length > 0
        )

        # Buttons that require a sequence
        sequence_dependent_buttons = [
            "save_image",
            "mirror_sequence",
            "swap_colors",
            "rotate_sequence",
            "copy_json",
            "add_to_dictionary",
        ]

        for button_name in sequence_dependent_buttons:
            self._button_panel.set_button_enabled(button_name, has_sequence)

        # Clear button is always enabled
        self._button_panel.set_button_enabled("clear_sequence", True)

        # Delete beat requires selection
        # This will be updated when beat selection changes
        self._button_panel.set_button_enabled("delete_beat", False)

    def update_button_sizes(self, container_height: int):
        """Update button sizes for responsive design"""
        if self._button_panel:
            self._button_panel.update_button_sizes(container_height)
