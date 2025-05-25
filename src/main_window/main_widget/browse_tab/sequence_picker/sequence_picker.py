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

        # Set size policy to respect the layout stretch ratios and prevent excessive expansion
        from PyQt6.QtWidgets import QSizePolicy

        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,  # Expanding allows growth but respects constraints
        )
        size_policy.setHorizontalStretch(
            2
        )  # This should match the stretch factor in TabManager
        self.setSizePolicy(size_policy)

        # TESTING: Temporarily disable width constraint to isolate window expansion issue
        # self._enforce_width_constraint()

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

    def _enforce_width_constraint(self):
        """Enforce the 2/3 width constraint for the sequence picker."""
        try:
            # Get the main widget's total width
            main_widget_width = self.main_widget.width()
            if main_widget_width > 0:
                # Calculate the maximum allowed width (2/3 of total + small tolerance)
                max_width = int(
                    main_widget_width * 2 / 3 + 20
                )  # Small tolerance for rounding
                self.setMaximumWidth(max_width)

                # CRITICAL: Also set size policy to prevent expansion
                from PyQt6.QtWidgets import QSizePolicy

                size_policy = self.sizePolicy()
                size_policy.setHorizontalPolicy(QSizePolicy.Policy.Maximum)
                size_policy.setHorizontalStretch(2)
                self.setSizePolicy(size_policy)
        except (AttributeError, TypeError):
            # If we can't get the width, don't set a constraint
            pass
