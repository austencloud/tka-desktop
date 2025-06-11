"""
Quality Enhancer - Handles high-quality image scaling with single responsibility.

Extracted from the monolithic ImageProcessor class to follow SRP.
"""

import logging
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QSize, QRect


class QualityEnhancer:
    """
    Handles high-quality image scaling and enhancement.

    Responsibilities:
    - High-quality scaling algorithms
    - Multi-step scaling for better quality
    - Error pixmap creation
    - Quality optimization
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def scale_image_high_quality(
        self, image: QImage, target_width: int, target_height: int
    ) -> QImage:
        """
        Scale image using high-quality algorithm.

        Args:
            image: Source image
            target_width: Target width
            target_height: Target height

        Returns:
            Scaled QImage
        """
        if image.isNull() or target_width <= 0 or target_height <= 0:
            return QImage()

        return image.scaled(
            target_width,
            target_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    def scale_image_multi_step(
        self, image: QImage, target_width: int, target_height: int
    ) -> QImage:
        """
        Scale image using multi-step algorithm for better quality on large scale changes.

        Args:
            image: Source image
            target_width: Target width
            target_height: Target height

        Returns:
            Scaled QImage with enhanced quality
        """
        if image.isNull() or target_width <= 0 or target_height <= 0:
            return QImage()

        original_width = image.width()
        original_height = image.height()

        if original_width <= 0 or original_height <= 0:
            return QImage()

        # Calculate scale factor
        scale_factor = min(
            target_width / original_width, target_height / original_height
        )

        # Use multi-step scaling for significant size reductions
        if scale_factor < 0.6:
            return self._multi_step_scale(
                image, target_width, target_height, scale_factor
            )
        else:
            # Single-step high-quality scaling for smaller changes
            return self.scale_image_high_quality(image, target_width, target_height)

    def _multi_step_scale(
        self, image: QImage, target_width: int, target_height: int, scale_factor: float
    ) -> QImage:
        """
        Perform multi-step scaling for better quality.

        Args:
            image: Source image
            target_width: Target width
            target_height: Target height
            scale_factor: Overall scale factor

        Returns:
            Multi-step scaled QImage
        """
        original_width = image.width()
        original_height = image.height()

        if scale_factor < 0.4:
            # Very aggressive downscaling - use 3 stages
            intermediate_factor1 = 0.7
            intermediate_factor2 = 0.5

            # Stage 1
            intermediate_width1 = int(original_width * intermediate_factor1)
            intermediate_height1 = int(original_height * intermediate_factor1)

            stage1_image = image.scaled(
                intermediate_width1,
                intermediate_height1,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Stage 2
            intermediate_width2 = int(original_width * intermediate_factor2)
            intermediate_height2 = int(original_height * intermediate_factor2)

            stage2_image = stage1_image.scaled(
                intermediate_width2,
                intermediate_height2,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Final stage
            final_image = stage2_image.scaled(
                target_width,
                target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.logger.debug(
                f"3-stage scaling: {original_width}x{original_height} -> {target_width}x{target_height}"
            )
            return final_image

        else:
            # Moderate downscaling - use 2 stages
            intermediate_factor = 0.75
            intermediate_width = int(original_width * intermediate_factor)
            intermediate_height = int(original_height * intermediate_factor)

            # Step 1: Scale to intermediate size
            intermediate_image = image.scaled(
                intermediate_width,
                intermediate_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Step 2: Scale to final size
            final_image = intermediate_image.scaled(
                target_width,
                target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.logger.debug(
                f"2-stage scaling: {original_width}x{original_height} -> {target_width}x{target_height}"
            )
            return final_image

    def create_error_pixmap(self, size: QSize) -> QPixmap:
        """
        Create a pixmap indicating an error loading the image.

        Args:
            size: Size of the error pixmap

        Returns:
            QPixmap with error indicator
        """
        if not size.isValid() or size.width() <= 0 or size.height() <= 0:
            size = QSize(100, 100)  # Default error pixmap size

        pixmap = QPixmap(size)
        pixmap.fill(QColor(220, 50, 50))  # Red background

        painter = QPainter(pixmap)
        font = QFont()
        font.setPointSize(max(8, min(10, size.height() // 10)))  # Dynamic font size
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))  # White text

        text_rect = QRect(5, 5, size.width() - 10, size.height() - 10)
        painter.drawText(
            text_rect, Qt.AlignmentFlag.AlignCenter, "Error\nLoading\nImage"
        )
        painter.end()

        return pixmap
