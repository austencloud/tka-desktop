# src/main_window/main_widget/sequence_card_tab/components/display/lazy_loader.py
import logging
from typing import Dict, Set, Optional, Callable, Any
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget, QScrollArea
from PyQt6.QtGui import QPixmap


class LazyImageLoader(QObject):
    """
    Lazy loading system that only loads images when they become visible.

    Features:
    - Viewport-based loading (only load what's visible)
    - Placeholder images for non-loaded content
    - Automatic loading when scrolling
    - Configurable loading buffer (load slightly ahead)
    - Memory-efficient unloading of off-screen images
    """

    # Signals
    image_loaded = pyqtSignal(str, QPixmap)  # path, pixmap
    loading_started = pyqtSignal(str)  # path
    loading_completed = pyqtSignal()

    def __init__(
        self, scroll_area: QScrollArea, image_processor, buffer_pixels: int = 200
    ):
        """
        Initialize the lazy loader.

        Args:
            scroll_area: The scroll area to monitor for visibility
            image_processor: ImageProcessor instance for loading images
            buffer_pixels: Extra pixels to load outside viewport
        """
        super().__init__()

        self.scroll_area = scroll_area
        self.image_processor = image_processor
        self.buffer_pixels = buffer_pixels

        # Track image states
        self.pending_images: Dict[str, Dict[str, Any]] = {}  # path -> load_params
        self.loaded_images: Set[str] = set()
        self.loading_images: Set[str] = set()
        self.visible_images: Set[str] = set()

        # Placeholder pixmap for unloaded images
        self.placeholder_pixmap: Optional[QPixmap] = None
        self._create_placeholder()

        # Timer for debounced loading
        self.load_timer = QTimer()
        self.load_timer.setSingleShot(True)
        self.load_timer.timeout.connect(self._process_visible_images)
        self.load_delay_ms = 100  # Delay before loading after scroll stops

        # Connect scroll events
        if self.scroll_area and self.scroll_area.verticalScrollBar():
            self.scroll_area.verticalScrollBar().valueChanged.connect(self._on_scroll)

        # Statistics
        self.images_loaded_lazily = 0
        self.images_unloaded = 0
        self.placeholder_requests = 0

        logging.info("Lazy image loader initialized")

    def _create_placeholder(self) -> None:
        """Create a placeholder pixmap for unloaded images."""
        try:
            from PyQt6.QtGui import QPainter, QColor, QFont
            from PyQt6.QtCore import Qt, QSize

            size = QSize(200, 150)
            self.placeholder_pixmap = QPixmap(size)
            self.placeholder_pixmap.fill(QColor(240, 240, 240))

            painter = QPainter(self.placeholder_pixmap)
            painter.setPen(QColor(180, 180, 180))
            painter.setFont(QFont("Arial", 12))

            # Draw loading text
            text_rect = self.placeholder_pixmap.rect()
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, "Loading...")

            # Draw border
            painter.drawRect(self.placeholder_pixmap.rect().adjusted(0, 0, -1, -1))
            painter.end()

        except Exception as e:
            logging.warning(f"Failed to create placeholder pixmap: {e}")
            self.placeholder_pixmap = QPixmap(200, 150)
            self.placeholder_pixmap.fill(QColor(240, 240, 240))

    def register_image(
        self, image_path: str, widget: QWidget, load_callback: Callable, **load_params
    ) -> QPixmap:
        """
        Register an image for lazy loading.

        Args:
            image_path: Path to the image file
            widget: Widget that will display the image (for visibility checking)
            load_callback: Function to call when image is loaded
            **load_params: Parameters to pass to the image processor

        Returns:
            Placeholder pixmap to display immediately
        """
        # Store loading parameters
        self.pending_images[image_path] = {
            "widget": widget,
            "callback": load_callback,
            "load_params": load_params,
        }

        self.placeholder_requests += 1

        # Check if image should be loaded immediately (if visible)
        if self._is_widget_visible(widget):
            self._schedule_loading()

        return self.placeholder_pixmap or QPixmap(200, 150)

    def _is_widget_visible(self, widget: QWidget) -> bool:
        """Check if a widget is visible in the scroll area viewport."""
        if not widget or not self.scroll_area:
            return False

        try:
            # Get widget position relative to scroll area
            widget_pos = widget.mapTo(self.scroll_area.widget(), widget.pos())
            widget_rect = widget.geometry()
            widget_rect.moveTo(widget_pos)

            # Get visible viewport with buffer
            viewport_rect = self.scroll_area.viewport().rect()
            scroll_pos = self.scroll_area.verticalScrollBar().value()

            # Adjust viewport for scroll position and add buffer
            visible_rect = viewport_rect.translated(0, scroll_pos)
            visible_rect.adjust(
                -self.buffer_pixels,
                -self.buffer_pixels,
                self.buffer_pixels,
                self.buffer_pixels,
            )

            return visible_rect.intersects(widget_rect)

        except Exception as e:
            logging.debug(f"Error checking widget visibility: {e}")
            return True  # Default to visible if we can't determine

    def _on_scroll(self) -> None:
        """Handle scroll events with debouncing."""
        if self.load_timer.isActive():
            self.load_timer.stop()
        self.load_timer.start(self.load_delay_ms)

    def _schedule_loading(self) -> None:
        """Schedule loading of visible images."""
        if self.load_timer.isActive():
            self.load_timer.stop()
        self.load_timer.start(self.load_delay_ms)

    def _process_visible_images(self) -> None:
        """Process and load visible images."""
        try:
            newly_visible = set()

            # Check which images are now visible
            for image_path, params in self.pending_images.items():
                widget = params["widget"]

                if self._is_widget_visible(widget):
                    newly_visible.add(image_path)
                    if image_path not in self.visible_images:
                        self.visible_images.add(image_path)

            # Load newly visible images
            for image_path in newly_visible:
                if (
                    image_path not in self.loaded_images
                    and image_path not in self.loading_images
                ):
                    self._load_image(image_path)

            # Unload images that are no longer visible (optional memory optimization)
            self._unload_invisible_images()

        except Exception as e:
            logging.warning(f"Error processing visible images: {e}")

    def _load_image(self, image_path: str) -> None:
        """Load a specific image."""
        if image_path not in self.pending_images:
            return

        try:
            self.loading_images.add(image_path)
            self.loading_started.emit(image_path)

            params = self.pending_images[image_path]
            load_params = params["load_params"]
            callback = params["callback"]

            # Load the image using the image processor
            pixmap = self.image_processor.load_image_with_consistent_scaling(
                image_path, **load_params
            )

            if pixmap and not pixmap.isNull():
                self.loaded_images.add(image_path)
                self.images_loaded_lazily += 1

                # Call the callback to update the UI
                if callback:
                    callback(image_path, pixmap)

                # Emit signal
                self.image_loaded.emit(image_path, pixmap)

                logging.debug(f"Lazy loaded image: {image_path}")

            # Remove from pending and loading
            if image_path in self.pending_images:
                del self.pending_images[image_path]

        except Exception as e:
            logging.warning(f"Error loading image {image_path}: {e}")

        finally:
            self.loading_images.discard(image_path)

            # Check if all loading is complete
            if not self.loading_images:
                self.loading_completed.emit()

    def _unload_invisible_images(self) -> None:
        """Unload images that are no longer visible to save memory."""
        try:
            # Find images that are no longer visible
            invisible_images = set()

            for image_path in self.visible_images.copy():
                if image_path in self.pending_images:
                    widget = self.pending_images[image_path]["widget"]
                    if not self._is_widget_visible(widget):
                        invisible_images.add(image_path)

            # Remove from visible set
            for image_path in invisible_images:
                self.visible_images.discard(image_path)
                self.images_unloaded += 1

                logging.debug(f"Unloaded invisible image: {image_path}")

        except Exception as e:
            logging.debug(f"Error unloading invisible images: {e}")

    def force_load_all(self) -> None:
        """Force load all pending images (useful for export operations)."""
        try:
            for image_path in list(self.pending_images.keys()):
                if (
                    image_path not in self.loaded_images
                    and image_path not in self.loading_images
                ):
                    self._load_image(image_path)

        except Exception as e:
            logging.warning(f"Error force loading all images: {e}")

    def clear(self) -> None:
        """Clear all pending and loaded images."""
        self.pending_images.clear()
        self.loaded_images.clear()
        self.loading_images.clear()
        self.visible_images.clear()

        if self.load_timer.isActive():
            self.load_timer.stop()

    def get_stats(self) -> Dict[str, Any]:
        """Get lazy loading statistics."""
        return {
            "pending_images": len(self.pending_images),
            "loaded_images": len(self.loaded_images),
            "loading_images": len(self.loading_images),
            "visible_images": len(self.visible_images),
            "images_loaded_lazily": self.images_loaded_lazily,
            "images_unloaded": self.images_unloaded,
            "placeholder_requests": self.placeholder_requests,
            "buffer_pixels": self.buffer_pixels,
        }
