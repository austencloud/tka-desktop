from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from main_window.main_widget.sequence_widget.beat_frame.beat_deleter.beat_deleter import (
    BeatDeleter,
)


from .sequence_color_swapper import SequenceColorSwapper
from .sequence_reflector import SequenceReflector
from .sequence_rotater import SequenceRotater
from .sequence_widget_layout_manager import SequenceWorkbenchLayoutManager
from .sequence_auto_completer.sequence_auto_completer import SequenceAutoCompleter
from .beat_frame.sequence_widget_beat_frame import SequenceWorkbenchBeatFrame
from .add_to_dictionary_manager.add_to_dictionary_manager import AddToDictionaryManager
from .labels.current_word_label import CurrentWordLabel
from .labels.difficulty_label import DifficultyLabel
from .graph_editor.graph_editor import GraphEditor
from .sequence_widget_indicator_label import SequenceWorkbenchIndicatorLabel
from .sequence_widget_button_panel import SequenceWorkbenchButtonPanel
from .sequence_widget_scroll_area import SequenceWorkbenchScrollArea

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceWorkbench(QWidget):
    beat_frame_layout: QHBoxLayout
    indicator_label_layout: QHBoxLayout

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget

        # Managers
        self.add_to_dictionary_manager = AddToDictionaryManager(self)
        self.autocompleter = SequenceAutoCompleter(self)

        # Modification Managers
        self.mirror_manager = SequenceReflector(self)
        self.color_swap_manager = SequenceColorSwapper(self)
        self.rotation_manager = SequenceRotater(self)

        # Labels
        self.indicator_label = SequenceWorkbenchIndicatorLabel(self)
        self.current_word_label = CurrentWordLabel(self)
        self.difficulty_label = DifficultyLabel(self)

        # Sections
        self.scroll_area = SequenceWorkbenchScrollArea(self)
        self.beat_frame = SequenceWorkbenchBeatFrame(self)
        self.button_panel = SequenceWorkbenchButtonPanel(self)
        self.graph_editor = GraphEditor(self)

        # Layout
        self.layout_manager = SequenceWorkbenchLayoutManager(self)
        self.beat_deleter = BeatDeleter(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.graph_editor.toggle_tab.reposition_toggle_tab()
