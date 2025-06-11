#!/usr/bin/env python3
"""
Test script for V1-compatible pictograph rendering.

This script tests the fixed SimplePictographComponent to ensure:
1. V1 SVG assets are loaded correctly
2. Grid scaling is pixel-perfect (950x950 scene)
3. Props and arrows are sized correctly relative to grid
4. Diamond grid is used as specified
5. All elements maintain V1 proportions
"""

import sys
from pathlib import Path

# Add the v2 src directory to path
v2_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(v2_src_path))

# Add the project root to path for absolute imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.presentation.components.simple_pictograph_component import (
    SimplePictographComponent,
    get_v2_image_path,
)
from src.domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)
from src.application.services.pictograph_data_service import PictographDataService
import os


class PictographRenderingTestWindow(QMainWindow):
    """Test window for V1-compatible pictograph rendering."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("V1 Pictograph Rendering Test")
        self.setMinimumSize(1200, 800)
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
        self.data_service = PictographDataService()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title
        title = QLabel("Pictograph Rendering Test")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            color: #2c5aa0;
            padding: 15px;
            background: rgba(44, 90, 160, 0.1);
            border-radius: 8px;
            margin-bottom: 10px;
        """
        )
        main_layout.addWidget(title)

        # Info
        info = QLabel(
            "Testing V1-compatible pictograph rendering with random valid combinations"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet(
            """
            background: #e3f2fd;
            padding: 12px;
            border-radius: 6px;
            font-size: 13px;
            color: #1565c0;
            border: 1px solid #bbdefb;
        """
        )
        main_layout.addWidget(info)

        # Create test pictographs
        pictographs_layout = QHBoxLayout()
        pictographs_layout.setSpacing(20)

        try:
            print("\n🎯 GENERATING TEST PICTOGRAPHS:")
            print("=" * 50)

            for i in range(3):
                pictograph_data = self.data_service.get_random_valid_pictograph_data()
                print(f"\nPictograph {i+1}:")
                print(f"  Letter: {pictograph_data['letter']}")
                print(f"  Blue Motion: {pictograph_data['blue_motion']['motion_type']}")
                print(
                    f"  Blue Locations: {pictograph_data['blue_motion']['start_loc']} → {pictograph_data['blue_motion']['end_loc']}"
                )
                print(
                    f"  Blue Rotation: {pictograph_data['blue_motion']['prop_rot_dir']}"
                )
                print(f"  Red Motion: {pictograph_data['red_motion']['motion_type']}")
                print(
                    f"  Red Locations: {pictograph_data['red_motion']['start_loc']} → {pictograph_data['red_motion']['end_loc']}"
                )
                print(
                    f"  Red Rotation: {pictograph_data['red_motion']['prop_rot_dir']}"
                )
                print(f"  Grid Mode: {pictograph_data.get('grid_mode', 'diamond')}")
                print(f"  Timing: {pictograph_data.get('timing', 'together')}")

                beat_data = self._convert_to_beat_data(pictograph_data)

                container = self._create_pictograph_container(
                    f"Pictograph {i+1}",
                    f"Letter {beat_data.letter}",
                    beat_data,
                )
                pictographs_layout.addWidget(container)

            print("\n" + "=" * 50)

        except Exception as e:
            print(f"❌ Error generating pictographs: {e}")
            error_label = QLabel(f"Error generating pictographs: {e}")
            error_label.setStyleSheet("color: red; font-weight: bold;")
            pictographs_layout.addWidget(error_label)

        main_layout.addLayout(pictographs_layout)

        # Asset verification
        asset_status = self._verify_assets()
        status_label = QLabel(asset_status)
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet(
            """
            font-family: 'Consolas', monospace;
            font-size: 11px;
            padding: 15px;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            color: #495057;
            margin-top: 10px;
        """
        )
        main_layout.addWidget(status_label)

    def _convert_to_beat_data(self, pictograph_data: dict) -> BeatData:
        blue_motion_data = pictograph_data["blue_motion"]
        red_motion_data = pictograph_data["red_motion"]

        blue_motion = MotionData(
            motion_type=MotionType(blue_motion_data["motion_type"]),
            prop_rot_dir=RotationDirection(blue_motion_data["prop_rot_dir"]),
            start_loc=Location(blue_motion_data["start_loc"]),
            end_loc=Location(blue_motion_data["end_loc"]),
            turns=blue_motion_data.get("turns", 1.0),
        )

        red_motion = MotionData(
            motion_type=MotionType(red_motion_data["motion_type"]),
            prop_rot_dir=RotationDirection(red_motion_data["prop_rot_dir"]),
            start_loc=Location(red_motion_data["start_loc"]),
            end_loc=Location(red_motion_data["end_loc"]),
            turns=red_motion_data.get("turns", 1.0),
        )

        return BeatData(
            letter=pictograph_data["letter"],
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

    def _create_pictograph_container(
        self, title: str, subtitle: str, beat_data: BeatData
    ) -> QWidget:
        """Create a container with a pictograph and title."""
        container = QWidget()
        container.setFixedWidth(280)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c5aa0; margin-bottom: 5px;")
        layout.addWidget(title_label)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #6c757d; margin-bottom: 10px;")
        layout.addWidget(subtitle_label)

        # Pictograph component with fixed V1 rendering
        pictograph = SimplePictographComponent()
        pictograph.update_from_beat(beat_data)
        pictograph.setFixedSize(220, 220)

        pictograph_wrapper = QWidget()
        pictograph_wrapper.setFixedSize(240, 240)
        pictograph_wrapper.setStyleSheet(
            """
            background: white;
            border: 2px solid #dee2e6;
            border-radius: 8px;
        """
        )
        pictograph_layout = QVBoxLayout(pictograph_wrapper)
        pictograph_layout.setContentsMargins(10, 10, 10, 10)
        pictograph_layout.addWidget(pictograph)

        layout.addWidget(pictograph_wrapper, 0, Qt.AlignmentFlag.AlignCenter)

        # Beat info
        info_text = f"Beat {beat_data.letter}"
        if beat_data.blue_motion:
            info_text += f"\nBlue: {beat_data.blue_motion.motion_type.value}"
            info_text += f"\n{beat_data.blue_motion.start_loc.value} → {beat_data.blue_motion.end_loc.value}"
        if beat_data.red_motion:
            info_text += f"\nRed: {beat_data.red_motion.motion_type.value}"
            info_text += f"\n{beat_data.red_motion.start_loc.value} → {beat_data.red_motion.end_loc.value}"

        info_label = QLabel(info_text)
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet(
            """
            font-size: 10px;
            color: #6c757d;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 4px;
            line-height: 1.4;
        """
        )
        layout.addWidget(info_label)

        container.setStyleSheet(
            """
            QWidget {
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 10px;
                margin: 5px;
            }
        """
        )

        return container

    def _verify_assets(self) -> str:
        """Verify that V1 assets are accessible."""
        test_files = [
            "grid/diamond_grid.svg",
            "props/simple_staff.svg",
            "arrows/static/from_radial/static_1.0.svg",
            "arrows/pro/from_radial/pro_1.0.svg",
            "arrows/dash/from_radial/dash_1.0.svg",
        ]

        status_lines = ["Asset Verification Status:"]
        all_found = True

        for filename in test_files:
            path = get_v2_image_path(filename)
            exists = os.path.exists(path)
            status = "✓" if exists else "✗"
            status_lines.append(f"  {status} {filename}")
            if not exists:
                all_found = False

        if all_found:
            status_lines.append("\nAll assets found - rendering enabled")
        else:
            status_lines.append("\nSome assets missing - copy from v1/src/images/")

        return "\n".join(status_lines)


def main():
    """Main entry point for the V1 pictograph test."""
    print("🧪 Testing V1-Compatible Pictograph Rendering")
    print("=" * 50)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Create test window
    window = PictographRenderingTestWindow()
    window.show()

    print("✅ V1 Pictograph test window created!")
    print("📋 Verify the following:")
    print("   - Diamond grid is displayed (not box grid)")
    print("   - Grid fills the entire pictograph area")
    print("   - Props (staffs) are positioned at grid points")
    print("   - Arrows are properly sized relative to grid")
    print("   - All elements maintain square aspect ratio")
    print("   - Visual appearance matches V1 exactly")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
