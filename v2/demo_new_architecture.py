#!/usr/bin/env python3
"""
CRITICAL: Complete Working Demo - IMPLEMENT SEVENTH

This demonstrates the entire new architecture working together.
Run this to see how the new system eliminates ALL technical debt.

DEMONSTRATES:
- Dependency injection replacing AppContext
- Modern components without global state access
- Service layer with clean business logic
- Immutable domain models
- No patches or workarounds needed

USAGE:
    python demo_new_architecture.py
"""

import sys
from pathlib import Path
from typing import Tuple

# Add the v2 src directory to path
v2_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src_path))

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

# Import the new architecture components
from src.core.dependency_injection.simple_container import (
    get_container,
    SimpleContainer,
)
from src.core.interfaces.core_services import (
    ILayoutService,
    ISettingsService,
    ISequenceDataService,
    IValidationService,
)
from src.domain.models.core_models import (
    SequenceData,
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from src.application.services.simple_sequence_service import (
    SequenceService,
    SimpleSequenceDataService,
    SimpleSettingsService,
    SimpleValidationService,
)
from src.presentation.components.option_picker import ModernOptionPicker


class SimpleLayoutService(ILayoutService):
    """Simple implementation of layout service."""

    def __init__(self):
        self._main_window_size = QSize(1200, 800)
        self._layout_ratio = (2, 1)  # workbench:picker

    def get_main_window_size(self) -> QSize:
        return self._main_window_size

    def get_workbench_size(self) -> QSize:
        total_width = self._main_window_size.width()
        workbench_width = int(
            total_width * self._layout_ratio[0] / sum(self._layout_ratio)
        )
        return QSize(workbench_width, self._main_window_size.height())

    def get_picker_size(self) -> QSize:
        total_width = self._main_window_size.width()
        picker_width = int(
            total_width * self._layout_ratio[1] / sum(self._layout_ratio)
        )
        return QSize(picker_width, self._main_window_size.height())

    def get_layout_ratio(self) -> Tuple[int, int]:
        return self._layout_ratio

    def set_layout_ratio(self, ratio: Tuple[int, int]) -> None:
        self._layout_ratio = ratio

    def calculate_component_size(
        self, component_type: str, parent_size: QSize
    ) -> QSize:
        return parent_size


class DemoMainWindow(QMainWindow):
    """
    Demo main window showing the new architecture.

    DEMONSTRATES: How to use the new architecture without any global state.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kinetic Constructor v2 - New Architecture Demo")
        self.setMinimumSize(1200, 800)

        # Setup dependency injection container
        self.container = self._setup_dependency_injection()

        # Setup UI
        self._setup_ui()

        # Initialize demo data
        self._setup_demo_data()

    def _setup_dependency_injection(self) -> SimpleContainer:
        """
        Setup dependency injection container.

        REPLACES: AppContext initialization and global state setup
        """
        container = get_container()

        # Register core services
        container.register_singleton(ILayoutService, SimpleLayoutService)
        container.register_singleton(ISettingsService, SimpleSettingsService)
        container.register_singleton(ISequenceDataService, SimpleSequenceDataService)
        container.register_singleton(IValidationService, SimpleValidationService)

        # Register application services
        container.register_singleton(SequenceService, SequenceService)

        print("✅ Dependency injection configured - NO AppContext needed!")
        return container

    def _setup_ui(self) -> None:
        """Setup the main UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Kinetic Constructor v2 - New Architecture Demo")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Info panel
        info_panel = self._create_info_panel()
        main_layout.addWidget(info_panel)

        # Main content area
        content_layout = QHBoxLayout()

        # Workbench area (simplified for demo)
        workbench_area = self._create_workbench_area()
        content_layout.addWidget(workbench_area, 2)  # 2/3 of space

        # Option picker area
        self.option_picker = ModernOptionPicker(self.container)
        self.option_picker.initialize()
        self.option_picker.option_selected.connect(self._handle_option_selected)
        content_layout.addWidget(self.option_picker.widget, 1)  # 1/3 of space

        main_layout.addLayout(content_layout)

        # Apply modern styling
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel {
                color: #212529;
            }
        """
        )

    def _create_info_panel(self) -> QWidget:
        """Create info panel showing architecture benefits."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        info_text = QLabel(
            """
🎉 NEW ARCHITECTURE BENEFITS:
✅ NO AppContext global state access
✅ NO main widget coupling (self.mw eliminated)
✅ NO layout patches needed (option_picker_layout_patch.py eliminated)
✅ NO mw_size_provider() functions
✅ Clean dependency injection throughout
✅ Immutable domain models
✅ Testable components
✅ Works standalone AND embedded
        """
        )
        info_text.setFont(QFont("Consolas", 10))
        info_text.setStyleSheet(
            """
            QLabel {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 5px;
                padding: 10px;
                color: #155724;
            }
        """
        )
        layout.addWidget(info_text)

        return panel

    def _create_workbench_area(self) -> QWidget:
        """Create simplified workbench area for demo."""
        workbench = QWidget()
        layout = QVBoxLayout(workbench)

        # Title
        title = QLabel("Sequence Workbench")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        # Current sequence display
        self.sequence_display = QLabel("No sequence loaded")
        self.sequence_display.setStyleSheet(
            """
            QLabel {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 20px;
                min-height: 200px;
            }
        """
        )
        layout.addWidget(self.sequence_display)

        # Control buttons
        button_layout = QHBoxLayout()

        new_sequence_btn = QPushButton("New Sequence")
        new_sequence_btn.clicked.connect(self._create_new_sequence)
        button_layout.addWidget(new_sequence_btn)

        load_demo_btn = QPushButton("Load Demo Sequence")
        load_demo_btn.clicked.connect(self._load_demo_sequence)
        button_layout.addWidget(load_demo_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        workbench.setStyleSheet(
            """
            QWidget {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
            }
        """
        )

        return workbench

    def _setup_demo_data(self) -> None:
        """Setup demo data to show the system working."""
        try:
            # Get sequence service through dependency injection
            sequence_service = self.container.resolve(SequenceService)

            # Create a demo sequence
            demo_sequence = sequence_service.create_new_sequence("Demo Sequence")

            # Add a demo beat
            demo_beat = BeatData(
                letter="A",
                duration=1.0,
                blue_motion=MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.EAST,
                    turns=1.0,
                ),
                red_motion=MotionData(
                    motion_type=MotionType.DASH,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.SOUTH,
                    end_loc=Location.WEST,
                    turns=0.5,
                ),
            )

            updated_sequence = sequence_service.add_beat_to_sequence(demo_beat)
            self._update_sequence_display(updated_sequence)

            print("✅ Demo data created using clean service layer!")

        except Exception as e:
            print(f"❌ Error setting up demo data: {e}")

    def _create_new_sequence(self) -> None:
        """Create a new sequence."""
        try:
            sequence_service = self.container.resolve(SequenceService)
            new_sequence = sequence_service.create_new_sequence("New Sequence")
            self._update_sequence_display(new_sequence)

            # Refresh option picker
            self.option_picker.refresh_options()

            print("✅ New sequence created!")

        except Exception as e:
            print(f"❌ Error creating new sequence: {e}")

    def _load_demo_sequence(self) -> None:
        """Load the demo sequence."""
        try:
            sequence_service = self.container.resolve(SequenceService)
            current_sequence = sequence_service.load_current_sequence()
            self._update_sequence_display(current_sequence)

            # Refresh option picker
            self.option_picker.refresh_options()

            print("✅ Demo sequence loaded!")

        except Exception as e:
            print(f"❌ Error loading demo sequence: {e}")

    def _update_sequence_display(self, sequence: SequenceData) -> None:
        """Update the sequence display."""
        display_text = f"""
Sequence: {sequence.name}
ID: {sequence.id}
Length: {sequence.length} beats
Total Duration: {sequence.total_duration}
Valid: {sequence.is_valid}

Beats:
"""

        for beat in sequence.beats:
            display_text += f"  Beat {beat.beat_number}: {beat.letter} (duration: {beat.duration})\n"

        if not sequence.beats:
            display_text += "  No beats yet - use the option picker to add beats!"

        self.sequence_display.setText(display_text)

    def _handle_option_selected(self, option_id: str) -> None:
        """Handle option selection from the option picker."""
        try:
            sequence_service = self.container.resolve(SequenceService)
            updated_sequence = sequence_service.load_current_sequence()
            self._update_sequence_display(updated_sequence)

            print(f"✅ Option selected: {option_id}")

        except Exception as e:
            print(f"❌ Error handling option selection: {e}")


def main():
    """
    Main entry point for the demo.

    DEMONSTRATES: Complete new architecture without any global state or patches.
    """
    print("🚀 Starting Kinetic Constructor v2 - New Architecture Demo")
    print("=" * 60)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Create main window with new architecture
    window = DemoMainWindow()
    window.show()

    print("✅ Demo started successfully!")
    print("📋 Try the following:")
    print("   - Click 'New Sequence' to create a sequence")
    print("   - Click options in the option picker to add beats")
    print("   - Notice NO global state access anywhere!")
    print("   - Notice NO layout patches needed!")
    print("   - Notice clean dependency injection throughout!")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
