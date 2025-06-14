from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt
from ....domain.models.core_models import BeatData
from presentation.components.pictograph.pictograph_component import PictographComponent


class ClickablePictographFrame(QFrame):
    clicked = pyqtSignal(str)

    def __init__(self, beat_data: BeatData, parent=None):
        # Validate parent before proceeding
        if parent is not None:
            try:
                # Test if parent is still valid
                _ = parent.isVisible()
            except RuntimeError:
                print(
                    f"❌ Parent widget deleted, cannot create ClickablePictographFrame"
                )
                raise RuntimeError("Parent widget has been deleted")

        super().__init__(parent)
        self.beat_data = beat_data
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)

        # Store parent container for dynamic sizing (V1-style)
        self.container_widget = None

        # Initial size - will be updated by resize_frame()
        square_size = 160
        self.setFixedSize(square_size, square_size)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setSpacing(0)

        try:
            # Create pictograph component with proper parent
            self.pictograph_component = PictographComponent(parent=self)
            self.pictograph_component.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.pictograph_component.update_from_beat(beat_data)
            layout.addWidget(self.pictograph_component)
        except RuntimeError as e:
            print(f"❌ Failed to create PictographComponent: {e}")
            # Create a fallback label instead
            from PyQt6.QtWidgets import QLabel
            from PyQt6.QtCore import Qt

            fallback_label = QLabel(f"Beat {beat_data.letter}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            self.pictograph_component = None

        self.setStyleSheet(
            """
            ClickablePictographFrame {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 6px;
            }
            ClickablePictographFrame:hover {
                border-color: #007bff;
                background-color: #f8f9fa;
                border-width: 3px;
            }
        """
        )

        # Ensure frame and component are visible
        self.show()
        if self.pictograph_component:
            self.pictograph_component.show()

    def set_container_widget(self, container_widget):
        """Set container widget for dynamic sizing (V1-style, but decoupled)"""
        self.container_widget = container_widget

    def resize_frame(self):
        """Resize frame using V1's dynamic sizing algorithm based on container width"""
        if not self.container_widget:
            return

        try:
            # V1's sizing algorithm adapted for container-based sizing
            container_width = self.container_widget.width()
            if container_width <= 0:
                return  # Container not ready yet

            # V1's algorithm: Calculate size based on desired columns and available width
            desired_columns = 8  # V1 default
            spacing = 8  # Grid spacing
            margin = 20  # Container margins

            # Calculate available width for pictographs
            available_width = container_width - (2 * margin)

            # Calculate size per pictograph: (width - spacing) / columns
            total_spacing = spacing * (desired_columns - 1)
            size_per_pictograph = (available_width - total_spacing) / desired_columns

            # Apply V1's border width calculation
            border_width = max(1, int(size_per_pictograph * 0.015))
            final_size = int(size_per_pictograph - (2 * border_width))

            # Ensure reasonable size bounds
            final_size = max(60, min(final_size, 200))  # Between 60px and 200px

            # Apply the calculated size
            self.setFixedSize(final_size, final_size)

        except Exception as e:
            print(f"❌ Error in resize_frame: {e}")

    def update_beat_data(self, beat_data: BeatData):
        """Update the frame's content with new beat data (V1-style reuse pattern)"""
        self.beat_data = beat_data
        if self.pictograph_component:
            self.pictograph_component.update_from_beat(beat_data)

    def cleanup(self):
        """Cleanup resources to prevent memory leaks"""
        if self.pictograph_component:
            self.pictograph_component.cleanup()
            self.pictograph_component = None

    def closeEvent(self, event):
        """Handle close event to cleanup resources"""
        self.cleanup()
        super().closeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(f"beat_{self.beat_data.letter}")
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)
