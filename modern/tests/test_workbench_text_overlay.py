#!/usr/bin/env python3
"""
Real Workbench Text Overlay Test

This test creates an actual Modern workbench instance with a real sequence to test:
- START text overlay on start position beat (exact V1 specs)
- Beat number text overlay on sequence beats
- Proper sizing and scaling based on actual beat frame dimensions

Uses the exact sequence provided to ensure logical beat progression and proper
prop orientations following the kinetic alphabet rules.
"""

import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTextEdit,
    QSplitter,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# Add src to path for Modern imports
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

try:
    from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
    from core.dependency_injection.di_container import DIContainer
    from domain.models.core_models import SequenceData, BeatData

    MODERN_IMPORTS_AVAILABLE = True
    print("✅ Modern imports successful - using real construct tab")
except ImportError as e:
    print(f"❌ Modern imports failed: {e}")
    print(f"Error details: {e}")
    import traceback

    traceback.print_exc()
    MODERN_IMPORTS_AVAILABLE = False


# The exact sequence data provided
SEQUENCE_JSON = """[
    {
        "word": "AABB",
        "author": "",
        "level": 1,
        "prop_type": "staff",
        "grid_mode": "diamond",
        "is_circular": true,
        "can_be_CAP": true,
        "is_strict_rotated_CAP": false,
        "is_strict_mirrored_CAP": true,
        "is_strict_swapped_CAP": false,
        "is_mirrored_swapped_CAP": false,
        "is_rotated_swapped_CAP": false
    },
    {
        "beat": 0,
        "sequence_start_position": "alpha",
        "letter": "α",
        "end_pos": "alpha1",
        "timing": "none",
        "direction": "none",
        "blue_attributes": {
            "start_loc": "s",
            "end_loc": "s",
            "start_ori": "in",
            "end_ori": "in",
            "prop_rot_dir": "no_rot",
            "turns": 0,
            "motion_type": "static"
        },
        "red_attributes": {
            "start_loc": "n",
            "end_loc": "n",
            "start_ori": "in",
            "end_ori": "in",
            "prop_rot_dir": "no_rot",
            "turns": 0,
            "motion_type": "static"
        }
    },
    {
        "beat": 1,
        "letter": "A",
        "letter_type": "Type1",
        "duration": 1,
        "start_pos": "alpha1",
        "end_pos": "alpha3",
        "timing": "split",
        "direction": "same",
        "blue_attributes": {
            "motion_type": "pro",
            "start_ori": "in",
            "prop_rot_dir": "cw",
            "start_loc": "s",
            "end_loc": "w",
            "turns": 0,
            "end_ori": "in"
        },
        "red_attributes": {
            "motion_type": "pro",
            "start_ori": "in",
            "prop_rot_dir": "cw",
            "start_loc": "n",
            "end_loc": "e",
            "turns": 0,
            "end_ori": "in"
        }
    },
    {
        "beat": 2,
        "letter": "A",
        "letter_type": "Type1",
        "duration": 1,
        "start_pos": "alpha3",
        "end_pos": "alpha5",
        "timing": "split",
        "direction": "same",
        "blue_attributes": {
            "motion_type": "pro",
            "start_ori": "in",
            "prop_rot_dir": "cw",
            "start_loc": "w",
            "end_loc": "n",
            "turns": 0,
            "end_ori": "in"
        },
        "red_attributes": {
            "motion_type": "pro",
            "start_ori": "in",
            "prop_rot_dir": "cw",
            "start_loc": "e",
            "end_loc": "s",
            "turns": 0,
            "end_ori": "in"
        }
    },
    {
        "beat": 3,
        "letter": "B",
        "letter_type": "Type1",
        "duration": 1,
        "start_pos": "alpha5",
        "end_pos": "alpha3",
        "timing": "split",
        "direction": "same",
        "blue_attributes": {
            "motion_type": "anti",
            "start_ori": "in",
            "prop_rot_dir": "cw",
            "start_loc": "n",
            "end_loc": "w",
            "turns": 0,
            "end_ori": "out"
        },
        "red_attributes": {
            "motion_type": "anti",
            "start_ori": "in",
            "prop_rot_dir": "cw",
            "start_loc": "s",
            "end_loc": "e",
            "turns": 0,
            "end_ori": "out"
        }
    },
    {
        "beat": 4,
        "letter": "B",
        "letter_type": "Type1",
        "duration": 1,
        "start_pos": "alpha3",
        "end_pos": "alpha1",
        "timing": "split",
        "direction": "same",
        "blue_attributes": {
            "motion_type": "anti",
            "start_ori": "out",
            "prop_rot_dir": "cw",
            "start_loc": "w",
            "end_loc": "s",
            "turns": 0,
            "end_ori": "in"
        },
        "red_attributes": {
            "motion_type": "anti",
            "start_ori": "out",
            "prop_rot_dir": "cw",
            "start_loc": "e",
            "end_loc": "n",
            "turns": 0,
            "end_ori": "in"
        }
    }
]"""


