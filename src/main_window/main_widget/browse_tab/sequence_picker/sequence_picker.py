from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from .filter_stack.sequence_picker_filter_stack import SequencePickerFilterStack
from .sequence_picker_section_manager import SequencePickerSectionManager
from .sequence_picker_sorter import SequencePickerSorter
from .control_panel.sequence_picker_control_panel import SequencePickerControlPanel
from .sequence_picker_progress_bar import SequencePickerProgressBar
from .nav_sidebar.sequence_picker_nav_sidebar import SequencePickerNavSidebar
from .sequence_picker_scroll_widget import SequencePickerScrollWidget

if TYPE_CHECKING:
    from ..browse_tab import BrowseTab


class SequencePicker(QWidget):
    initialized = False

    def __init__(self, browse_tab: "BrowseTab"):
        super().__init__(browse_tab)
        self.browse_tab = browse_tab
        self.main_widget = browse_tab.main_widget
        self.sections: dict[str, list[tuple[str, list[str]]]] = {}
        self.currently_displayed_sequences = []
        self.selected_sequence_dict = None
        self._setup_components()
        self._setup_layout()

    def _setup_components(self):

        # Widgets
        self.filter_stack = SequencePickerFilterStack(self)
        self.control_panel = SequencePickerControlPanel(self)
        self.progress_bar = SequencePickerProgressBar(self)
        self.scroll_widget = SequencePickerScrollWidget(self)
        self.nav_sidebar = SequencePickerNavSidebar(self)

        # Managers
        self.sorter = SequencePickerSorter(self)
        self.section_manager = SequencePickerSectionManager(self)

    def _setup_layout(self):
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.nav_sidebar)
        content_layout.addWidget(self.scroll_widget)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addLayout(content_layout)

        self.setLayout(self.main_layout)

