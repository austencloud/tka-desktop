#!/usr/bin/env python3
"""
Pictograph System Test Application

This application demonstrates the new pictograph system working within
the v2 architecture. It shows multiple pictographs with different
configurations to validate the arrow positioning and rendering system.

DEMONSTRATES:
- Pictograph domain models working
- Pictograph service layer functionality
- Pictograph component rendering
- Integration with v2 dependency injection
- Multiple pictograph configurations
"""

import sys
from pathlib import Path
from typing import List

# Add the v2 architecture to path
v2_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_path))

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import v2 architecture components
from src.core.dependency_injection.simple_container import get_container
from src.core.interfaces.core_services import ILayoutService, ISettingsService
from src.application.services.pictograph_service import (
    IPictographService,
    PictographService,
)
from src.application.services.v1_data_service import IV1DataService, V1DataService
from src.presentation.components.pictograph_component import PictographComponent
from src.domain.models.pictograph_models import GridMode
from src.domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)


class SimpleLayoutService(ILayoutService):
    """Simple layout service for testing."""

    def __init__(self):
        from PyQt6.QtCore import QSize

        self._main_window_size = QSize(1400, 900)

    def get_main_window_size(self):
        return self._main_window_size

    def get_workbench_size(self):
        return self._main_window_size

    def get_picker_size(self):
        return self._main_window_size

    def get_layout_ratio(self):
        return (2, 1)

    def set_layout_ratio(self, ratio):
        pass

    def calculate_component_size(self, component_type, parent_size):
        return parent_size


class SimpleSettingsService(ISettingsService):
    """Simple settings service for testing."""

    def __init__(self):
        self._settings = {}
        self._current_tab = "sequence_builder"

    def get_setting(self, key: str, default=None):
        return self._settings.get(key, default)

    def set_setting(self, key: str, value):
        self._settings[key] = value

    def get_current_tab(self) -> str:
        return self._current_tab

    def set_current_tab(self, tab_name: str) -> None:
        self._current_tab = tab_name

    def get_export_settings(self):
        return {}

    def get_global_settings(self):
        return self._settings


