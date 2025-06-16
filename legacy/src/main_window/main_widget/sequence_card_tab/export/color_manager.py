# src/main_window/main_widget/sequence_card_tab/export/color_manager.py
import logging
import sys
from typing import Dict, Any, Optional, Tuple
import re
from PyQt6.QtGui import QImage, QColor
from PyQt6.QtCore import Qt, QVersionNumber

from data.constants import HEX_RED, HEX_BLUE, RED, BLUE


class ColorManager:
    """
    Manages color transformations and corrections for exported images.

    This class handles:
    1. Color profile preservation
    2. Gamma correction
    3. Color channel adjustments
    4. Specific color replacements
    5. Color space transformations for print-optimized output
    """

    def __init__(self, config_settings: Dict[str, Any]):
        """
        Initialize the ColorManager with configuration settings.

        Args:
            config_settings: Dictionary containing color management settings
        """
        self.logger = logging.getLogger(__name__)
        self.settings = config_settings

        # Extract specific settings with defaults
        self.preserve_color_profile = self.settings.get("preserve_color_profile", True)
        self.gamma_correction = self.settings.get("gamma_correction", 1.0)
        self.enhance_red_channel = self.settings.get("enhance_red_channel", 1.15)
        self.color_correction = self.settings.get("color_correction", {})
        self.use_high_bit_depth = self.settings.get("use_high_bit_depth", True)

        # Determine available image formats based on PyQt version
        self._detect_available_formats()

        # Initialize color correction maps
        self._initialize_color_maps()

    def _detect_available_formats(self):
        """Detect available QImage formats based on PyQt version."""
        self.logger.debug("Detecting available QImage formats")

        # Default to 8-bit formats which are always available
        self.high_bit_depth_format = QImage.Format.Format_ARGB32_Premultiplied
        self.standard_format = QImage.Format.Format_ARGB32_Premultiplied

        # Check if 16-bit formats are available
        try:
            # Try to access Format_RGBA64_Premultiplied (available in newer PyQt6 versions)
            if hasattr(QImage.Format, "Format_RGBA64_Premultiplied"):
                self.high_bit_depth_format = QImage.Format.Format_RGBA64_Premultiplied
                self.logger.debug(
                    "Using Format_RGBA64_Premultiplied for high bit depth"
                )
            # Try to access Format_ARGB64_Premultiplied (might be available in some versions)
            elif hasattr(QImage.Format, "Format_ARGB64_Premultiplied"):
                self.high_bit_depth_format = QImage.Format.Format_ARGB64_Premultiplied
                self.logger.debug(
                    "Using Format_ARGB64_Premultiplied for high bit depth"
                )
            else:
                # Fallback to 8-bit format if no 16-bit format is available
                self.logger.warning(
                    "No 16-bit image format available, using 8-bit format"
                )
                self.use_high_bit_depth = False
        except Exception as e:
            self.logger.warning(f"Error detecting image formats: {e}")
            self.use_high_bit_depth = False

    def _initialize_color_maps(self) -> None:
        """Initialize color correction maps for efficient processing."""
        # Add standard colors if not already in the color correction map
        if HEX_RED not in self.color_correction:
            # Default enhancement for the standard red color
            brighter_red = self._brighten_color(HEX_RED, factor=1.15)
            self.color_correction[HEX_RED] = brighter_red

        self.logger.debug(f"Initialized color correction map: {self.color_correction}")

    def _brighten_color(self, hex_color: str, factor: float = 1.15) -> str:
        """
        Brighten a hex color by the specified factor.

        Args:
            hex_color: Hex color string (e.g., "#ED1C24")
            factor: Brightness factor (>1.0 = brighter, <1.0 = darker)

        Returns:
            str: Brightened hex color
        """
        if not hex_color.startswith("#") or len(hex_color) != 7:
            return hex_color

        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)

            # Apply brightness factor with limits
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))

            return f"#{r:02X}{g:02X}{b:02X}"
        except ValueError:
            self.logger.warning(f"Invalid hex color: {hex_color}")
            return hex_color

    def correct_svg_colors(self, svg_data: str) -> str:
        """
        Apply color corrections to SVG data.

        Args:
            svg_data: SVG data as string

        Returns:
            str: Corrected SVG data
        """
        if not svg_data:
            return svg_data

        # Replace known colors with corrected versions
        for original_color, corrected_color in self.color_correction.items():
            # Skip if the original color is not in the standard format
            if not original_color.startswith("#"):
                continue

            # Create patterns to match the color in different contexts
            patterns = [
                # CSS fill property
                re.compile(r'(fill=")(' + re.escape(original_color) + r')(")'),
                # CSS style attribute
                re.compile(r"(fill:\s*)(" + re.escape(original_color) + r")(\s*;)"),
                # Class definition
                re.compile(
                    r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)("
                    + re.escape(original_color)
                    + r")([^}]*?\})"
                ),
            ]

            # Apply replacements
            for pattern in patterns:
                svg_data = pattern.sub(
                    lambda m: m.group(1) + corrected_color + m.group(len(m.groups())),
                    svg_data,
                )

        return svg_data

    def process_image(self, image: QImage) -> QImage:
        """
        Apply color corrections to a QImage.

        Args:
            image: Source QImage

        Returns:
            QImage: Color-corrected QImage
        """
        if image.isNull():
            self.logger.warning("Cannot process null image")
            return image

        # Convert to a format that supports color manipulation
        try:
            if self.use_high_bit_depth and image.format() != self.high_bit_depth_format:
                # Use 16-bit color depth for better color fidelity if available
                self.logger.debug(f"Converting image to high bit depth format")
                processed_image = image.convertToFormat(self.high_bit_depth_format)
            else:
                # Fallback to 8-bit color depth
                self.logger.debug(f"Converting image to standard format")
                processed_image = image.convertToFormat(self.standard_format)
        except Exception as e:
            # If format conversion fails, use the original image
            self.logger.warning(
                f"Error converting image format: {e}. Using original format."
            )
            processed_image = image.copy()

        # Apply gamma correction if needed
        if self.gamma_correction != 1.0:
            processed_image = self._apply_gamma_correction(
                processed_image, self.gamma_correction
            )

        # Apply red channel enhancement if needed
        if self.enhance_red_channel != 1.0:
            processed_image = self._enhance_color_channel(
                processed_image, channel=0, factor=self.enhance_red_channel
            )

        # Apply specific color corrections
        processed_image = self._apply_specific_color_corrections(processed_image)

        return processed_image

    def _apply_gamma_correction(self, image: QImage, gamma: float) -> QImage:
        """
        Apply gamma correction to an image.

        Args:
            image: Source QImage
            gamma: Gamma correction factor

        Returns:
            QImage: Gamma-corrected QImage
        """
        if gamma == 1.0 or image.isNull():
            return image

        # Create a copy of the image to avoid modifying the original
        result = image.copy()

        # Apply gamma correction to each pixel
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))

                # Apply gamma correction to RGB channels
                r = int(255 * pow(color.red() / 255.0, 1.0 / gamma))
                g = int(255 * pow(color.green() / 255.0, 1.0 / gamma))
                b = int(255 * pow(color.blue() / 255.0, 1.0 / gamma))

                # Set the corrected color
                result.setPixelColor(x, y, QColor(r, g, b, color.alpha()))

        return result

    def _enhance_color_channel(
        self, image: QImage, channel: int, factor: float
    ) -> QImage:
        """
        Enhance a specific color channel.

        Args:
            image: Source QImage
            channel: Color channel index (0=R, 1=G, 2=B)
            factor: Enhancement factor

        Returns:
            QImage: Channel-enhanced QImage
        """
        if factor == 1.0 or image.isNull():
            return image

        # Create a copy of the image to avoid modifying the original
        result = image.copy()

        # Apply channel enhancement to each pixel
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))

                # Get current channel values
                channels = [color.red(), color.green(), color.blue()]

                # Enhance the specified channel
                channels[channel] = min(255, int(channels[channel] * factor))

                # Set the corrected color
                result.setPixelColor(
                    x, y, QColor(channels[0], channels[1], channels[2], color.alpha())
                )

        return result

    def _apply_specific_color_corrections(self, image: QImage) -> QImage:
        """
        Apply specific color corrections to an image.

        Args:
            image: Source QImage

        Returns:
            QImage: Color-corrected QImage
        """
        if not self.color_correction or image.isNull():
            return image

        # Create a copy of the image to avoid modifying the original
        result = image.copy()

        # Convert hex colors to QColor objects for comparison
        color_map = {}
        for hex_color, corrected_hex in self.color_correction.items():
            if hex_color.startswith("#") and corrected_hex.startswith("#"):
                try:
                    original = QColor(hex_color)
                    corrected = QColor(corrected_hex)
                    color_map[original.rgb()] = corrected
                except Exception as e:
                    self.logger.warning(
                        f"Invalid color conversion: {hex_color} -> {corrected_hex}: {e}"
                    )

        # Apply color corrections to each pixel
        for y in range(image.height()):
            for x in range(image.width()):
                color = QColor(image.pixel(x, y))

                # Check if this color needs correction (with some tolerance)
                for original_rgb, corrected_color in color_map.items():
                    original_color = QColor(original_rgb)

                    # Use color distance to allow for some tolerance
                    if (
                        self._color_distance(color, original_color) < 30
                    ):  # Adjust tolerance as needed
                        # Apply the correction
                        result.setPixelColor(
                            x,
                            y,
                            QColor(
                                corrected_color.red(),
                                corrected_color.green(),
                                corrected_color.blue(),
                                color.alpha(),
                            ),
                        )
                        break

        return result

    def _color_distance(self, color1: QColor, color2: QColor) -> float:
        """
        Calculate the Euclidean distance between two colors in RGB space.

        Args:
            color1: First color
            color2: Second color

        Returns:
            float: Color distance
        """
        return (
            (color1.red() - color2.red()) ** 2
            + (color1.green() - color2.green()) ** 2
            + (color1.blue() - color2.blue()) ** 2
        ) ** 0.5
