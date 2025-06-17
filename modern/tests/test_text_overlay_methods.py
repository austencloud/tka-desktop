#!/usr/bin/env python3
"""
Comprehensive Visual Text Overlay Test Application

This test systematically evaluates different text rendering approaches for:
- START text overlay (Georgia 60pt DemiBold at top-left)
- Beat number text overlay (sequential numbers on beat views)

The goal is to identify working solutions for Modern construct tab beat frame text display issues.
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsProxyWidget,
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QFont, QPainter, QPen, QColor, QBrush

# Add src to path for Modern imports
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

try:
    from domain.models.core_models import BeatData
    from presentation.components.pictograph.pictograph_component import (
        PictographComponent,
    )

    Modern_IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Modern imports not available: {e}")
    print("Running with mock components for testing...")
    Modern_IMPORTS_AVAILABLE = False


class MockPictographComponent:
    """Mock pictograph component for testing when Modern imports unavailable"""

    def __init__(self, parent=None):
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 100, 100)
        # Add a simple background rectangle
        self.scene.addRect(
            0, 0, 100, 100, QPen(QColor("gray")), QBrush(QColor("lightgray"))
        )

    def update_from_beat(self, beat_data):
        pass

    def clear_pictograph(self):
        pass


class TestBeatView(QFrame):
    """Test beat view for evaluating text overlay methods"""

    def __init__(self, method_name: str, test_type: str, beat_number: int = 1):
        super().__init__()
        self.method_name = method_name
        self.test_type = test_type  # "START", "BEAT_NUMBER", or "COMBINED"
        self.beat_number = beat_number

        self.setFixedSize(120, 120)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setStyleSheet(
            """
            QFrame {
                background: white;
                border: 2px solid #ccc;
                border-radius: 8px;
            }
        """
        )

        # Setup pictograph component
        if Modern_IMPORTS_AVAILABLE:
            self.pictograph_component = PictographComponent(self)
        else:
            self.pictograph_component = MockPictographComponent()

        # Setup graphics view
        self.graphics_view = QGraphicsView(self.pictograph_component.scene, self)
        self.graphics_view.setGeometry(10, 10, 100, 100)
        self.graphics_view.setStyleSheet("border: 1px solid #999;")

        # Apply the specific text rendering method
        self._apply_text_method()

    def _apply_text_method(self):
        """Apply the specific text rendering method being tested"""
        try:
            if "QGraphicsTextItem" in self.method_name:
                self._test_graphics_text_item()
            elif "QLabel_overlay" in self.method_name:
                self._test_qlabel_overlay()
            elif "QPainter" in self.method_name:
                self._test_qpainter_method()
            elif "QGraphicsProxyWidget" in self.method_name:
                self._test_graphics_proxy_widget()
            elif "Custom_QGraphicsItem" in self.method_name:
                self._test_custom_graphics_item()
            elif "Pictograph_internal" in self.method_name:
                self._test_pictograph_internal()
        except Exception as e:
            print(f"❌ Error applying {self.method_name}: {e}")

    def _test_graphics_text_item(self):
        """Test QGraphicsTextItem added directly to scene"""
        scene = self.pictograph_component.scene

        if self.test_type in ["START", "COMBINED"]:
            start_text = QGraphicsTextItem("START")
            start_text.setFont(
                QFont("Georgia", 16, QFont.Weight.DemiBold)
            )  # Scaled down for test
            start_text.setDefaultTextColor(QColor("red"))
            start_text.setPos(5, 5)  # Top-left position
            scene.addItem(start_text)

        if self.test_type in ["BEAT_NUMBER", "COMBINED"]:
            beat_text = QGraphicsTextItem(str(self.beat_number))
            beat_text.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            beat_text.setDefaultTextColor(QColor("blue"))
            beat_text.setPos(75, 5)  # Top-right position
            scene.addItem(beat_text)

    def _test_qlabel_overlay(self):
        """Test QLabel positioned on top of beat view widget"""
        if self.test_type in ["START", "COMBINED"]:
            start_label = QLabel("START", self)
            start_label.setFont(QFont("Georgia", 12, QFont.Weight.DemiBold))
            start_label.setStyleSheet("color: red; background: rgba(255,255,255,128);")
            start_label.setGeometry(15, 15, 50, 20)
            start_label.show()

        if self.test_type in ["BEAT_NUMBER", "COMBINED"]:
            beat_label = QLabel(str(self.beat_number), self)
            beat_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            beat_label.setStyleSheet("color: blue; background: rgba(255,255,255,128);")
            beat_label.setGeometry(85, 15, 20, 20)
            beat_label.show()

    def _test_qpainter_method(self):
        """Test QPainter direct painting on widget"""
        # This will be handled in paintEvent
        self.use_qpainter = True

    def _test_graphics_proxy_widget(self):
        """Test QGraphicsProxyWidget containing QLabel"""
        scene = self.pictograph_component.scene

        if self.test_type in ["START", "COMBINED"]:
            start_label = QLabel("START")
            start_label.setFont(QFont("Georgia", 12, QFont.Weight.DemiBold))
            start_label.setStyleSheet("color: red; background: rgba(255,255,255,128);")
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(start_label)
            proxy.setPos(5, 5)
            scene.addItem(proxy)

        if self.test_type in ["BEAT_NUMBER", "COMBINED"]:
            beat_label = QLabel(str(self.beat_number))
            beat_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            beat_label.setStyleSheet("color: blue; background: rgba(255,255,255,128);")
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(beat_label)
            proxy.setPos(75, 5)
            scene.addItem(proxy)

    def _test_custom_graphics_item(self):
        """Test custom QGraphicsItem subclass"""
        scene = self.pictograph_component.scene

        if self.test_type in ["START", "COMBINED"]:
            start_item = CustomTextItem(
                "START", QFont("Georgia", 16, QFont.Weight.DemiBold), QColor("red")
            )
            start_item.setPos(5, 5)
            scene.addItem(start_item)

        if self.test_type in ["BEAT_NUMBER", "COMBINED"]:
            beat_item = CustomTextItem(
                str(self.beat_number),
                QFont("Arial", 14, QFont.Weight.Bold),
                QColor("blue"),
            )
            beat_item.setPos(75, 5)
            scene.addItem(beat_item)

    def _test_pictograph_internal(self):
        """Test text rendering within pictograph component"""
        # This would require modifying the actual pictograph component
        # For now, just add a note
        scene = self.pictograph_component.scene
        note = QGraphicsTextItem("Internal rendering test")
        note.setFont(QFont("Arial", 8))
        note.setDefaultTextColor(QColor("gray"))
        note.setPos(10, 40)
        scene.addItem(note)

    def paintEvent(self, event):
        """Handle QPainter method if enabled"""
        super().paintEvent(event)

        if hasattr(self, "use_qpainter") and self.use_qpainter:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            if self.test_type in ["START", "COMBINED"]:
                painter.setFont(QFont("Georgia", 12, QFont.Weight.DemiBold))
                painter.setPen(QColor("red"))
                painter.drawText(15, 30, "START")

            if self.test_type in ["BEAT_NUMBER", "COMBINED"]:
                painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                painter.setPen(QColor("blue"))
                painter.drawText(85, 30, str(self.beat_number))


try:
    from PyQt6.QtWidgets import QGraphicsItem

    class CustomTextItem(QGraphicsItem):
        """Custom QGraphicsItem for text rendering"""

        def __init__(self, text: str, font: QFont, color: QColor):
            super().__init__()
            self.text = text
            self.font = font
            self.color = color

        def boundingRect(self):
            return QRectF(0, 0, 50, 20)

        def paint(self, painter, option, widget):
            painter.setFont(self.font)
            painter.setPen(self.color)
            painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignLeft, self.text)

except ImportError:
    # Fallback for when QGraphicsItem is not available
    class CustomTextItem:
        def __init__(self, text: str, font: QFont, color: QColor):
            self.text = text
            self.font = font
            self.color = color

        def setPos(self, x, y):
            pass


class TextOverlayTestWindow(QMainWindow):
    """Main test window for text overlay methods"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "🧪 Text Overlay Methods Test - Modern Beat Frame Diagnosis"
        )
        self.setMinimumSize(1400, 1000)

        # Test results storage
        self.test_results = {}

        self._setup_ui()
        self._create_test_matrix()

    def _setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Title and instructions
        title = QLabel("Text Overlay Methods Test - Modern Beat Frame Diagnosis")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet(
            """
            QLabel {
                color: #2c3e50;
                padding: 15px;
                background-color: #ecf0f1;
                border-radius: 8px;
                margin: 10px;
            }
        """
        )
        layout.addWidget(title)

        instructions = QLabel(
            "Click '✅ This Works' if text is clearly visible, '❌ Not Working' if not. "
            "Results logged to console for implementation guidance."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #7f8c8d; font-size: 12px; margin: 5px;")
        layout.addWidget(instructions)

        # Test matrix container
        self.test_container = QWidget()
        self.test_layout = QGridLayout(self.test_container)
        layout.addWidget(self.test_container)

        # Results summary
        self.results_label = QLabel("Test Results: Click buttons to record findings...")
        self.results_label.setStyleSheet(
            """
            QLabel {
                color: #34495e;
                font-size: 14px;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 5px;
                margin: 10px;
            }
        """
        )
        layout.addWidget(self.results_label)

    def _create_test_matrix(self):
        """Create the test matrix with different rendering methods"""
        # Define test methods
        methods = [
            ("QGraphicsTextItem", "Direct QGraphicsTextItem to scene"),
            ("QLabel_overlay", "QLabel positioned over widget"),
            ("QPainter", "Direct QPainter in paintEvent"),
            ("QGraphicsProxyWidget", "QGraphicsProxyWidget with QLabel"),
            ("Custom_QGraphicsItem", "Custom QGraphicsItem subclass"),
            ("Pictograph_internal", "Internal pictograph rendering"),
        ]

        test_types = [
            ("START", "START Text Only"),
            ("BEAT_NUMBER", "Beat Number Only"),
            ("COMBINED", "START + Beat Number"),
        ]

        # Create headers
        self.test_layout.addWidget(QLabel("Method"), 0, 0)
        for col, (test_type, description) in enumerate(test_types, 1):
            header = QLabel(description)
            header.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header.setStyleSheet(
                """
                QLabel {
                    font-weight: bold;
                    color: #2c3e50;
                    background-color: #bdc3c7;
                    padding: 8px;
                    border-radius: 4px;
                }
            """
            )
            self.test_layout.addWidget(header, 0, col)

        # Create test cells
        for row, (method_name, method_desc) in enumerate(methods, 1):
            # Method name label
            method_label = QLabel(f"{method_name}\n({method_desc})")
            method_label.setWordWrap(True)
            method_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            method_label.setStyleSheet(
                """
                QLabel {
                    font-size: 10px;
                    color: #34495e;
                    background-color: #ecf0f1;
                    padding: 5px;
                    border-radius: 4px;
                    max-width: 120px;
                }
            """
            )
            self.test_layout.addWidget(method_label, row, 0)

            # Test cells for each type
            for col, (test_type, _) in enumerate(test_types, 1):
                cell_widget = self._create_test_cell(method_name, test_type, row + col)
                self.test_layout.addWidget(cell_widget, row, col)

    def _create_test_cell(
        self, method_name: str, test_type: str, beat_number: int
    ) -> QWidget:
        """Create a single test cell with beat view and feedback buttons"""
        cell = QWidget()
        layout = QVBoxLayout(cell)
        layout.setSpacing(5)

        # Test beat view
        beat_view = TestBeatView(method_name, test_type, beat_number)
        layout.addWidget(beat_view)

        # Feedback buttons
        button_layout = QHBoxLayout()

        success_btn = QPushButton("✅")
        success_btn.setFixedSize(30, 25)
        success_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """
        )
        success_btn.clicked.connect(
            lambda: self._record_result(method_name, test_type, True)
        )

        fail_btn = QPushButton("❌")
        fail_btn.setFixedSize(30, 25)
        fail_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        )
        fail_btn.clicked.connect(
            lambda: self._record_result(method_name, test_type, False)
        )

        button_layout.addWidget(success_btn)
        button_layout.addWidget(fail_btn)
        layout.addLayout(button_layout)

        cell.setStyleSheet(
            """
            QWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                margin: 2px;
            }
        """
        )

        return cell

    def _record_result(self, method_name: str, test_type: str, success: bool):
        """Record test result and update console/UI"""
        result_key = f"{method_name}_{test_type}"
        self.test_results[result_key] = success

        # Console logging
        status = "SUCCESS" if success else "FAILED"
        description = self._get_method_description(method_name, test_type)
        print(f"{status}: {result_key} - {description}")

        # Update results summary
        self._update_results_summary()

    def _get_method_description(self, method_name: str, test_type: str) -> str:
        """Get human-readable description of the test"""
        descriptions = {
            "QGraphicsTextItem": "QGraphicsTextItem added directly to pictograph scene",
            "QLabel_overlay": "QLabel positioned as overlay on beat view widget",
            "QPainter": "Direct QPainter rendering in widget paintEvent",
            "QGraphicsProxyWidget": "QGraphicsProxyWidget containing QLabel in scene",
            "Custom_QGraphicsItem": "Custom QGraphicsItem subclass for text",
            "Pictograph_internal": "Text rendering within pictograph component",
        }

        type_desc = {
            "START": "START text clearly visible at top-left",
            "BEAT_NUMBER": "Beat numbers visible and properly positioned",
            "COMBINED": "Both START text and beat numbers visible",
        }

        return f"{descriptions.get(method_name, method_name)} - {type_desc.get(test_type, test_type)}"

    def _update_results_summary(self):
        """Update the results summary display"""
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results.values() if result)

        summary = f"Test Results: {successful_tests}/{total_tests} methods working"

        if successful_tests > 0:
            working_methods = [
                key for key, result in self.test_results.items() if result
            ]
            summary += f"\n✅ Working: {', '.join(working_methods[:3])}"
            if len(working_methods) > 3:
                summary += f" (+{len(working_methods) - 3} more)"

        self.results_label.setText(summary)


def main():
    """Main function to run the text overlay test application"""
    print("🧪 Starting Text Overlay Methods Test")
    print("=" * 60)
    print("This test evaluates different approaches for rendering:")
    print("- START text overlay (Georgia 60pt DemiBold at top-left)")
    print("- Beat number text overlay (sequential numbers on beats)")
    print()
    print("INSTRUCTIONS:")
    print("1. Examine each test cell visually")
    print("2. Click ✅ if text is clearly visible and properly positioned")
    print("3. Click ❌ if text is not visible or incorrectly positioned")
    print("4. Check console output for detailed results")
    print()
    print("=== TEXT OVERLAY TEST RESULTS ===")

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set application-wide font for consistency
    app.setFont(QFont("Arial", 9))

    window = TextOverlayTestWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