class PictographTestWindow(QMainWindow):
    """Main test window for the pictograph system."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kinetic Constructor v2 - Pictograph System Test")
        self.setMinimumSize(1400, 900)

        # Setup dependency injection
        self.container = self._setup_dependencies()

        # Setup UI
        self._setup_ui()

        # Create test pictographs
        self._create_test_pictographs()

    def _setup_dependencies(self):
        """Setup dependency injection container."""
        container = get_container()

        # Register services
        container.register_singleton(ILayoutService, SimpleLayoutService)
        container.register_singleton(ISettingsService, SimpleSettingsService)
        container.register_singleton(IPictographService, PictographService)
        container.register_singleton(IV1DataService, V1DataService)

        print("✅ Dependencies configured for pictograph testing")
        return container

    def _setup_ui(self):
        """Setup the main UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Pictograph System Test - Multiple Configurations")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Info panel
        info_text = QLabel(
            "🎯 Testing pictograph rendering with different arrow and prop configurations\n"
            "✅ Clean v2 architecture with dependency injection\n"
            "✅ Immutable domain models\n"
            "✅ Separated business logic and UI"
        )
        info_text.setStyleSheet(
            """
            QLabel {
                background-color: #e8f5e8;
                border: 1px solid #4caf50;
                border-radius: 5px;
                padding: 10px;
                margin: 10px;
            }
        """
        )
        main_layout.addWidget(info_text)

        # Control buttons
        button_layout = QHBoxLayout()

        refresh_btn = QPushButton("Refresh Pictographs")
        refresh_btn.clicked.connect(self._refresh_pictographs)
        button_layout.addWidget(refresh_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self._clear_pictographs)
        button_layout.addWidget(clear_btn)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        # Scroll area for pictographs
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        self.pictograph_layout = QGridLayout(scroll_widget)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Store pictograph components
        self.pictograph_components: List[PictographComponent] = []

    def _create_test_pictographs(self):
        """Create test pictographs using ACTUAL v1 data from the CSV files."""
        # Get the v1 data service
        v1_data_service = self.container.resolve(IV1DataService)

        # Show dataset info
        dataset_info = v1_data_service.get_dataset_info()
        print(f"📊 V1 Dataset Info: {dataset_info}")

        # Generate test configurations using REAL v1 data
        test_configurations = []

        # Generate 6 random valid pictographs from the v1 dataset
        for i in range(6):
            try:
                v1_data = v1_data_service.get_random_valid_pictograph_data()

                # Convert v1 motion types to v2 enums
                blue_motion_type = self._convert_v1_motion_type(
                    v1_data["blue_motion"]["motion_type"]
                )
                red_motion_type = self._convert_v1_motion_type(
                    v1_data["red_motion"]["motion_type"]
                )

                # Convert v1 rotation directions to v2 enums
                blue_rot_dir = self._convert_v1_rotation_dir(
                    v1_data["blue_motion"]["prop_rot_dir"]
                )
                red_rot_dir = self._convert_v1_rotation_dir(
                    v1_data["red_motion"]["prop_rot_dir"]
                )

                # Convert v1 locations to v2 enums
                blue_start_loc = self._convert_v1_location(
                    v1_data["blue_motion"]["start_loc"]
                )
                blue_end_loc = self._convert_v1_location(
                    v1_data["blue_motion"]["end_loc"]
                )
                red_start_loc = self._convert_v1_location(
                    v1_data["red_motion"]["start_loc"]
                )
                red_end_loc = self._convert_v1_location(
                    v1_data["red_motion"]["end_loc"]
                )

                config = {
                    "name": f"V1 Data: {v1_data['letter']} ({v1_data['start_position']}→{v1_data['end_position']})",
                    "beat": BeatData(
                        letter=v1_data["letter"],
                        blue_motion=MotionData(
                            motion_type=blue_motion_type,
                            prop_rot_dir=blue_rot_dir,
                            start_loc=blue_start_loc,
                            end_loc=blue_end_loc,
                            turns=v1_data["blue_motion"]["turns"],
                            start_ori=v1_data["blue_motion"]["start_ori"],
                            end_ori=v1_data["blue_motion"]["end_ori"],
                        ),
                        red_motion=MotionData(
                            motion_type=red_motion_type,
                            prop_rot_dir=red_rot_dir,
                            start_loc=red_start_loc,
                            end_loc=red_end_loc,
                            turns=v1_data["red_motion"]["turns"],
                            start_ori=v1_data["red_motion"]["start_ori"],
                            end_ori=v1_data["red_motion"]["end_ori"],
                        ),
                    ),
                }
                test_configurations.append(config)

            except Exception as e:
                print(f"⚠️ Error generating v1 data for pictograph {i}: {e}")
                # Fallback to a simple static pictograph
                config = {
                    "name": f"Fallback Static {i}",
                    "beat": BeatData(
                        letter="α",
                        blue_motion=MotionData(
                            motion_type=MotionType.STATIC,
                            prop_rot_dir=RotationDirection.NO_ROTATION,
                            start_loc=Location.SOUTH,
                            end_loc=Location.SOUTH,
                            turns=0.0,
                            start_ori="in",
                            end_ori="in",
                        ),
                        red_motion=MotionData(
                            motion_type=MotionType.STATIC,
                            prop_rot_dir=RotationDirection.NO_ROTATION,
                            start_loc=Location.NORTH,
                            end_loc=Location.NORTH,
                            turns=0.0,
                            start_ori="in",
                            end_ori="in",
                        ),
                    ),
                }
                test_configurations.append(config)

        # Create pictograph components for each configuration
        for i, config in enumerate(test_configurations):
            row = i // 3
            col = i % 3

            # Create container widget
            container_widget = QWidget()
            container_layout = QVBoxLayout(container_widget)

            # Add label
            label = QLabel(config["name"])
            label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.addWidget(label)

            # Create pictograph component
            pictograph_component = PictographComponent(self.container)
            pictograph_component.initialize()

            # Update with beat data
            pictograph_component.update_from_beat(config["beat"])

            container_layout.addWidget(pictograph_component.widget)
            self.pictograph_layout.addWidget(container_widget, row, col)

            self.pictograph_components.append(pictograph_component)

        print(f"✅ Created {len(test_configurations)} test pictographs")

    def _refresh_pictographs(self):
        """Refresh all pictographs."""
        for component in self.pictograph_components:
            current_pictograph = component.get_current_pictograph()
            if current_pictograph:
                component.update_pictograph(current_pictograph)

        print("✅ Refreshed all pictographs")

    def _clear_pictographs(self):
        """Clear all pictographs."""
        for component in self.pictograph_components:
            component.clear_pictograph()

        print("✅ Cleared all pictographs")

    def _convert_v1_motion_type(self, v1_motion_type: str) -> MotionType:
        """Convert v1 motion type string to v2 enum."""
        mapping = {
            "static": MotionType.STATIC,
            "pro": MotionType.SHIFT,  # v1 "pro" maps to v2 "shift"
            "anti": MotionType.SHIFT,  # v1 "anti" maps to v2 "shift"
            "dash": MotionType.DASH,
            "float": MotionType.FLOAT,
        }
        return mapping.get(v1_motion_type.lower(), MotionType.STATIC)

    def _convert_v1_rotation_dir(self, v1_rot_dir: str) -> RotationDirection:
        """Convert v1 rotation direction string to v2 enum."""
        mapping = {
            "cw": RotationDirection.CLOCKWISE,
            "ccw": RotationDirection.COUNTER_CLOCKWISE,
            "no_rot": RotationDirection.NO_ROTATION,
        }
        return mapping.get(v1_rot_dir.lower(), RotationDirection.NO_ROTATION)

    def _convert_v1_location(self, v1_location: str) -> Location:
        """Convert v1 location string to v2 enum."""
        mapping = {
            "n": Location.NORTH,
            "e": Location.EAST,
            "s": Location.SOUTH,
            "w": Location.WEST,
            "ne": Location.NORTHEAST,
            "se": Location.SOUTHEAST,
            "sw": Location.SOUTHWEST,
            "nw": Location.NORTHWEST,
        }
        return mapping.get(v1_location.lower(), Location.NORTH)


def main():
    """Main entry point for the pictograph test application."""
    print("🚀 Starting Pictograph System Test")
    print("=" * 50)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Create and show test window
    window = PictographTestWindow()
    window.show()

    print("✅ Pictograph test application started!")
    print("📋 Features being tested:")
    print("   - Multiple pictograph configurations")
    print("   - Different motion types (Pro, Anti, Dash, Float, Static)")
    print("   - Arrow and prop positioning")
    print("   - Clean v2 architecture integration")
    print("   - Dependency injection throughout")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
