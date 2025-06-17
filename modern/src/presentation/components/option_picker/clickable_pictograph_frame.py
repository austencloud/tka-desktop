from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy, QWidget, QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QEvent
from PyQt6.QtGui import QCloseEvent, QMouseEvent, QEnterEvent
from typing import Optional

from domain.models.core_models import BeatData
from presentation.components.pictograph.pictograph_component import PictographComponent


class ClickablePictographFrame(QFrame):
    clicked = pyqtSignal(str)
    beat_data_clicked = pyqtSignal(object)  # New signal that passes the actual BeatData

    def __init__(self, beat_data: BeatData, parent: Optional[QWidget] = None) -> None:
        if parent is not None:
            try:
                _ = parent.isVisible()
            except RuntimeError:
                print(
                    f"❌ Parent widget deleted, cannot create ClickablePictographFrame"
                )
                raise RuntimeError("Parent widget has been deleted")

        super().__init__(parent)
        self.beat_data: BeatData = beat_data
        # CRITICAL FIX: Remove frame's own border styling to prevent double borders
        # The PictographComponent's border manager will handle all border rendering
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setLineWidth(0)

        self.container_widget: Optional[QWidget] = None

        square_size: int = 160
        self.setFixedSize(square_size, square_size)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        try:
            self.pictograph_component: Optional[PictographComponent] = (
                PictographComponent(parent=None)
            )
            self.pictograph_component.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

            self._configure_option_picker_context(beat_data)

            self.pictograph_component.update_from_beat(beat_data)
            layout.addWidget(self.pictograph_component)
        except RuntimeError as e:
            print(f"❌ Failed to create PictographComponent: {e}")

            fallback_label = QLabel(f"Beat {beat_data.letter}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            self.pictograph_component = None

        # CRITICAL FIX: Remove CSS border styling to prevent conflicts with border manager
        # The PictographComponent's border manager handles all border rendering and styling
        self.setStyleSheet(
            """
            ClickablePictographFrame {
                background-color: transparent;
                border: none;
            }
            ClickablePictographFrame:hover {
                background-color: transparent;
            }
        """
        )

        self.show()
        if self.pictograph_component:
            self.pictograph_component.show()

    def _configure_option_picker_context(self, beat_data: BeatData) -> None:
        if not self.pictograph_component:
            return

        try:
            # CRITICAL FIX: Set appropriate scaling context for option picker
            # This prevents the over-scaling issue seen in the option picker
            from application.services.ui.context_aware_scaling_service import (
                ScalingContext,
            )

            self.pictograph_component.set_scaling_context(ScalingContext.OPTION_VIEW)

            # Apply letter type-specific colored borders
            if beat_data.glyph_data and beat_data.glyph_data.letter_type:
                self.pictograph_component.enable_borders()
                self.pictograph_component.update_border_colors_for_letter_type(
                    beat_data.glyph_data.letter_type
                )

            # Configure hover effects for option picker context
            # This is now handled by the pictograph component itself

        except Exception as e:
            print(f"⚠️  Failed to configure Option Picker context: {e}")
            # Fallback: enable borders with letter type colors and set scaling context
            from application.services.ui.context_aware_scaling_service import (
                ScalingContext,
            )

            self.pictograph_component.set_scaling_context(ScalingContext.OPTION_VIEW)
            if beat_data.glyph_data and beat_data.glyph_data.letter_type:
                self.pictograph_component.enable_borders()
                self.pictograph_component.update_border_colors_for_letter_type(
                    beat_data.glyph_data.letter_type
                )

    def set_container_widget(self, container_widget: QWidget) -> None:
        self.container_widget = container_widget

    def resize_frame(self) -> None:
        if not self.container_widget:
            return

        try:
            container_width: int = self.container_widget.width()
            if container_width <= 0:
                return

            desired_columns: int = 8
            spacing: int = 8
            margin: int = 20

            available_width: int = container_width - (2 * margin)

            total_spacing: int = spacing * (desired_columns - 1)
            size_per_pictograph: float = (
                available_width - total_spacing
            ) / desired_columns

            border_width: int = max(1, int(size_per_pictograph * 0.015))
            final_size: int = int(size_per_pictograph - (2 * border_width))

            final_size = max(60, min(final_size, 200))

            self.setFixedSize(final_size, final_size)

        except Exception as e:
            print(f"❌ Error in resize_frame: {e}")

    def update_beat_data(self, beat_data: BeatData) -> None:
        """Update the frame's content with new beat data (Legacy-style reuse pattern)"""
        self.beat_data = beat_data
        if self.pictograph_component:
            # Reconfigure context for new beat data (important for letter type colors)
            self._configure_option_picker_context(beat_data)
            self.pictograph_component.update_from_beat(beat_data)

    def cleanup(self) -> None:
        if self.pictograph_component:
            self.pictograph_component.cleanup()
            self.pictograph_component = None

    def closeEvent(self, event: QCloseEvent) -> None:
        self.cleanup()
        super().closeEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            # Emit both the old signal (for compatibility) and the new signal with actual beat data
            self.clicked.emit(f"beat_{self.beat_data.letter}")
            self.beat_data_clicked.emit(
                self.beat_data
            )  # Pass the actual BeatData object
        super().mousePressEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)
