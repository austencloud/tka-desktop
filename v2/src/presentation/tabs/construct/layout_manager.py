"""
ConstructTabLayoutManager

Handles UI layout setup, panel creation, and widget management for the construct tab.
Responsible for creating the main layout structure and organizing UI components.
"""

from typing import Optional, Callable
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QStackedWidget,
)
from PyQt6.QtCore import Qt

from core.dependency_injection.di_container import DIContainer
from presentation.factories.workbench_factory import create_modern_workbench
from presentation.components.option_picker.option_picker import OptionPicker


class ConstructTabLayoutManager:
    """
    Manages the UI layout and panel creation for the construct tab.
    
    Responsibilities:
    - Setting up the main horizontal layout (50/50 split)
    - Creating workbench panel (left side)
    - Creating picker panel with stacked widget (right side)
    - Managing progress callbacks during initialization
    """
    
    def __init__(
        self,
        container: DIContainer,
        progress_callback: Optional[Callable[[str, float], None]] = None
    ):
        self.container = container
        self.progress_callback = progress_callback
        
        # UI components that will be created
        self.workbench = None
        self.picker_stack = None
        self.start_position_picker = None
        self.option_picker = None
    
    def setup_ui(self, parent_widget: QWidget) -> None:
        """Setup the main UI layout with progress updates"""
        if self.progress_callback:
            self.progress_callback("Setting up construct tab layout...", 0.1)

        # Main horizontal layout: 50/50 split like Legacy
        main_layout = QHBoxLayout(parent_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(12, 12, 12, 12)

        if self.progress_callback:
            self.progress_callback("Creating sequence workbench panel...", 0.2)

        # Left panel: Sequence Workbench (50% width)
        workbench_panel = self._create_workbench_panel()
        main_layout.addWidget(workbench_panel, 1)  # Equal weight = 50%

        if self.progress_callback:
            self.progress_callback("Creating option picker panel...", 0.5)

        # Right panel: Option Picker (50% width)
        picker_panel = self._create_picker_panel_with_progress()
        main_layout.addWidget(picker_panel, 1)  # Equal weight = 50%

        if self.progress_callback:
            self.progress_callback("Construct tab layout complete!", 1.0)

    def _create_workbench_panel(self) -> QWidget:
        """Create the left panel containing sequence workbench"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Create modern workbench with integrated button panel
        self.workbench = create_modern_workbench(self.container, panel)
        layout.addWidget(self.workbench)

        return panel

    def _create_picker_panel_with_progress(self) -> QWidget:
        """Create the right panel containing start pos picker and option picker"""
        if self.progress_callback:
            self.progress_callback("Creating picker panel layout...", 0.6)

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Create stacked widget for picker views (like Legacy)
        self.picker_stack = QStackedWidget()

        if self.progress_callback:
            self.progress_callback("Initializing start position picker...", 0.7)

        # Index 0: Start Position Picker
        start_pos_widget = self._create_start_position_widget()
        self.picker_stack.addWidget(start_pos_widget)

        if self.progress_callback:
            self.progress_callback("Loading option picker dataset...", 0.8)

        # Index 1: Option Picker
        option_widget = self._create_option_picker_widget_with_progress()
        self.picker_stack.addWidget(option_widget)

        if self.progress_callback:
            self.progress_callback("Configuring picker transitions...", 0.9)

        # Start with start position picker visible
        self.picker_stack.setCurrentIndex(0)

        layout.addWidget(self.picker_stack)
        return panel

    def _create_start_position_widget(self) -> QWidget:
        """Create start position picker widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        from ...components.start_position_picker.start_position_picker import (
            StartPositionPicker,
        )

        self.start_position_picker = StartPositionPicker()
        layout.addWidget(self.start_position_picker)

        return widget

    def _create_option_picker_widget_with_progress(self) -> QWidget:
        """Create option picker widget with progress updates for the heavy initialization"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        try:
            # Create progress callback for ModernOptionPicker's internal initialization
            def option_picker_progress(step: str, progress: float):
                if self.progress_callback:
                    # Map option picker progress (0.0-1.0) to our remaining range
                    mapped_progress = 0.8 + (progress * 0.1)  # 0.8 to 0.9 range
                    self.progress_callback(f"Option picker: {step}", mapped_progress)

            self.option_picker = OptionPicker(
                self.container, progress_callback=option_picker_progress
            )
            self.option_picker.initialize()
            layout.addWidget(self.option_picker.widget)
        except RuntimeError as e:
            print(f"❌ Failed to create option picker: {e}")
            # Create fallback widget
            fallback_label = QLabel("Option picker unavailable")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            self.option_picker = None

        return widget
    
    def transition_to_option_picker(self):
        """Switch from start position picker to option picker"""
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(1)

    def transition_to_start_position_picker(self):
        """Switch back to start position picker"""
        if self.picker_stack:
            self.picker_stack.setCurrentIndex(0)
