#!/usr/bin/env python3
"""
Simple Beat Frame Text Overlay Test

This test creates a real Modern beat frame with actual sequence data to test:
- START text overlay on start position beat (exact V1 specs)
- Beat number text overlay on sequence beats
- Proper sizing and scaling based on actual beat frame dimensions

Uses the exact sequence provided and bypasses complex dependency injection.
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
    from presentation.components.workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )
    from domain.models.core_models import (
        SequenceData,
        BeatData,
        MotionData,
        MotionType,
        RotationDirection,
        Location,
    )
    from application.services.layout.layout_management_service import (
        LayoutManagementService,
    )

    MODERN_IMPORTS_AVAILABLE = True
    print("✅ Modern imports successful - using real beat frame")
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


class SimpleBeatFrameTest(QMainWindow):
    """Simple test application using real Modern beat frame with actual sequence data"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧪 Simple Beat Frame Text Overlay Test - Modern")
        self.setMinimumSize(1400, 900)

        # Initialize components
        self.beat_frame = None
        self.sequence_data = None

        # Text overlay settings (adjustable)
        self.start_text_settings = {
            "font_size": 10,  # Start smaller
            "x_pos": 10,
            "y_pos": 10,
            "width": 60,  # Increased width to prevent clipping
            "height": 30,  # Increased height to prevent overflow
        }

        self.beat_number_settings = {
            "font_size": 10,  # Start smaller
            "x_pos": 10,
            "y_pos": 10,
            "width": 25,  # Increased width to prevent clipping
            "height": 25,  # Increased height to prevent overflow
        }

        self._setup_ui()
        self._load_sequence_data()

        # Delay beat frame creation to allow UI to render
        QTimer.singleShot(100, self._create_beat_frame)

    def _setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create splitter for beat frame and controls
        splitter = QSplitter(Qt.Orientation.Horizontal)
        central_widget_layout = QVBoxLayout(central_widget)
        central_widget_layout.addWidget(splitter)

        # Left side: Beat frame container
        self.beat_frame_container = QFrame()
        self.beat_frame_container.setStyleSheet(
            """
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #dee2e6;
                border-radius: 8px;
            }
        """
        )
        self.beat_frame_layout = QVBoxLayout(self.beat_frame_container)
        splitter.addWidget(self.beat_frame_container)

        # Right side: Controls and feedback
        controls_widget = self._create_controls_panel()
        splitter.addWidget(controls_widget)

        # Set splitter proportions (beat frame takes more space)
        splitter.setSizes([1000, 400])

    def _create_controls_panel(self) -> QWidget:
        """Create the controls and feedback panel"""
        controls = QWidget()
        controls.setMaximumWidth(400)
        layout = QVBoxLayout(controls)

        # Title
        title = QLabel("Simple Beat Frame Text Test")
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
            "This test uses a real Modern beat frame with the exact sequence provided.\n\n"
            "Expected behavior:\n"
            "• START text on start position beat (Georgia 60pt DemiBold)\n"
            "• Beat numbers 1,2,3,4 on sequence beats\n"
            "• Proper sizing based on actual beat frame dimensions"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #7f8c8d; font-size: 11px; margin: 5px;")
        layout.addWidget(instructions)

        # Status label
        self.status_label = QLabel("Initializing beat frame...")
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

        # Interactive adjustment controls
        self._create_adjustment_controls(layout)

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

    def _create_adjustment_controls(self, layout):
        """Create interactive adjustment controls for text positioning and sizing"""
        adjustment_label = QLabel("Interactive Text Adjustments:")
        adjustment_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        adjustment_label.setStyleSheet("color: #2c3e50; margin-top: 15px;")
        layout.addWidget(adjustment_label)

        # START text adjustments
        start_adj_label = QLabel("START Text Adjustments:")
        start_adj_label.setStyleSheet(
            "color: #34495e; font-weight: bold; margin-top: 10px;"
        )
        layout.addWidget(start_adj_label)

        # Size controls
        start_size_layout = QHBoxLayout()
        start_smaller_btn = QPushButton("📉 Smaller")
        start_smaller_btn.clicked.connect(
            lambda: self._adjust_start_text("font_size", -1)
        )
        start_smaller_btn.setStyleSheet(self._get_button_style("#e67e22"))

        start_bigger_btn = QPushButton("📈 Bigger")
        start_bigger_btn.clicked.connect(
            lambda: self._adjust_start_text("font_size", 1)
        )
        start_bigger_btn.setStyleSheet(self._get_button_style("#e67e22"))

        start_size_layout.addWidget(start_smaller_btn)
        start_size_layout.addWidget(start_bigger_btn)
        layout.addLayout(start_size_layout)

        # Position controls
        start_pos_layout = QHBoxLayout()
        start_left_btn = QPushButton("⬅️ Left")
        start_left_btn.clicked.connect(lambda: self._adjust_start_text("x_pos", -2))
        start_left_btn.setStyleSheet(self._get_button_style("#9b59b6"))

        start_right_btn = QPushButton("➡️ Right")
        start_right_btn.clicked.connect(lambda: self._adjust_start_text("x_pos", 2))
        start_right_btn.setStyleSheet(self._get_button_style("#9b59b6"))

        start_up_btn = QPushButton("⬆️ Up")
        start_up_btn.clicked.connect(lambda: self._adjust_start_text("y_pos", -2))
        start_up_btn.setStyleSheet(self._get_button_style("#9b59b6"))

        start_down_btn = QPushButton("⬇️ Down")
        start_down_btn.clicked.connect(lambda: self._adjust_start_text("y_pos", 2))
        start_down_btn.setStyleSheet(self._get_button_style("#9b59b6"))

        start_pos_layout.addWidget(start_left_btn)
        start_pos_layout.addWidget(start_right_btn)
        start_pos_layout.addWidget(start_up_btn)
        start_pos_layout.addWidget(start_down_btn)
        layout.addLayout(start_pos_layout)

        # Beat numbers adjustments
        beat_adj_label = QLabel("Beat Numbers Adjustments:")
        beat_adj_label.setStyleSheet(
            "color: #34495e; font-weight: bold; margin-top: 10px;"
        )
        layout.addWidget(beat_adj_label)

        # Size controls
        beat_size_layout = QHBoxLayout()
        beat_smaller_btn = QPushButton("📉 Smaller")
        beat_smaller_btn.clicked.connect(
            lambda: self._adjust_beat_numbers("font_size", -1)
        )
        beat_smaller_btn.setStyleSheet(self._get_button_style("#e67e22"))

        beat_bigger_btn = QPushButton("📈 Bigger")
        beat_bigger_btn.clicked.connect(
            lambda: self._adjust_beat_numbers("font_size", 1)
        )
        beat_bigger_btn.setStyleSheet(self._get_button_style("#e67e22"))

        beat_size_layout.addWidget(beat_smaller_btn)
        beat_size_layout.addWidget(beat_bigger_btn)
        layout.addLayout(beat_size_layout)

        # Position controls
        beat_pos_layout = QHBoxLayout()
        beat_left_btn = QPushButton("⬅️ Left")
        beat_left_btn.clicked.connect(lambda: self._adjust_beat_numbers("x_pos", -2))
        beat_left_btn.setStyleSheet(self._get_button_style("#9b59b6"))

        beat_right_btn = QPushButton("➡️ Right")
        beat_right_btn.clicked.connect(lambda: self._adjust_beat_numbers("x_pos", 2))
        beat_right_btn.setStyleSheet(self._get_button_style("#9b59b6"))

        beat_up_btn = QPushButton("⬆️ Up")
        beat_up_btn.clicked.connect(lambda: self._adjust_beat_numbers("y_pos", -2))
        beat_up_btn.setStyleSheet(self._get_button_style("#9b59b6"))

        beat_down_btn = QPushButton("⬇️ Down")
        beat_down_btn.clicked.connect(lambda: self._adjust_beat_numbers("y_pos", 2))
        beat_down_btn.setStyleSheet(self._get_button_style("#9b59b6"))

        beat_pos_layout.addWidget(beat_left_btn)
        beat_pos_layout.addWidget(beat_right_btn)
        beat_pos_layout.addWidget(beat_up_btn)
        beat_pos_layout.addWidget(beat_down_btn)
        layout.addLayout(beat_pos_layout)

        # Apply changes button
        apply_btn = QPushButton("🔄 Apply Changes")
        apply_btn.clicked.connect(self._apply_text_adjustments)
        apply_btn.setStyleSheet(self._get_button_style("#27ae60"))
        layout.addWidget(apply_btn)

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

    def _create_motion_data_from_json(self, motion_attrs):
        """Convert JSON motion attributes to MotionData object"""
        try:
            return MotionData(
                motion_type=MotionType(motion_attrs["motion_type"]),
                prop_rot_dir=RotationDirection(motion_attrs["prop_rot_dir"]),
                start_loc=Location(motion_attrs["start_loc"]),
                end_loc=Location(motion_attrs["end_loc"]),
                turns=motion_attrs.get("turns", 0.0),
                start_ori=motion_attrs.get("start_ori", "in"),
                end_ori=motion_attrs.get("end_ori", "in"),
            )
        except Exception as e:
            print(f"Error creating motion data: {e}")
            return None

    def _load_sequence_data(self):
        """Load and create real sequence data with actual motion data"""
        try:
            sequence_json = json.loads(SEQUENCE_JSON)

            if MODERN_IMPORTS_AVAILABLE:
                beats = []

                # Sequence beats (beats 1-4) - from JSON indices 2-5
                # Index 1 is start position (handled separately), indices 2-5 are actual beats
                for i, beat_json in enumerate(
                    sequence_json[2:], 1
                ):  # Start from beat 1
                    blue_motion = self._create_motion_data_from_json(
                        beat_json["blue_attributes"]
                    )
                    red_motion = self._create_motion_data_from_json(
                        beat_json["red_attributes"]
                    )

                    beat = BeatData(
                        beat_number=i,
                        letter=beat_json["letter"],
                        duration=beat_json.get("duration", 1.0),
                        blue_motion=blue_motion,
                        red_motion=red_motion,
                        is_blank=False,
                    )
                    beats.append(beat)

                # Store start position data separately (from JSON index 1)
                start_position_json = sequence_json[1]
                start_position_data = {
                    "letter": start_position_json["letter"],
                    "blue_motion": self._create_motion_data_from_json(
                        start_position_json["blue_attributes"]
                    ),
                    "red_motion": self._create_motion_data_from_json(
                        start_position_json["red_attributes"]
                    ),
                    "end_pos": start_position_json["end_pos"],
                }

                # Create sequence data with start position
                self.sequence_data = SequenceData(
                    name="AABB Test Sequence",
                    word="AABB",
                    beats=beats,
                    start_position=start_position_data["end_pos"],  # alpha1
                )

                # Store start position data for later use
                self.start_position_data = start_position_data

                self.status_label.setText(
                    f"✅ Real sequence created: {self.sequence_data.word} ({self.sequence_data.length} beats + start position with motion data)"
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

                print(f"✅ Created sequence with real motion data:")
                print(
                    f"  Start Position: {start_position_data['letter']} at {start_position_data['end_pos']} - Blue: {start_position_data['blue_motion'].motion_type.value if start_position_data['blue_motion'] else 'None'}, Red: {start_position_data['red_motion'].motion_type.value if start_position_data['red_motion'] else 'None'}"
                )
                for beat in beats:
                    print(
                        f"  Beat {beat.beat_number}: {beat.letter} - Blue: {beat.blue_motion.motion_type.value if beat.blue_motion else 'None'}, Red: {beat.red_motion.motion_type.value if beat.red_motion else 'None'}"
                    )

            else:
                self.status_label.setText(
                    "⚠️ Modern imports unavailable - cannot create sequence"
                )

        except Exception as e:
            self.status_label.setText(f"❌ Error creating sequence: {e}")
            print(f"Error creating sequence: {e}")
            import traceback

            traceback.print_exc()

    def _create_beat_frame(self):
        """Create the real Modern beat frame instance"""
        if not MODERN_IMPORTS_AVAILABLE or not self.sequence_data:
            self.status_label.setText(
                "❌ Cannot create beat frame - missing dependencies or sequence data"
            )
            return

        try:
            # Create layout service
            layout_service = LayoutManagementService()

            # Create real Modern beat frame
            self.beat_frame = SequenceBeatFrame(layout_service)
            self.beat_frame_layout.addWidget(self.beat_frame)

            # Load the sequence into the beat frame
            self.beat_frame.set_sequence(self.sequence_data)

            # Set start position data if available
            if hasattr(self, "start_position_data") and self.start_position_data:
                self._set_start_position_data()

            self.status_label.setText(
                "✅ Real Modern beat frame created with sequence loaded!"
            )
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

            print("✅ Beat frame created successfully!")
            print(
                f"✅ Sequence loaded: {self.sequence_data.word} with {self.sequence_data.length} beats"
            )

        except Exception as e:
            self.status_label.setText(f"❌ Error creating beat frame: {e}")
            print(f"Error creating beat frame: {e}")
            import traceback

            traceback.print_exc()

    def _set_start_position_data(self):
        """Set the start position data on the beat frame"""
        try:
            if (
                hasattr(self.beat_frame, "_start_position_view")
                and self.beat_frame._start_position_view
            ):
                # Create BeatData for start position (use beat_number=1 since it must be positive)
                start_beat_data = BeatData(
                    beat_number=1,  # Must be positive, but this represents start position
                    letter=self.start_position_data["letter"],
                    blue_motion=self.start_position_data["blue_motion"],
                    red_motion=self.start_position_data["red_motion"],
                    is_blank=False,
                )

                # Set the start position data
                self.beat_frame._start_position_view.set_position_data(start_beat_data)
                print(
                    f"✅ Start position data set: {start_beat_data.letter} with motion data"
                )
            else:
                print("❌ Start position view not found in beat frame")
        except Exception as e:
            print(f"❌ Error setting start position data: {e}")
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

    def _adjust_start_text(self, property_name: str, delta: int):
        """Adjust START text property and log the change"""
        old_value = self.start_text_settings[property_name]
        self.start_text_settings[property_name] = max(
            1, old_value + delta
        )  # Ensure positive values
        new_value = self.start_text_settings[property_name]
        print(f"🔧 START text {property_name}: {old_value} → {new_value}")
        self.status_label.setText(
            f"🔧 START text {property_name}: {old_value} → {new_value}"
        )

    def _adjust_beat_numbers(self, property_name: str, delta: int):
        """Adjust beat numbers property and log the change"""
        old_value = self.beat_number_settings[property_name]
        self.beat_number_settings[property_name] = max(
            1, old_value + delta
        )  # Ensure positive values
        new_value = self.beat_number_settings[property_name]
        print(f"🔧 Beat numbers {property_name}: {old_value} → {new_value}")
        self.status_label.setText(
            f"🔧 Beat numbers {property_name}: {old_value} → {new_value}"
        )

    def _apply_text_adjustments(self):
        """Apply the current text settings by re-implementing the overlays"""
        print(f"🔄 Applying text adjustments...")
        print(f"   START text settings: {self.start_text_settings}")
        print(f"   Beat number settings: {self.beat_number_settings}")

        # Clear existing overlays and re-implement with new settings
        self._clear_existing_overlays()
        self._implement_text_overlays()

        self.status_label.setText("🔄 Text adjustments applied!")

    def _clear_existing_overlays(self):
        """Clear existing text overlays before applying new ones"""
        try:
            # Clear start position overlays
            if (
                hasattr(self.beat_frame, "_start_position_view")
                and self.beat_frame._start_position_view
            ):
                start_view = self.beat_frame._start_position_view
                if hasattr(start_view, "_text_overlays"):
                    for overlay in start_view._text_overlays:
                        overlay.deleteLater()
                    start_view._text_overlays.clear()

            # Clear beat view overlays
            if hasattr(self.beat_frame, "_beat_views"):
                for beat_view in self.beat_frame._beat_views[:4]:  # Only first 4
                    if beat_view and hasattr(beat_view, "_text_overlays"):
                        for overlay in beat_view._text_overlays:
                            overlay.deleteLater()
                        beat_view._text_overlays.clear()

            print("🧹 Cleared existing text overlays")
        except Exception as e:
            print(f"❌ Error clearing overlays: {e}")

    def _test_text_implementation(self):
        """Test text overlay implementation directly"""
        if not self.beat_frame:
            self.status_label.setText("❌ No beat frame available for testing")
            return

        try:
            self.status_label.setText("🔧 Testing text implementation on beat frame...")
            print("🔧 Attempting to implement text overlays...")

            # This is where we would implement the working text overlay method
            # based on the results from the previous test
            self._implement_text_overlays()

        except Exception as e:
            self.status_label.setText(f"❌ Text implementation test failed: {e}")
            print(f"Text implementation error: {e}")

    def _implement_text_overlays(self):
        """Implement text overlays using the QLabel overlay method that worked"""
        try:
            print("🔧 Implementing text overlays using QLabel overlay method...")

            # Access the start position view and beat views separately
            if hasattr(self.beat_frame, "_start_position_view"):
                start_position_view = self.beat_frame._start_position_view
                if start_position_view:
                    self._add_start_text_overlay(start_position_view)
                    print("✅ Added START text to start position view")
                else:
                    print("❌ Start position view is None")
            else:
                print("❌ Start position view not found in beat frame")

            # Access beat views - only add numbers to the first 4 beats that contain our sequence
            if hasattr(self.beat_frame, "_beat_views"):
                beat_views = self.beat_frame._beat_views
                print(f"📊 Found {len(beat_views)} beat views total")

                # Only add beat numbers to the first 4 beats (our actual sequence length)
                sequence_length = (
                    len(self.sequence_data.beats) if self.sequence_data else 4
                )
                print(f"📊 Adding beat numbers to first {sequence_length} beat views")

                for i in range(min(sequence_length, len(beat_views))):
                    beat_view = beat_views[i]
                    if beat_view:
                        # Add beat number (1, 2, 3, 4)
                        self._add_beat_number_overlay(beat_view, i + 1)
                        print(f"✅ Added beat number {i + 1} to beat view {i}")
                    else:
                        print(f"❌ Beat view {i} is None")
            else:
                print("❌ Beat views not found in beat frame")

            self.status_label.setText(
                "✅ Text overlays implemented! Check beat frame for START text and beat numbers."
            )

        except Exception as e:
            print(f"❌ Error implementing text overlays: {e}")
            import traceback

            traceback.print_exc()
            self.status_label.setText(f"❌ Text overlay implementation failed: {e}")

    def _add_start_text_overlay(self, start_position_view):
        """Add Start text overlay using widget overlay approach (more reliable)"""
        try:
            # Try widget overlay approach - create QLabel directly on the view
            from PyQt6.QtWidgets import QLabel
            from PyQt6.QtCore import Qt

            start_label = QLabel("Start", start_position_view)
            start_label.setFont(
                QFont(
                    "Georgia",
                    self.start_text_settings["font_size"],
                    QFont.Weight.DemiBold,
                )
            )  # Use configurable font size
            start_label.setStyleSheet(
                """
                QLabel {
                    color: black;
                    background: transparent;
                    border: none;
                    padding: 0px;
                }
            """
            )

            # Use configurable position and size
            start_label.setGeometry(
                self.start_text_settings["x_pos"],
                self.start_text_settings["y_pos"],
                self.start_text_settings["width"],
                self.start_text_settings["height"],
            )
            start_label.show()
            start_label.raise_()  # Bring to front

            # Store reference to prevent garbage collection
            if not hasattr(start_position_view, "_text_overlays"):
                start_position_view._text_overlays = []
            start_position_view._text_overlays.append(start_label)

            print(
                f"✅ Start text widget overlay added at ({self.start_text_settings['x_pos']}, {self.start_text_settings['y_pos']}) with Georgia {self.start_text_settings['font_size']}pt DemiBold font"
            )
            print(f"   Widget geometry: {start_label.geometry()}")
            print(f"   Widget is visible: {start_label.isVisible()}")
            print(f"   Parent view size: {start_position_view.size()}")

        except Exception as e:
            print(f"❌ Error adding Start text overlay: {e}")
            import traceback

            traceback.print_exc()

    def _add_beat_number_overlay(self, beat_view, beat_number):
        """Add beat number overlay to a beat view using exact Legacy approach"""
        try:
            # Try widget overlay approach - create QLabel directly on the view
            from PyQt6.QtWidgets import QLabel

            number_label = QLabel(str(beat_number), beat_view)
            number_label.setFont(
                QFont(
                    "Georgia",
                    self.beat_number_settings["font_size"],
                    QFont.Weight.DemiBold,
                )
            )  # Use configurable font size
            number_label.setStyleSheet(
                """
                QLabel {
                    color: black;
                    background: transparent;
                    border: none;
                    padding: 0px;
                }
            """
            )

            # Use configurable position and size
            number_label.setGeometry(
                self.beat_number_settings["x_pos"],
                self.beat_number_settings["y_pos"],
                self.beat_number_settings["width"],
                self.beat_number_settings["height"],
            )
            number_label.show()
            number_label.raise_()  # Bring to front

            # Store reference to prevent garbage collection
            if not hasattr(beat_view, "_text_overlays"):
                beat_view._text_overlays = []
            beat_view._text_overlays.append(number_label)

            print(
                f"✅ Beat number {beat_number} widget overlay added at ({self.beat_number_settings['x_pos']}, {self.beat_number_settings['y_pos']}) with Georgia {self.beat_number_settings['font_size']}pt DemiBold font"
            )
            print(f"   Widget geometry: {number_label.geometry()}")
            print(f"   Widget is visible: {number_label.isVisible()}")
            print(f"   Parent view size: {beat_view.size()}")

        except Exception as e:
            print(f"❌ Error adding beat number overlay: {e}")
            import traceback

            traceback.print_exc()


def main():
    """Main function to run the simple beat frame text overlay test"""
    print("🧪 Starting Simple Beat Frame Text Overlay Test")
    print("=" * 60)
    print("This test creates a real Modern beat frame with actual sequence data:")
    print("- Word: AABB (5 beats including start position)")
    print("- Start position: alpha1 (static)")
    print("- Beat progression: alpha1→alpha3→alpha5→alpha3→alpha1")
    print("- Tests START text and beat number overlays with proper sizing")
    print()
    print("INSTRUCTIONS:")
    print("1. Wait for beat frame to load with sequence")
    print("2. Examine START text on start position beat")
    print("3. Examine beat numbers on sequence beats (1,2,3,4)")
    print("4. Use feedback buttons to report what you see")
    print("5. Use 'Test Text Implementation' to try fixes")
    print()
    print("=== SIMPLE BEAT FRAME TEXT OVERLAY TEST ===")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = SimpleBeatFrameTest()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
