# Example of how to use the refactored DictionaryService in SequenceWorkbench

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout

# Import the refactored DictionaryService and UI
from main_window.main_widget.sequence_workbench.add_to_dictionary_manager.dictionary_service import (
    DictionaryService,
)
from main_window.main_widget.sequence_workbench.add_to_dictionary_manager.add_to_dictionary_ui import (
    AddToDictionaryUI,
)

# Other imports remain the same
from main_window.main_widget.sequence_workbench.beat_deleter.beat_deleter import (
    BeatDeleter,
)
from main_window.main_widget.sequence_workbench.labels.workbench_difficulty_label import (
    WorkbenchDifficultyLabel,
)
from main_window.main_widget.sequence_workbench.labels.circular_sequence_indicator import (
    CircularSequenceIndicator,
)
from main_window.main_widget.sequence_workbench.labels.sequence_workbench_indicator_label import (
    SequenceWorkbenchIndicatorLabel,
)
from legacy.src.main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
    LegacyBeatFrame,
)
from .full_screen_viewer import FullScreenViewer
from .sequence_color_swapper import SequenceColorSwapper
from .sequence_reflector import SequenceReflector
from .sequence_rotater import SequenceRotater
from .sequence_workbench_layout_manager import SequenceWorkbenchLayoutManager
from .labels.current_word_label import CurrentWordLabel
from .graph_editor.legacy_graph_editor import LegacyGraphEditor
from .sequence_workbench_button_panel import SequenceWorkbenchButtonPanel
from .sequence_workbench_scroll_area import SequenceWorkbenchScrollArea

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceWorkbench(QWidget):
    beat_frame_layout: QHBoxLayout
    indicator_label_layout: QHBoxLayout
    difficulty_label: WorkbenchDifficultyLabel
    circular_indicator: CircularSequenceIndicator
    current_word_label: CurrentWordLabel

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_widget.splash_screen.updater.update_progress("SequenceWorkbench")
        self.setObjectName("SequenceWorkbench")

        # Initialize UI components
        self.scroll_area = SequenceWorkbenchScrollArea(self)
        self.beat_frame = LegacyBeatFrame(self)

        # Initialize the refactored DictionaryService with the beat_frame
        self.dictionary_service = DictionaryService(self.beat_frame)

        # Initialize the UI wrapper that uses the dictionary service
        self.add_to_dictionary_ui = AddToDictionaryUI(self)

        # Modification Managers
        self.mirror_manager = SequenceReflector(self)
        self.color_swap_manager = SequenceColorSwapper(self)
        self.rotation_manager = SequenceRotater(self)

        # Labels
        self.indicator_label = SequenceWorkbenchIndicatorLabel(self)
        self.current_word_label = CurrentWordLabel(self)
        self.difficulty_label = WorkbenchDifficultyLabel(self)
        self.circular_indicator = CircularSequenceIndicator(self)

        # Sections
        self.button_panel = SequenceWorkbenchButtonPanel(self)
        self.graph_editor = LegacyGraphEditor(self)

        # Full Screen Viewer
        self.full_screen_viewer = FullScreenViewer(self)

        # Layout
        self.layout_manager = SequenceWorkbenchLayoutManager(self)
        self.beat_deleter = BeatDeleter(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graph_editor.resizeEvent(event)
