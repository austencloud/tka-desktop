from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QFrame, QMenu
from PyQt6.QtCore import Qt, QEvent, QTimer
from PyQt6.QtGui import QCursor, QAction, QKeyEvent

from base_widgets.pictograph.managers.pictograph_data_copier import dictCopier


if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class BasePictographView(QGraphicsView):
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        super().__init__(pictograph)
        if pictograph:
            self.pictograph = pictograph
            self.pictograph.elements.view = self

        # Dimension debugging
        self.debug_enabled = False
        self.debug_timer = QTimer()
        self.debug_timer.timeout.connect(self._print_debug_dimensions)
        self.debug_timer.setSingleShot(True)

        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.setContentsMargins(0, 0, 0, 0)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

    ### EVENTS ###

    def resizeEvent(self, event):
        """Handle resizing and maintain aspect ratio."""
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        # Trigger debug print if enabled
        self._trigger_debug_print()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle key press events for debugging."""
        if (
            event.key() == Qt.Key.Key_D
            and event.modifiers() == Qt.KeyboardModifier.ControlModifier
        ):
            self.toggle_dimension_debugging()
        else:
            super().keyPressEvent(event)

    def toggle_dimension_debugging(self) -> None:
        """Toggle dimension debugging on/off."""
        self.debug_enabled = not self.debug_enabled
        if self.debug_enabled:
            print(
                "🔍 Legacy Dimension debugging ENABLED - Press Ctrl+D again to disable"
            )
            self._trigger_debug_print()
        else:
            print("🔍 Legacy Dimension debugging DISABLED")

    def _trigger_debug_print(self) -> None:
        """Trigger debug print after a short delay to ensure rendering is complete."""
        if self.debug_enabled:
            self.debug_timer.start(100)  # 100ms delay

    def _print_debug_dimensions(self) -> None:
        """Print detailed dimension information for debugging."""
        if not self.debug_enabled or not self.pictograph:
            return

        print("\n" + "=" * 80)
        print("🔍 Legacy PICTOGRAPH DIMENSION DEBUG")
        print("=" * 80)

        # Component dimensions
        component_size = self.size()
        viewport_size = self.viewport().size()
        print(f"📐 Component Size: {component_size.width()}x{component_size.height()}")
        print(f"📐 Viewport Size: {viewport_size.width()}x{viewport_size.height()}")

        # Scene dimensions
        scene_rect = self.sceneRect()
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

        # View-specific scaling info
        self._debug_view_specific_scaling()

        # TKA glyph analysis
        self._debug_tka_glyph_dimensions()

        print("=" * 80)
        print()

    def _debug_view_specific_scaling(self) -> None:
        """Debug view-specific scaling calculations."""
        print(f"\n🎯 VIEW TYPE: {self.__class__.__name__}")

        # Check if this view has specific scaling logic
        if hasattr(self, "view_scale"):
            print(f"   View Scale: {self.view_scale:.4f}")

        if hasattr(self, "size_provider"):
            try:
                provider_size = self.size_provider()
                print(
                    f"   Size Provider: {provider_size.width()}x{provider_size.height()}"
                )
            except:
                print("   Size Provider: Error getting size")

    def _debug_tka_glyph_dimensions(self) -> None:
        """Debug TKA glyph specific dimensions."""
        if not self.pictograph or not hasattr(self.pictograph, "elements"):
            return

        print("\n🔤 TKA GLYPH ANALYSIS:")

        # Check if TKA glyph exists
        if (
            hasattr(self.pictograph.elements, "tka_glyph")
            and self.pictograph.elements.tka_glyph
        ):
            tka_glyph = self.pictograph.elements.tka_glyph

            # Group dimensions
            group_rect = tka_glyph.boundingRect()
            group_pos = tka_glyph.pos()
            print(
                f"   TKA Group Rect: {group_rect.width():.1f}x{group_rect.height():.1f}"
            )
            print(f"   TKA Group Pos: ({group_pos.x():.1f}, {group_pos.y():.1f})")

            # Letter dimensions if available
            if hasattr(tka_glyph, "letter_item") and tka_glyph.letter_item:
                letter_item = tka_glyph.letter_item
                letter_rect = letter_item.boundingRect()
                letter_pos = letter_item.pos()
                print(
                    f"   Letter Rect: {letter_rect.width():.1f}x{letter_rect.height():.1f}"
                )
                print(f"   Letter Pos: ({letter_pos.x():.1f}, {letter_pos.y():.1f})")

                # Scene coordinates
                scene_rect = tka_glyph.sceneBoundingRect()
                print(
                    f"   Scene Rect: {scene_rect.width():.1f}x{scene_rect.height():.1f} at ({scene_rect.x():.1f}, {scene_rect.y():.1f})"
                )

                # Effective size after view scaling
                transform = self.transform()
                effective_width = scene_rect.width() * transform.m11()
                effective_height = scene_rect.height() * transform.m22()
                print(
                    f"   Effective Size: {effective_width:.1f}x{effective_height:.1f}"
                )
        else:
            print("   No TKA glyph found")

    def contextMenuEvent(self, event: QEvent) -> None:
        context_menu = QMenu(self)
        copy_action = QAction("Copy Dictionary", self)
        copy_action.triggered.connect(
            self.pictograph.managers.data_copier.copy_pictograph_data
        )
        context_menu.addAction(copy_action)
        context_menu.exec(QCursor.pos())
