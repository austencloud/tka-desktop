from PyQt6.QtCore import Qt, QRect, QSize, QTimer
from PyQt6.QtGui import QPixmap, QCursor, QMouseEvent, QPainter, QColor, QPen, QImage
from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING, Optional, Final
import logging
import os

from data.constants import GOLD, BLUE
from main_window.main_widget.metadata_extractor import MetaDataExtractor
from main_window.main_widget.browse_tab.cache import BrowseThumbnailCache

# PIL/Pillow imports for superior image processing
try:
    from PIL import Image as PILImage, ImageFilter, ImageEnhance

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL/Pillow not available - using Qt-only scaling")

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox


class UltraHighQualityImageProcessor:
    """
    Ultra high-quality image processor for razor-sharp thumbnails.

    Features:
    - PIL/Pillow-based scaling with Lanczos resampling
    - Multi-stage scaling for optimal quality
    - Post-processing sharpening and enhancement
    - Professional-grade quality optimization
    - Smart scaling threshold detection
    """

    @staticmethod
    def process_image_to_ultra_quality(
        source_path: str,
        target_size: QSize,
        enable_sharpening: bool = True,
        enable_enhancement: bool = True,
    ) -> QPixmap:
        """
        Process image to ultra high quality using advanced techniques.

        Args:
            source_path: Path to source image
            target_size: Target size for thumbnail
            enable_sharpening: Apply sharpening filter
            enable_enhancement: Apply contrast/brightness enhancement

        Returns:
            Ultra high-quality QPixmap
        """
        if not PIL_AVAILABLE:
            return UltraHighQualityImageProcessor._fallback_qt_processing(
                source_path, target_size
            )

        try:
            # Load image with PIL for superior processing
            pil_image = PILImage.open(source_path)

            # Convert to RGB if necessary
            if pil_image.mode not in ("RGB", "RGBA"):
                pil_image = pil_image.convert("RGB")

            original_size = pil_image.size
            target_w, target_h = target_size.width(), target_size.height()

            # Calculate aspect ratio preserving dimensions
            aspect_ratio = original_size[0] / original_size[1]
            if target_w / target_h > aspect_ratio:
                # Height is the limiting factor
                new_h = target_h
                new_w = int(target_h * aspect_ratio)
            else:
                # Width is the limiting factor
                new_w = target_w
                new_h = int(target_w / aspect_ratio)

            # ULTRA QUALITY SCALING STRATEGY
            scale_factor = min(new_w / original_size[0], new_h / original_size[1])

            if scale_factor < 0.75:
                # Multi-stage scaling for maximum quality when downscaling significantly
                processed_image = UltraHighQualityImageProcessor._multi_stage_scaling(
                    pil_image, (new_w, new_h), scale_factor
                )
            else:
                # Single-stage high-quality scaling
                processed_image = pil_image.resize(
                    (new_w, new_h), PILImage.Resampling.LANCZOS  # Superior to bicubic
                )

            # POST-PROCESSING FOR RAZOR SHARPNESS
            if enable_enhancement:
                processed_image = UltraHighQualityImageProcessor._enhance_image_quality(
                    processed_image
                )

            if enable_sharpening:
                processed_image = UltraHighQualityImageProcessor._apply_sharpening(
                    processed_image, scale_factor
                )

            # Convert back to QPixmap
            return UltraHighQualityImageProcessor._pil_to_qpixmap(processed_image)

        except Exception as e:
            logging.warning(f"PIL processing failed for {source_path}: {e}")
            return UltraHighQualityImageProcessor._fallback_qt_processing(
                source_path, target_size
            )

    @staticmethod
    def _multi_stage_scaling(
        pil_image: "PILImage.Image", target_size: tuple, scale_factor: float
    ) -> "PILImage.Image":
        """
        Multi-stage scaling for optimal quality when downscaling significantly.
        """
        current_image = pil_image
        current_size = pil_image.size
        target_w, target_h = target_size

        # Define scaling stages based on scale factor
        if scale_factor < 0.25:
            # Very aggressive downscaling - use 3 stages
            stages = [0.6, 0.35, 1.0]  # Final stage scales to exact target
        elif scale_factor < 0.5:
            # Moderate downscaling - use 2 stages
            stages = [0.7, 1.0]
        else:
            # Single stage for less aggressive scaling
            stages = [1.0]

        for i, stage_factor in enumerate(stages):
            if i == len(stages) - 1:
                # Final stage - scale to exact target size
                intermediate_size = (target_w, target_h)
            else:
                # Intermediate stage
                intermediate_w = int(current_size[0] * stage_factor)
                intermediate_h = int(current_size[1] * stage_factor)
                intermediate_size = (intermediate_w, intermediate_h)

            current_image = current_image.resize(
                intermediate_size, PILImage.Resampling.LANCZOS
            )
            current_size = intermediate_size

            logging.debug(f"Scaling stage {i+1}: {current_size}")

        return current_image

    @staticmethod
    def _enhance_image_quality(pil_image: "PILImage.Image") -> "PILImage.Image":
        """
        Apply quality enhancements for better visual appearance.
        """
        # Subtle contrast enhancement for better definition
        contrast_enhancer = ImageEnhance.Contrast(pil_image)
        enhanced_image = contrast_enhancer.enhance(1.05)  # 5% contrast boost

        # Slight brightness adjustment for better visibility
        brightness_enhancer = ImageEnhance.Brightness(enhanced_image)
        enhanced_image = brightness_enhancer.enhance(1.02)  # 2% brightness boost

        # Color saturation for more vibrant images
        color_enhancer = ImageEnhance.Color(enhanced_image)
        enhanced_image = color_enhancer.enhance(1.03)  # 3% saturation boost

        return enhanced_image

    @staticmethod
    def _apply_sharpening(
        pil_image: "PILImage.Image", scale_factor: float
    ) -> "PILImage.Image":
        """
        Apply intelligent sharpening based on scale factor.
        """
        # Determine sharpening intensity based on how much we scaled down
        if scale_factor < 0.3:
            # Heavy downscaling needs more aggressive sharpening
            sharpening_filter = ImageFilter.UnsharpMask(
                radius=1.2,  # Larger radius for more comprehensive sharpening
                percent=120,  # Higher percentage for stronger effect
                threshold=1,  # Lower threshold to affect more pixels
            )
        elif scale_factor < 0.6:
            # Moderate downscaling needs moderate sharpening
            sharpening_filter = ImageFilter.UnsharpMask(
                radius=0.8, percent=100, threshold=2
            )
        else:
            # Light scaling needs subtle sharpening
            sharpening_filter = ImageFilter.UnsharpMask(
                radius=0.5, percent=80, threshold=3
            )

        # Apply the sharpening filter
        sharpened_image = pil_image.filter(sharpening_filter)

        # Additional edge enhancement for very small images
        if min(pil_image.size) < 150:
            edge_enhance_filter = ImageFilter.EDGE_ENHANCE_MORE
            sharpened_image = sharpened_image.filter(edge_enhance_filter)

        return sharpened_image

    @staticmethod
    def _pil_to_qpixmap(pil_image: "PILImage.Image") -> QPixmap:
        """
        Convert PIL Image to QPixmap with optimal quality.
        """
        # Convert to RGB if not already
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        # Convert to bytes
        import io

        byte_array = io.BytesIO()
        pil_image.save(byte_array, format="PNG", optimize=True)
        byte_array.seek(0)

        # Create QPixmap from bytes
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array.getvalue())

        return pixmap

    @staticmethod
    def _fallback_qt_processing(source_path: str, target_size: QSize) -> QPixmap:
        """
        Fallback processing using Qt when PIL is not available.
        Enhanced Qt-only processing with multi-step scaling.
        """
        try:
            # Load original image
            original_pixmap = QPixmap(source_path)
            if original_pixmap.isNull():
                logging.error(f"Failed to load image: {source_path}")
                return UltraHighQualityImageProcessor._create_error_pixmap(target_size)

            # Calculate target dimensions maintaining aspect ratio
            original_size = original_pixmap.size()
            aspect_ratio = original_size.width() / original_size.height()

            if target_size.width() / target_size.height() > aspect_ratio:
                new_h = target_size.height()
                new_w = int(target_size.height() * aspect_ratio)
            else:
                new_w = target_size.width()
                new_h = int(target_size.width() / aspect_ratio)

            target_w, target_h = new_w, new_h
            scale_factor = min(
                target_w / original_size.width(), target_h / original_size.height()
            )

            # Enhanced multi-step scaling with Qt
            if scale_factor < 0.6:  # Lower threshold than before
                # Multi-step scaling
                intermediate_factor = 0.75 if scale_factor < 0.4 else 0.8
                intermediate_w = int(original_size.width() * intermediate_factor)
                intermediate_h = int(original_size.height() * intermediate_factor)

                # Step 1: Scale to intermediate size
                intermediate_pixmap = original_pixmap.scaled(
                    intermediate_w,
                    intermediate_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                # Step 2: Scale to final size
                final_pixmap = intermediate_pixmap.scaled(
                    target_w,
                    target_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            else:
                # Single-step high-quality scaling
                final_pixmap = original_pixmap.scaled(
                    target_w,
                    target_h,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

            return final_pixmap

        except Exception as e:
            logging.error(f"Qt fallback processing failed for {source_path}: {e}")
            return UltraHighQualityImageProcessor._create_error_pixmap(target_size)

    @staticmethod
    def _create_error_pixmap(size: QSize) -> QPixmap:
        """Create error pixmap when image processing fails."""
        pixmap = QPixmap(size)
        pixmap.fill(QColor(200, 200, 200))

        painter = QPainter(pixmap)
        painter.setPen(QColor(100, 100, 100))
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "Image\nError")
        painter.end()

        return pixmap


class ThumbnailImageLabel(QLabel):
    BORDER_WIDTH_RATIO: Final = 0.01
    SEQUENCE_VIEWER_BORDER_SCALE: Final = 0.8

    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__()
        # Instance attributes
        self.thumbnail_box = thumbnail_box
        self.metadata_extractor = MetaDataExtractor()
        self.selected = False
        self.current_path: Optional[str] = None

        # Private attributes
        self._border_width = 4
        self._border_color: Optional[str] = None
        self._original_pixmap: Optional[QPixmap] = None
        self._cached_available_size: Optional[QSize] = None

        # Ultra quality processor
        self.ultra_processor = UltraHighQualityImageProcessor()

        # Deferred loading to prevent UI blocking
        self._load_timer = QTimer()
        self._load_timer.setSingleShot(True)
        self._load_timer.timeout.connect(self._load_pending_image)
        self._pending_path: Optional[str] = None
        self._pending_index: Optional[int] = None

        # Quality enhancement timer
        self._quality_timer = QTimer()
        self._quality_timer.setSingleShot(True)
        self._quality_timer.timeout.connect(self._enhance_image_quality)
        self._needs_quality_enhancement = False

        # Cache integration with ultra quality
        self._cache: Optional[BrowseThumbnailCache] = None
        self._word: Optional[str] = None
        self._variation: int = 0

        # Setup UI
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Initialize cache
        self._initialize_cache()

    @property
    def border_width(self) -> int:
        return self._border_width

    @property
    def is_in_sequence_viewer(self) -> bool:
        return self.thumbnail_box.in_sequence_viewer

    @property
    def aspect_ratio(self) -> float:
        """Get aspect ratio of the original image"""
        return (
            self._original_pixmap.width() / self._original_pixmap.height()
            if self._original_pixmap and self._original_pixmap.height() > 0
            else 1
        )

    def update_thumbnail(self, index: int) -> None:
        """Update the displayed image based on the given index (synchronous)."""
        thumbnails = self.thumbnail_box.state.thumbnails
        if not thumbnails or not (0 <= index < len(thumbnails)):
            return

        path = thumbnails[index]
        if path != self.current_path:
            self.current_path = path
            self._original_pixmap = QPixmap(path)
            self._cached_available_size = None

        self._resize_pixmap_to_ultra_quality()

    def update_thumbnail_async(self, index: int) -> None:
        """Update the displayed image asynchronously with ultra quality processing."""
        thumbnails = self.thumbnail_box.state.thumbnails
        if not thumbnails or not (0 <= index < len(thumbnails)):
            return

        path = thumbnails[index]
        if path != self.current_path:
            self._pending_path = path
            self._pending_index = index

            # Check ultra quality cache first
            if self._cache and self._word is not None:
                available_size = self._calculate_available_space()
                cached_pixmap = self._cache.get_cached_thumbnail(
                    path, available_size, self._word, index
                )

                if cached_pixmap and not cached_pixmap.isNull():
                    # Use cached ultra quality image
                    self.current_path = path
                    self._original_pixmap = QPixmap(path)
                    self._cached_available_size = None
                    self.setFixedSize(available_size)
                    self.setPixmap(cached_pixmap)

                    logging.debug(f"⚡ ULTRA QUALITY cache hit: {self._word}_{index}")
                    return

            # Load with ultra quality processing
            self._load_timer.start(1)
        else:
            self._resize_pixmap_to_ultra_quality()

    def _load_pending_image(self) -> None:
        """Load pending image with ultra quality processing."""
        if self._pending_path and self._pending_index is not None:
            try:
                # Check cache first
                cached_pixmap = None
                if self._cache and self._word is not None:
                    available_size = self._calculate_available_space()
                    cached_pixmap = self._cache.get_cached_thumbnail(
                        self._pending_path, available_size, self._word, self._variation
                    )

                if cached_pixmap and not cached_pixmap.isNull():
                    # Use cached ultra quality image
                    self.current_path = self._pending_path
                    self._original_pixmap = QPixmap(self._pending_path)
                    self._cached_available_size = None

                    available_size = self._calculate_available_space()
                    self.setFixedSize(available_size)
                    self.setPixmap(cached_pixmap)

                    logging.debug(
                        f"✅ Using cached ULTRA QUALITY image for {self._word}_{self._variation}"
                    )
                else:
                    # Process with ultra quality
                    if os.path.exists(self._pending_path):
                        self.current_path = self._pending_path
                        self._original_pixmap = QPixmap(self._pending_path)
                        self._cached_available_size = None

                        # Get quality settings from browse settings
                        quality_settings = self._get_quality_settings()

                        if quality_settings["ultra_quality_enabled"]:
                            # ULTRA QUALITY PROCESSING
                            self._resize_pixmap_to_ultra_quality()
                        else:
                            # Standard quality processing
                            self._resize_pixmap_to_fit_smooth()

            except Exception as e:
                logging.error(f"Error in ultra quality loading: {e}")
            finally:
                self._pending_path = None
                self._pending_index = None

    def _calculate_available_space(self) -> QSize:
        """Calculate available space - ENHANCED FOR MAXIMUM QUALITY."""
        if self._cached_available_size:
            return self._cached_available_size

        if self.is_in_sequence_viewer:
            available_size = self._calculate_sequence_viewer_size()
        else:
            available_size = self._calculate_normal_view_size_enhanced()

        self._cached_available_size = available_size
        return available_size

    def _calculate_normal_view_size_enhanced(self) -> QSize:
        """Enhanced calculation for maximum quality thumbnails."""
        scroll_widget = self.thumbnail_box.sequence_picker.scroll_widget
        scroll_widget_width = scroll_widget.width()

        # Account for scrollbar and margins
        scrollbar_width = scroll_widget.calculate_scrollbar_width()

        # ULTRA QUALITY: Maximize thumbnail size for crisp display
        total_margins = (3 * self.thumbnail_box.margin * 2) + 5
        usable_width = scroll_widget_width - scrollbar_width - total_margins

        # Calculate thumbnail width (3 columns)
        thumbnail_width = max(200, int(usable_width // 3))  # Increased from 150 to 200

        # ULTRA QUALITY: Use maximum available space (minimal padding)
        available_width = int(thumbnail_width - 8)  # Minimal padding
        available_width = max(
            180, available_width
        )  # Increased from 140 to 180 for better quality

        # Calculate height based on aspect ratio
        available_height = int(available_width / self.aspect_ratio)

        # ULTRA QUALITY: Ensure minimum size for crisp display
        available_height = max(135, available_height)  # Increased from 100 to 135

        return QSize(available_width, available_height)

    def _calculate_sequence_viewer_size(self) -> QSize:
        """Calculate available space in sequence viewer mode."""
        sequence_viewer = self.thumbnail_box.browse_tab.sequence_viewer

        try:
            available_width = int(sequence_viewer.width() * 0.95)
            available_height = int(sequence_viewer.height() * 0.65)

            # ULTRA QUALITY: Higher minimums for sequence viewer
            available_width = max(400, available_width)
            available_height = max(300, available_height)

        except (AttributeError, TypeError):
            available_width = 500  # Higher fallback
            available_height = 400

        return QSize(available_width, available_height)

    def _resize_pixmap_to_ultra_quality(self) -> None:
        """Resize pixmap using ULTRA QUALITY processing with user settings."""
        if not self.current_path:
            return

        available_size = self._calculate_available_space()
        quality_settings = self._get_quality_settings()

        # ULTRA QUALITY PROCESSING with user preferences
        ultra_quality_pixmap = self.ultra_processor.process_image_to_ultra_quality(
            self.current_path,
            available_size,
            enable_sharpening=quality_settings["sharpening_enabled"],
            enable_enhancement=quality_settings["enhancement_enabled"],
        )

        # CRITICAL: Ensure pixmap is not null before proceeding
        if ultra_quality_pixmap.isNull():
            logging.warning(
                f"Failed to create ultra quality pixmap for {self.current_path}"
            )
            # Fallback to standard processing
            self._resize_pixmap_to_fit_smooth()
            return

        self.setFixedSize(available_size)
        self.setPixmap(ultra_quality_pixmap)

        # Cache the ultra quality version with maximum quality preservation
        if self._cache and self._word is not None:
            success = self._cache.cache_thumbnail(
                self.current_path,
                ultra_quality_pixmap,
                available_size,
                self._word,
                self._variation,
            )
            if success:
                logging.debug(
                    f"🔥 ULTRA QUALITY thumbnail cached: {os.path.basename(self.current_path)}"
                )
            else:
                logging.debug(
                    f"⚠️ Failed to cache ultra quality thumbnail: {os.path.basename(self.current_path)}"
                )

        logging.debug(
            f"🔥 ULTRA QUALITY thumbnail processed: {os.path.basename(self.current_path)}"
        )

    def _get_quality_settings(self) -> dict:
        """Get quality settings from browse tab settings."""
        try:
            browse_settings = self.thumbnail_box.browse_tab.browse_settings
            return browse_settings.get_thumbnail_processing_settings()
        except Exception:
            # Fallback to default settings if settings unavailable
            return {
                "ultra_quality_enabled": True,
                "sharpening_enabled": True,
                "enhancement_enabled": True,
                "cache_quality_mode": "two_stage",
                "enable_disk_cache": True,
            }

    def _resize_pixmap_to_fit_smooth(self) -> None:
        """Enhanced smooth resizing with improved multi-step scaling."""
        if not self._original_pixmap:
            return

        available_size = self._calculate_available_space()
        scaled_size = self._calculate_scaled_pixmap_size(available_size)

        # Enhanced multi-step scaling for better quality
        scaled_pixmap = self._create_enhanced_scaled_pixmap(scaled_size)

        # CRITICAL: Ensure pixmap is not null before proceeding
        if scaled_pixmap.isNull():
            logging.warning(f"Failed to create scaled pixmap for {self.current_path}")
            return

        self.setFixedSize(available_size)
        self.setPixmap(scaled_pixmap)

        # Cache the high-quality version with maximum quality preservation
        if self._cache and self._word is not None:
            success = self._cache.cache_thumbnail(
                self.current_path,
                scaled_pixmap,
                scaled_size,
                self._word,
                self._variation,
            )
            if success:
                logging.debug(
                    f"✅ HIGH-QUALITY thumbnail cached: {os.path.basename(self.current_path)}"
                )
            else:
                logging.debug(
                    f"⚠️ Failed to cache high-quality thumbnail: {os.path.basename(self.current_path)}"
                )

    def _calculate_scaled_pixmap_size(self, available_size: QSize) -> QSize:
        """Calculate the optimal size for the pixmap while maintaining aspect ratio."""
        if not self._original_pixmap:
            return QSize(0, 0)

        aspect_ratio = self._original_pixmap.height() / self._original_pixmap.width()
        target_width = available_size.width()
        target_height = int(target_width * aspect_ratio)

        if target_height > available_size.height():
            target_height = available_size.height()
            target_width = int(target_height / aspect_ratio)

        return QSize(target_width, target_height)

    def _create_enhanced_scaled_pixmap(self, target_size: QSize) -> QPixmap:
        """Create enhanced scaled pixmap with improved multi-step scaling."""
        if not self._original_pixmap:
            return QPixmap()

        original_size = self._original_pixmap.size()

        # Calculate scale factor
        scale_factor = min(
            target_size.width() / original_size.width(),
            target_size.height() / original_size.height(),
        )

        # Enhanced multi-step scaling with lower threshold
        if scale_factor < 0.75:  # Improved from 0.5
            # Multi-step scaling for better quality
            if scale_factor < 0.4:
                # Very aggressive downscaling - use 3 stages
                intermediate_factor1 = 0.7
                intermediate_factor2 = 0.5

                # Stage 1
                intermediate_size1 = QSize(
                    int(original_size.width() * intermediate_factor1),
                    int(original_size.height() * intermediate_factor1),
                )
                stage1_pixmap = self._original_pixmap.scaled(
                    intermediate_size1,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                # Stage 2
                intermediate_size2 = QSize(
                    int(original_size.width() * intermediate_factor2),
                    int(original_size.height() * intermediate_factor2),
                )
                stage2_pixmap = stage1_pixmap.scaled(
                    intermediate_size2,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                # Final stage
                final_pixmap = stage2_pixmap.scaled(
                    target_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                return final_pixmap
            else:
                # Moderate downscaling - use 2 stages
                intermediate_factor = 0.75
                intermediate_size = QSize(
                    int(original_size.width() * intermediate_factor),
                    int(original_size.height() * intermediate_factor),
                )

                # Step 1: Scale to intermediate size
                intermediate_pixmap = self._original_pixmap.scaled(
                    intermediate_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                # Step 2: Scale to final size
                final_pixmap = intermediate_pixmap.scaled(
                    target_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                return final_pixmap
        else:
            # Single-step high-quality scaling for smaller scale changes
            return self._original_pixmap.scaled(
                target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

    # ... [Keep all other methods unchanged: mousePressEvent, enterEvent, leaveEvent,
    #      set_selected, _draw_border, paintEvent, resizeEvent, _initialize_cache,
    #      set_word_and_variation, _enhance_image_quality, _check_viewport_visibility]

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press events."""
        if not self.is_in_sequence_viewer:
            self.thumbnail_box.browse_tab.selection_handler.on_thumbnail_clicked(self)

    def enterEvent(self, event) -> None:
        """Highlight border on hover."""
        self._border_color = BLUE
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """Remove border highlight when leaving hover."""
        self._border_color = GOLD if self.selected else None
        self.update()
        super().leaveEvent(event)

    def set_selected(self, selected: bool) -> None:
        """Set selection state."""
        self.selected = selected
        self._border_color = GOLD if selected else None
        self.update()

    def _draw_border(self, painter: QPainter) -> None:
        """Draw border around the thumbnail."""
        if not self._original_pixmap or not (
            self._border_color or self.is_in_sequence_viewer
        ):
            return

        color = QColor(GOLD if self.is_in_sequence_viewer else self._border_color)
        border_width = int(
            self.border_width
            * (self.SEQUENCE_VIEWER_BORDER_SCALE if self.is_in_sequence_viewer else 1)
        )

        pen = QPen(color)
        pen.setWidth(border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        img_width, img_height = self.pixmap().width(), self.pixmap().height()
        x = (self.width() - img_width) // 2
        y = (self.height() - img_height) // 2
        rect = QRect(x, y, img_width, img_height)

        border_offset = border_width // 2
        adjusted_rect = rect.adjusted(
            border_offset, border_offset, -border_offset, -border_offset
        )

        painter.drawRect(adjusted_rect)

    def paintEvent(self, event) -> None:
        """Handle paint events."""
        super().paintEvent(event)

        if self.is_in_sequence_viewer or self._border_color:
            painter = QPainter(self)
            self._draw_border(painter)

    def resizeEvent(self, event) -> None:
        """Handle resize events."""
        self._cached_available_size = None
        self._border_width = max(1, int(self.width() * self.BORDER_WIDTH_RATIO))
        super().resizeEvent(event)

    def _initialize_cache(self) -> None:
        """Initialize cache for ultra quality thumbnails."""
        try:
            browse_settings = self.thumbnail_box.browse_tab.browse_settings
            if browse_settings.get_enable_disk_cache():
                cache_dir = browse_settings.get_cache_location()
                if not cache_dir:
                    cache_dir = None
                max_size = browse_settings.get_cache_max_size_mb()
                self._cache = BrowseThumbnailCache(cache_dir, max_size)
        except Exception as e:
            logging.debug(f"Failed to initialize ultra quality thumbnail cache: {e}")

    def set_word_and_variation(self, word: str, variation: int) -> None:
        """Set the word and variation for cache key generation."""
        self._word = word
        self._variation = variation

    def _enhance_image_quality(self) -> None:
        """Legacy method - now handled by ultra_processor."""
        pass  # Ultra quality processing handles all enhancement

    def _check_viewport_visibility(self) -> bool:
        """Check if this thumbnail is currently visible in the viewport."""
        try:
            scroll_widget = self.thumbnail_box.sequence_picker.scroll_widget
            scroll_area = scroll_widget.scroll_area

            thumbnail_global_pos = self.mapToGlobal(self.rect().topLeft())
            scroll_area_global_pos = scroll_area.mapToGlobal(
                scroll_area.rect().topLeft()
            )

            relative_pos = thumbnail_global_pos - scroll_area_global_pos
            visible_rect = scroll_area.viewport().rect()
            thumbnail_rect = self.rect()
            thumbnail_rect.moveTopLeft(relative_pos)

            return visible_rect.intersects(thumbnail_rect)

        except Exception:
            return True
