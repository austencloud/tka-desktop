#!/usr/bin/env python3
"""
Debug Option Picker Fixes

This script tests both critical fixes:
1. Widget parenting and timing problems
2. Pictograph visual rendering accuracy
"""

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from src.core.dependency_injection.simple_container import SimpleContainer
from src.presentation.tabs.construct_tab_widget import ConstructTabWidget
from src.application.services.simple_layout_service import SimpleLayoutService
from src.core.interfaces.core_services import ILayoutService


class OptionPickerFixesDebugWindow(QMainWindow):
    """Debug window for option picker fixes"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔧 Option Picker Fixes Debug")
        self.setGeometry(100, 100, 1800, 1200)

        # Create container and register services
        self.container = SimpleContainer()
        self.container.register_singleton(ILayoutService, SimpleLayoutService)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Status label
        self.status_label = QLabel("🔄 Initializing option picker fixes debug...")
        self.status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Test buttons
        test_btn = QPushButton("🎯 Test Widget Parenting Fix")
        test_btn.clicked.connect(self.test_widget_parenting)
        layout.addWidget(test_btn)

        visual_btn = QPushButton("🎨 Test Visual Rendering Accuracy")
        visual_btn.clicked.connect(self.test_visual_rendering)
        layout.addWidget(visual_btn)

        # Create the construct tab widget
        self.construct_tab = ConstructTabWidget(self.container, parent=self)
        layout.addWidget(self.construct_tab)

        # Set up automatic test after initialization
        QTimer.singleShot(1000, self.run_automatic_tests)

    def run_automatic_tests(self):
        """Run automatic tests of both fixes"""
        print("🔧 Option Picker Fixes Debug Started")
        print("=" * 70)

        self.status_label.setText("🎯 Testing widget parenting fix...")

        # Trigger start position selection
        self.construct_tab._handle_start_position_selected("alpha1_alpha1")

        # Check results after a short delay
        QTimer.singleShot(1500, self.test_widget_parenting)
        QTimer.singleShot(2500, self.test_visual_rendering)

    def test_widget_parenting(self):
        """Test widget parenting fix"""
        print("\n🔧 TESTING WIDGET PARENTING FIX")
        print("-" * 50)

        option_picker = self.construct_tab.option_picker

        if not option_picker:
            print("❌ Option picker not found")
            return

        # Check sections container parenting
        sections_container = getattr(option_picker, "sections_container", None)
        if sections_container:
            print(f"✅ Sections container exists")
            print(f"   Parent: {sections_container.parent()}")
            print(f"   Visible: {sections_container.isVisible()}")
            print(
                f"   Size: {sections_container.size().width()}x{sections_container.size().height()}"
            )
        else:
            print("❌ Sections container not found")

        # Check individual sections
        sections = getattr(option_picker, "_sections", {})
        parenting_issues = 0

        for section_type, section in sections.items():
            parent = section.parent()
            if parent == sections_container:
                print(
                    f"✅ Section {section_type} properly parented to sections_container"
                )
            else:
                print(f"❌ Section {section_type} parent issue: {parent}")
                parenting_issues += 1

            # Check pictograph frames
            pictographs = getattr(section, "pictographs", [])
            for i, frame in enumerate(pictographs):
                frame_parent = frame.parent()
                expected_parent = section.pictograph_container
                if frame_parent == expected_parent:
                    print(f"   ✅ Frame {i} in {section_type} properly parented")
                else:
                    print(
                        f"   ❌ Frame {i} in {section_type} parent issue: {frame_parent} != {expected_parent}"
                    )
                    parenting_issues += 1

        if parenting_issues == 0:
            print(f"\n🎉 WIDGET PARENTING FIX SUCCESSFUL!")
            print(f"   ✅ All widgets properly parented - no popup windows")
            self.status_label.setText("✅ Widget parenting fix verified!")
        else:
            print(f"\n❌ WIDGET PARENTING ISSUES FOUND: {parenting_issues}")
            self.status_label.setText(f"❌ {parenting_issues} parenting issues found")

    def test_visual_rendering(self):
        """Test visual rendering accuracy"""
        print("\n🎨 TESTING VISUAL RENDERING ACCURACY")
        print("-" * 50)

        option_picker = self.construct_tab.option_picker

        if not option_picker:
            print("❌ Option picker not found")
            return

        beat_options = getattr(option_picker, "_beat_options", [])
        if len(beat_options) == 0:
            print("❌ No beat options to test")
            return

        # Test first pictograph frame
        sections = getattr(option_picker, "_sections", {})
        test_frame = None
        test_section = None

        for section_type, section in sections.items():
            pictographs = getattr(section, "pictographs", [])
            if len(pictographs) > 0:
                test_frame = pictographs[0]
                test_section = section_type
                break

        if not test_frame:
            print("❌ No pictograph frames found to test")
            return

        print(f"🔍 Testing frame from section {test_section}")

        # Check frame properties
        print(
            f"   Frame size: {test_frame.size().width()}x{test_frame.size().height()}"
        )
        print(f"   Frame visible: {test_frame.isVisible()}")

        # Check pictograph component
        if hasattr(test_frame, "pictograph_component"):
            comp = test_frame.pictograph_component
            print(f"   Component size: {comp.size().width()}x{comp.size().height()}")
            print(f"   Component visible: {comp.isVisible()}")

            # Check scene
            if hasattr(comp, "scene") and comp.scene:
                scene = comp.scene
                print(f"   Scene size: {scene.SCENE_SIZE}")
                print(f"   Scene items: {len(scene.items())}")

                # Check for specific V1 elements
                print(f"   Scene item types:")
                for i, item in enumerate(scene.items()):
                    item_type = str(type(item))
                    print(f"     {i}: {item_type}")

                grid_items = [
                    item for item in scene.items() if "grid" in str(type(item)).lower()
                ]
                prop_items = [
                    item
                    for item in scene.items()
                    if "prop" in str(type(item)).lower()
                    or "staff" in str(type(item)).lower()
                ]
                arrow_items = [
                    item for item in scene.items() if "arrow" in str(type(item)).lower()
                ]
                svg_items = [
                    item for item in scene.items() if "svg" in str(type(item)).lower()
                ]
                pixmap_items = [
                    item
                    for item in scene.items()
                    if "pixmap" in str(type(item)).lower()
                ]

                print(f"   Grid items: {len(grid_items)}")
                print(f"   Prop items: {len(prop_items)}")
                print(f"   Arrow items: {len(arrow_items)}")
                print(f"   SVG items: {len(svg_items)}")
                print(f"   Pixmap items: {len(pixmap_items)}")

                # Check if we have the expected V1 elements
                # V1 elements are rendered as SVG items, so check for sufficient SVG content
                has_sufficient_svg = (
                    len(svg_items) >= 8
                )  # Grid + props + arrows should be multiple SVGs
                has_text = (
                    len(
                        [
                            item
                            for item in scene.items()
                            if "text" in str(type(item)).lower()
                        ]
                    )
                    > 0
                )
                has_groups = (
                    len(
                        [
                            item
                            for item in scene.items()
                            if "group" in str(type(item)).lower()
                        ]
                    )
                    > 0
                )

                if has_sufficient_svg and has_text:
                    print(
                        f"   ✅ V1 elements present ({len(svg_items)} SVGs, text, groups)"
                    )
                    v1_elements_ok = True
                else:
                    print(
                        f"   ⚠️ Insufficient V1 elements - SVGs:{len(svg_items)}, text:{has_text}, groups:{has_groups}"
                    )
                    v1_elements_ok = False

                # Check view scaling
                if hasattr(comp, "view") and comp.view:
                    view = comp.view
                    transform = view.transform()
                    scale_x = transform.m11()
                    scale_y = transform.m22()
                    print(f"   View scale: {scale_x:.3f}x{scale_y:.3f}")

                    # Check if scaling maintains 1:1 aspect ratio
                    aspect_ratio_ok = abs(scale_x - scale_y) < 0.001
                    print(f"   Aspect ratio 1:1: {aspect_ratio_ok}")

                    if aspect_ratio_ok and v1_elements_ok:
                        print(f"\n🎉 VISUAL RENDERING ACCURACY VERIFIED!")
                        print(f"   ✅ V1 elements present with correct scaling")
                        self.status_label.setText(
                            "✅ Both fixes verified successfully!"
                        )
                    else:
                        print(f"\n⚠️ VISUAL RENDERING NEEDS ATTENTION")
                        print(f"   Some elements or scaling issues detected")
                        self.status_label.setText("⚠️ Visual rendering needs attention")
                else:
                    print(f"   ❌ No view found in pictograph component")
            else:
                print(f"   ❌ No scene found in pictograph component")
        else:
            print(f"   ❌ No pictograph component found in frame")


def main():
    """Run the option picker fixes debug"""
    print("🔧 Starting Option Picker Fixes Debug...")

    app = QApplication(sys.argv)
    app.setApplicationName("Option Picker Fixes Debug")

    # Create and show debug window
    window = OptionPickerFixesDebugWindow()
    window.show()

    print("🔧 Debug window created - testing fixes")

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
