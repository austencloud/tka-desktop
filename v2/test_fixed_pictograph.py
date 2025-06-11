"""
Test the fixed pictograph system without v1 data service dependency.
This tests the core fixes: grid rendering, scaling, and aspect ratio.
"""

import sys
from pathlib import Path

# Add the v2 architecture to path
v2_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_path))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import v2 architecture components
from core.dependency_injection.simple_container import get_container
from core.interfaces.core_services import ILayoutService, ISettingsService
from application.services.pictograph_service import IPictographService, PictographService
from presentation.components.pictograph_component import PictographComponent
from domain.models.core_models import BeatData, MotionData, MotionType, RotationDirection, Location


class SimpleLayoutService(ILayoutService):
    def __init__(self):
        from PyQt6.QtCore import QSize
        self._main_window_size = QSize(800, 600)
    def get_main_window_size(self): return self._main_window_size
    def get_workbench_size(self): return self._main_window_size
    def get_picker_size(self): return self._main_window_size
    def get_layout_ratio(self): return (2, 1)
    def set_layout_ratio(self, ratio): pass
    def calculate_component_size(self, component_type, parent_size): return parent_size


class SimpleSettingsService(ISettingsService):
    def __init__(self):
        self._settings = {}
        self._current_tab = "sequence_builder"
    def get_setting(self, key: str, default=None): return self._settings.get(key, default)
    def set_setting(self, key: str, value): self._settings[key] = value
    def get_current_tab(self) -> str: return self._current_tab
    def set_current_tab(self, tab_name: str) -> None: self._current_tab = tab_name
    def get_export_settings(self): return {}
    def get_global_settings(self): return self._settings


class FixedPictographTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fixed Pictograph System Test")
        self.setMinimumSize(800, 600)
        
        # Setup dependency injection
        self.container = self._setup_dependencies()
        self._setup_ui()
        self._create_test_pictographs()

    def _setup_dependencies(self):
        container = get_container()
        container.register_singleton(ILayoutService, SimpleLayoutService)
        container.register_singleton(ISettingsService, SimpleSettingsService)
        container.register_singleton(IPictographService, PictographService)
        print("Dependencies configured")
        return container

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        title = QLabel("Fixed Pictograph System Test")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        info = QLabel("Testing: Grid rendering, Scaling fixes, Aspect ratio")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        # Create pictograph component
        self.pictograph_component = PictographComponent(self.container)
        self.pictograph_component.initialize()
        layout.addWidget(self.pictograph_component.widget)

    def _create_test_pictographs(self):
        # Create a simple valid test pictograph (no invalid B+pro combination)
        test_beat = BeatData(
            letter="A",  # A can have pro motions (valid)
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
        )
        
        self.pictograph_component.update_from_beat(test_beat)
        print("Test pictograph created with valid data")


def main():
    print("Starting Fixed Pictograph Test")
    app = QApplication(sys.argv)
    window = FixedPictographTestWindow()
    window.show()
    print("Test window opened - check for grid rendering and proper scaling")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