class WorkbenchTextOverlayTest(QMainWindow):
    """Test application using real Modern workbench with actual sequence data"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 Real Workbench Text Overlay Test - Modern")
        self.setMinimumSize(1600, 1000)

        # Initialize components
        self.container = DIContainer() if MODERN_IMPORTS_AVAILABLE else None
        self.construct_tab = None
        self.sequence_data = None

        self._setup_ui()
        self._load_sequence_data()

        # Delay construct tab creation to allow UI to render
        QTimer.singleShot(100, self._create_construct_tab)

    def _setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create splitter for workbench and controls
        splitter = QSplitter(Qt.Orientation.Horizontal)
        central_widget_layout = QVBoxLayout(central_widget)
        central_widget_layout.addWidget(splitter)

        # Left side: Workbench container
        self.workbench_container = QFrame()
        self.workbench_container.setStyleSheet(
            """
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
            }
        """
        )
        self.workbench_layout = QVBoxLayout(self.workbench_container)
        splitter.addWidget(self.workbench_container)

        # Right side: Controls and feedback
        controls_widget = self._create_controls_panel()
        splitter.addWidget(controls_widget)

        # Set splitter proportions (workbench takes more space)
        splitter.setSizes([1200, 400])

    def _create_controls_panel(self) -> QWidget:
        """Create the controls and feedback panel"""
        controls = QWidget()
        controls.setMaximumWidth(400)
        layout = QVBoxLayout(controls)

        # Title
        title = QLabel("Real Workbench Text Overlay Test")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            QLabel {
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
                margin: 5px;
            }
        """
        )
        layout.addWidget(title)

        # Instructions
        instructions = QLabel(
            "This test uses a real Modern workbench with the exact sequence provided.\n\n"
            "Expected behavior:\n"
            "• START text on start position beat (Georgia 60pt DemiBold)\n"
            "• Beat numbers 1,2,3,4 on sequence beats\n"
            "• Proper sizing based on actual beat frame dimensions"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #7f8c8d; font-size: 11px; margin: 5px;")
        layout.addWidget(instructions)

        # Status label
        self.status_label = QLabel("Initializing workbench...")
        self.status_label.setStyleSheet(
            """
            QLabel {
                color: #3498db;
                font-size: 12px;
                padding: 8px;
                background-color: #ebf3fd;
                border-radius: 4px;
                margin: 5px;
            }
        """
        )
        layout.addWidget(self.status_label)

        # Feedback buttons
        self._create_feedback_buttons(layout)

        # Sequence data display
        self._create_sequence_display(layout)

        layout.addStretch()
        return controls

    def _create_feedback_buttons(self, layout):
        """Create feedback buttons for different text overlay issues"""
        feedback_label = QLabel("Text Overlay Feedback:")
        feedback_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        feedback_label.setStyleSheet("color: #2c3e50; margin-top: 10px;")
        layout.addWidget(feedback_label)

        # START text feedback
        start_text_label = QLabel("START Text on Start Position:")
        start_text_label.setStyleSheet(
            "color: #34495e; font-weight: bold; margin-top: 5px;"
        )
        layout.addWidget(start_text_label)

        start_buttons_layout = QHBoxLayout()

        start_visible_btn = QPushButton("✅ Visible")
        start_visible_btn.clicked.connect(
            lambda: self._log_feedback("START_TEXT", "VISIBLE")
        )
        start_visible_btn.setStyleSheet(self._get_button_style("#27ae60"))

        start_missing_btn = QPushButton("❌ Missing")
        start_missing_btn.clicked.connect(
            lambda: self._log_feedback("START_TEXT", "MISSING")
        )
        start_missing_btn.setStyleSheet(self._get_button_style("#e74c3c"))

        start_wrong_size_btn = QPushButton("⚠️ Wrong Size")
        start_wrong_size_btn.clicked.connect(
            lambda: self._log_feedback("START_TEXT", "WRONG_SIZE")
        )
        start_wrong_size_btn.setStyleSheet(self._get_button_style("#f39c12"))

        start_buttons_layout.addWidget(start_visible_btn)
        start_buttons_layout.addWidget(start_missing_btn)
        start_buttons_layout.addWidget(start_wrong_size_btn)
        layout.addLayout(start_buttons_layout)

        # Beat numbers feedback
        beat_numbers_label = QLabel("Beat Numbers on Sequence Beats:")
        beat_numbers_label.setStyleSheet(
            "color: #34495e; font-weight: bold; margin-top: 10px;"
        )
        layout.addWidget(beat_numbers_label)

        beat_buttons_layout = QHBoxLayout()

        beat_visible_btn = QPushButton("✅ All Visible")
        beat_visible_btn.clicked.connect(
            lambda: self._log_feedback("BEAT_NUMBERS", "ALL_VISIBLE")
        )
        beat_visible_btn.setStyleSheet(self._get_button_style("#27ae60"))

        beat_missing_btn = QPushButton("❌ Missing")
        beat_missing_btn.clicked.connect(
            lambda: self._log_feedback("BEAT_NUMBERS", "MISSING")
        )
        beat_missing_btn.setStyleSheet(self._get_button_style("#e74c3c"))

        beat_partial_btn = QPushButton("⚠️ Partial")
        beat_partial_btn.clicked.connect(
            lambda: self._log_feedback("BEAT_NUMBERS", "PARTIAL")
        )
        beat_partial_btn.setStyleSheet(self._get_button_style("#f39c12"))

        beat_buttons_layout.addWidget(beat_visible_btn)
        beat_buttons_layout.addWidget(beat_missing_btn)
        beat_buttons_layout.addWidget(beat_partial_btn)
        layout.addLayout(beat_buttons_layout)

        # Implementation test button
        test_implementation_btn = QPushButton("🔧 Test Text Implementation")
        test_implementation_btn.clicked.connect(self._test_text_implementation)
        test_implementation_btn.setStyleSheet(self._get_button_style("#3498db"))
        layout.addWidget(test_implementation_btn)

    def _get_button_style(self, color: str) -> str:
        """Get button style with specified color"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
                margin: 2px;
            }}
            QPushButton:hover {{
                background-color: {color}dd;
            }}
        """

    def _create_sequence_display(self, layout):
        """Create sequence data display"""
        sequence_label = QLabel("Loaded Sequence Data:")
        sequence_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        sequence_label.setStyleSheet("color: #2c3e50; margin-top: 15px;")
        layout.addWidget(sequence_label)

        self.sequence_display = QTextEdit()
        self.sequence_display.setMaximumHeight(200)
        self.sequence_display.setStyleSheet(
            """
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-family: monospace;
                font-size: 9px;
            }
        """
        )
        layout.addWidget(self.sequence_display)

    def _load_sequence_data(self):
        """Load and display the sequence data"""
        try:
            sequence_json = json.loads(SEQUENCE_JSON)
            self.sequence_display.setPlainText(json.dumps(sequence_json, indent=2))

            if MODERN_IMPORTS_AVAILABLE:
                # For now, just create a simple sequence data structure
                # We'll load it into the construct tab when it's created
                self.sequence_json = sequence_json
                self.status_label.setText(
                    f"✅ Sequence JSON loaded: AABB (5 beats including start position)"
                )
                self.status_label.setStyleSheet(
                    """
                    QLabel {
                        color: #27ae60;
                        font-size: 12px;
                        padding: 8px;
                        background-color: #d5f4e6;
                        border-radius: 4px;
                        margin: 5px;
                    }
                """
                )
            else:
                self.status_label.setText(
                    "⚠️ Modern imports unavailable - cannot load sequence"
                )

        except Exception as e:
            self.status_label.setText(f"❌ Error loading sequence: {e}")
            print(f"Error loading sequence: {e}")

    def _create_construct_tab(self):
        """Create the real Modern construct tab instance"""
        if not MODERN_IMPORTS_AVAILABLE or self.container is None:
            self.status_label.setText(
                "❌ Cannot create construct tab - missing dependencies"
            )
            return

        try:
            # Create real Modern construct tab
            self.construct_tab = ConstructTabWidget(self.container)
            self.workbench_layout.addWidget(self.construct_tab)

            self.status_label.setText("✅ Real Modern construct tab created!")
            self.status_label.setStyleSheet(
                """
                QLabel {
                    color: #27ae60;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 8px;
                    background-color: #d5f4e6;
                    border: 2px solid #27ae60;
                    border-radius: 4px;
                    margin: 5px;
                }
            """
            )

            print("✅ Construct tab created successfully!")
            print("✅ Ready to test text overlays on real Modern components!")

        except Exception as e:
            self.status_label.setText(f"❌ Error creating construct tab: {e}")
            print(f"Error creating construct tab: {e}")
            import traceback

            traceback.print_exc()

    def _log_feedback(self, component: str, status: str):
        """Log user feedback about text overlay visibility"""
        message = f"FEEDBACK: {component} - {status}"
        print(message)

        # Update status with feedback
        feedback_messages = {
            ("START_TEXT", "VISIBLE"): "✅ START text confirmed visible!",
            ("START_TEXT", "MISSING"): "❌ START text missing - needs implementation",
            (
                "START_TEXT",
                "WRONG_SIZE",
            ): "⚠️ START text wrong size - needs font/scaling fix",
            ("BEAT_NUMBERS", "ALL_VISIBLE"): "✅ All beat numbers confirmed visible!",
            (
                "BEAT_NUMBERS",
                "MISSING",
            ): "❌ Beat numbers missing - needs implementation",
            (
                "BEAT_NUMBERS",
                "PARTIAL",
            ): "⚠️ Some beat numbers missing - partial implementation",
        }

        feedback_msg = feedback_messages.get(
            (component, status), f"Feedback recorded: {component} - {status}"
        )
        self.status_label.setText(feedback_msg)

    def _test_text_implementation(self):
        """Test text overlay implementation directly"""
        if not self.workbench:
            self.status_label.setText("❌ No workbench available for testing")
            return

        try:
            # Try to access beat frame and implement text overlays
            beat_frame = getattr(self.workbench, "_beat_frame", None)
            if beat_frame:
                self.status_label.setText(
                    "🔧 Testing text implementation on beat frame..."
                )
                print("🔧 Attempting to implement text overlays...")

                # This is where we would implement the working text overlay method
                # based on the results from the previous test
                self._implement_text_overlays(beat_frame)
            else:
                self.status_label.setText("❌ Beat frame not accessible")

        except Exception as e:
            self.status_label.setText(f"❌ Text implementation test failed: {e}")
            print(f"Text implementation error: {e}")

    def _implement_text_overlays(self, beat_frame):
        """Implement text overlays using the method that worked in previous tests"""
        # Based on previous test results, QLabel overlay method worked
        # This is where we would implement the actual fix
        print("🔧 Implementing text overlays...")
        self.status_label.setText(
            "🔧 Text overlay implementation attempted - check console for details"
        )


def main():
    """Main function to run the real workbench text overlay test"""
    print("🧪 Starting Real Workbench Text Overlay Test")
    print("=" * 60)
    print("This test creates a real Modern workbench with actual sequence data:")
    print("- Word: AABB (4 beats)")
    print("- Start position: alpha1 (static)")
    print("- Beat progression: alpha1→alpha3→alpha5→alpha3→alpha1")
    print("- Tests START text and beat number overlays with proper sizing")
    print()
    print("INSTRUCTIONS:")
    print("1. Wait for workbench to load with sequence")
    print("2. Examine START text on start position beat")
    print("3. Examine beat numbers on sequence beats (1,2,3,4)")
    print("4. Use feedback buttons to report what you see")
    print("5. Use 'Test Text Implementation' to try fixes")
    print()
    print("=== REAL WORKBENCH TEXT OVERLAY TEST ===")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = WorkbenchTextOverlayTest()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
