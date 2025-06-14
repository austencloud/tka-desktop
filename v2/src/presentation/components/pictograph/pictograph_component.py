"""
Direct pictograph view for Kinetic Constructor v2 - matches v1 container hierarchy.
"""

from typing import Optional
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import pyqtSignal, Qt, QTimer, QSize, QEvent
from PyQt6.QtGui import QPainter, QKeyEvent

from domain.models.core_models import BeatData

from .pictograph_scene import PictographScene
from application.services.context_aware_scaling_service import (
    ContextAwareScalingService,
    ScalingContext,
)
from .border_manager import BorderedPictographMixin


class PictographComponent(QGraphicsView, BorderedPictographMixin):
    pictograph_updated = pyqtSignal(object)

    def __init__(self, parent: Optional[QGraphicsView] = None):
        if parent is not None:
            try:
                _ = parent.isVisible()
            except RuntimeError:
                print(f"❌ Parent widget deleted, cannot create PictographComponent")
                raise RuntimeError("Parent widget has been deleted")

        super().__init__(parent)
        BorderedPictographMixin.__init__(self)

        self.current_beat: Optional[BeatData] = None
        self.scene: Optional[PictographScene] = None

        # Context-aware scaling
        self.scaling_service = ContextAwareScalingService()
        self.scaling_context = ScalingContext.DEFAULT
        self.context_params = {}

        # Dimension debugging
        self.debug_enabled = False
        self.debug_timer = QTimer()
        self.debug_timer.timeout.connect(self._print_debug_dimensions)
        self.debug_timer.setSingleShot(True)

        self._setup_ui()

    def _setup_ui(self) -> None:
        try:
            self.scene = PictographScene(parent=self)
            self.setScene(self.scene)

            self.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setFrameStyle(0)

            self.setContentsMargins(0, 0, 0, 0)
            viewport = self.viewport()
            if viewport:
                viewport.setContentsMargins(0, 0, 0, 0)
            self.setViewportMargins(0, 0, 0, 0)
            self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

            self._fit_view()
        except RuntimeError as e:
            print(f"❌ Failed to setup PictographComponent UI: {e}")

    def update_from_beat(self, beat_data: BeatData) -> None:
        self.current_beat = beat_data
        if self.scene:
            self.scene.update_beat(beat_data)
            self._fit_view()
        self.pictograph_updated.emit(beat_data)

    def get_current_beat(self) -> Optional[BeatData]:
        return self.current_beat

    def clear_pictograph(self) -> None:
        self.current_beat = None
        if self.scene:
            self.scene.clear()

    def cleanup(self) -> None:
        try:
            if self.scene:
                self.scene.clear()
                self.scene.setParent(None)
                self.scene = None
        except RuntimeError:
            pass

    def _fit_view(self) -> None:
        if self.scene:
            try:
                self.resetTransform()

                scene_size = QSize(950, 950)
                view_size = self.size()

                # CRITICAL FIX: Account for border space when borders are enabled
                # This prevents borders from cutting off pictograph content
                effective_view_size = view_size
                if self.border_manager.show_borders:
                    # Calculate exact border space usage matching the debug calculation
                    viewport_width = view_size.width()
                    outer_border_width = max(1.0, viewport_width * 0.016)
                    inner_border_width = max(1.0, viewport_width * 0.016)

                    # Calculate exact border inset as per debug output:
                    # Total Border Inset = half_outer_pen + outer_border_width + half_inner_pen + inner_border_width
                    half_outer_pen = outer_border_width / 2.0
                    half_inner_pen = inner_border_width / 2.0
                    total_border_inset = (
                        half_outer_pen
                        + outer_border_width
                        + half_inner_pen
                        + inner_border_width
                    )

                    # Apply border inset to both sides (left+right, top+bottom)
                    border_space = total_border_inset * 2

                    # Reduce effective view size to account for border space
                    border_adjusted_width = max(100, view_size.width() - border_space)
                    border_adjusted_height = max(100, view_size.height() - border_space)
                    effective_view_size = QSize(
                        int(border_adjusted_width), int(border_adjusted_height)
                    )

                # Use context-aware scaling service with border-adjusted size
                scale_x, scale_y = self.scaling_service.calculate_context_scale(
                    context=self.scaling_context,
                    container_size=effective_view_size,  # Use border-adjusted size
                    scene_size=scene_size,
                    parent_widget=self.parent(),
                    **self.context_params,
                )

                self.scale(scale_x, scale_y)
                self.centerOn(self.scene.CENTER_X, self.scene.CENTER_Y)
            except RuntimeError:
                pass

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._fit_view()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._fit_view()

    def paintEvent(self, event) -> None:
        """Handle paint events and draw borders if enabled."""
        super().paintEvent(event)

        # Draw borders using the border manager
        painter = QPainter(self.viewport())
        try:
            self.draw_pictograph_borders(
                painter, self.viewport().rect(), self.viewport().size().width()
            )
        finally:
            painter.end()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle key press events for debugging."""
        if (
            event.key() == Qt.Key.Key_D
            and event.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            self.toggle_dimension_debugging()
        else:
            super().keyPressEvent(event)

    def enterEvent(self, event: QEvent) -> None:
        """Handle mouse enter events for hover effects."""
        super().enterEvent(event)
        # Default hover behavior - can be overridden by context configurator
        if hasattr(self, "_hover_enter_func"):
            self._hover_enter_func()

    def leaveEvent(self, event: QEvent) -> None:
        """Handle mouse leave events for hover effects."""
        super().leaveEvent(event)
        # Default hover behavior - can be overridden by context configurator
        if hasattr(self, "_hover_leave_func"):
            self._hover_leave_func()

    def toggle_dimension_debugging(self) -> None:
        """Toggle dimension debugging on/off."""
        self.debug_enabled = not self.debug_enabled
        if self.debug_enabled:
            print("🔍 V2 Dimension debugging ENABLED - Press Ctrl+D again to disable")
            self._trigger_debug_print()
        else:
            print("🔍 V2 Dimension debugging DISABLED")

    def _trigger_debug_print(self) -> None:
        """Trigger debug print after a short delay to ensure rendering is complete."""
        if self.debug_enabled:
            self.debug_timer.start(100)  # 100ms delay

    def _print_debug_dimensions(self) -> None:
        """Print detailed dimension information for debugging."""
        if not self.debug_enabled or not self.scene:
            return

        print("\n" + "=" * 80)
        print("🔍 V2 PICTOGRAPH DIMENSION DEBUG")
        print("=" * 80)

        # Component dimensions
        component_size = self.size()
        viewport_size = self.viewport().size()
        print(f"📐 Component Size: {component_size.width()}x{component_size.height()}")
        print(f"📐 Viewport Size: {viewport_size.width()}x{viewport_size.height()}")

        # Scene dimensions
        scene_rect = self.scene.sceneRect()
        print(
            f"📐 Scene Rect: {scene_rect.width()}x{scene_rect.height()} at ({scene_rect.x()}, {scene_rect.y()})"
        )

        # View scaling
        transform = self.transform()
        scale_x = transform.m11()
        scale_y = transform.m22()
        print(f"📐 View Scale: {scale_x:.4f}x{scale_y:.4f}")

        # Calculate effective pictograph size
        effective_width = scene_rect.width() * scale_x
        effective_height = scene_rect.height() * scale_y
        print(
            f"📐 Effective Pictograph Size: {effective_width:.1f}x{effective_height:.1f}"
        )

        # TKA glyph analysis
        self._debug_tka_glyph_dimensions()

        print("=" * 80)
        print()

    def _debug_tka_glyph_dimensions(self) -> None:
        """Debug TKA glyph specific dimensions."""
        if not self.scene:
            return

        print("\n🔤 TKA GLYPH ANALYSIS:")

        # Find TKA glyph items in the scene
        tka_items = []
        for item in self.scene.items():
            if hasattr(item, "childItems") and item.childItems():
                # Check if this looks like a TKA group
                children = item.childItems()
                if len(children) > 0:
                    first_child = children[0]
                    if hasattr(first_child, "boundingRect"):
                        tka_items.append((item, first_child))

        if not tka_items:
            print("   No TKA glyph items found")
            return

        for i, (group_item, letter_item) in enumerate(tka_items):
            print(f"   TKA Group {i+1}:")

            # Group dimensions
            group_rect = group_item.boundingRect()
            group_pos = group_item.pos()
            print(
                f"     Group Rect: {group_rect.width():.1f}x{group_rect.height():.1f}"
            )
            print(f"     Group Pos: ({group_pos.x():.1f}, {group_pos.y():.1f})")

            # Letter dimensions
            letter_rect = letter_item.boundingRect()
            letter_pos = letter_item.pos()
            print(
                f"     Letter Rect: {letter_rect.width():.1f}x{letter_rect.height():.1f}"
            )
            print(f"     Letter Pos: ({letter_pos.x():.1f}, {letter_pos.y():.1f})")

            # Scene coordinates
            scene_rect = group_item.sceneBoundingRect()
            print(
                f"     Scene Rect: {scene_rect.width():.1f}x{scene_rect.height():.1f} at ({scene_rect.x():.1f}, {scene_rect.y():.1f})"
            )

            # Effective size after view scaling
            transform = self.transform()
            effective_width = scene_rect.width() * transform.m11()
            effective_height = scene_rect.height() * transform.m22()
            print(f"     Effective Size: {effective_width:.1f}x{effective_height:.1f}")

    def set_scaling_context(self, context: ScalingContext, **context_params) -> None:
        """Set the scaling context and parameters for context-aware scaling."""
        self.scaling_context = context
        self.context_params = context_params
        # Re-apply scaling with new context
        self._fit_view()

    def get_scaling_context(self) -> ScalingContext:
        """Get the current scaling context."""
        return self.scaling_context

    def update_from_beat(self, beat_data: BeatData) -> None:
        self.current_beat = beat_data
        if self.scene:
            self.scene.update_beat(beat_data)
            self._fit_view()
            # Trigger debug print if enabled
            self._trigger_debug_print()
        self.pictograph_updated.emit(beat_data)
