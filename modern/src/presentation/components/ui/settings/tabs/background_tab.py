"""
Background settings tab with animated clickable preview tiles.
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QGridLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPainter, QCursor

from src.core.interfaces.background_interfaces import IBackgroundService


class AnimatedBackgroundTile(QWidget):
    """Clickable animated preview tile for a background type."""

    clicked = pyqtSignal(str)  # Emits background type when clicked

    def __init__(self, background_type: str, parent=None):
        super().__init__(parent)
        self.background_type = background_type
        self.is_selected = False
        self.animation_frame = 0

        self.setFixedSize(200, 150)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Animation timer
        self.animation_timer = QTimer(self)  # Set parent for proper cleanup
        self.animation_timer.timeout.connect(self._animate)
        self.animation_timer.start(50)  # 20 FPS for smooth animation

        self._setup_styling()

    def __del__(self):
        """Destructor to ensure proper cleanup."""
        self.cleanup()

    def cleanup(self):
        """Clean up resources, particularly the animation timer."""
        if hasattr(self, "animation_timer") and self.animation_timer:
            if self.animation_timer.isActive():
                self.animation_timer.stop()
            self.animation_timer.deleteLater()
            self.animation_timer = None

    def closeEvent(self, event):
        """Handle widget close event."""
        self.cleanup()
        super().closeEvent(event)

    def _setup_styling(self):
        """Set up the tile styling."""
        border_color = "#0078d4" if self.is_selected else "#555"
        self.setStyleSheet(
            f"""
            AnimatedBackgroundTile {{
                border: 3px solid {border_color};
                border-radius: 12px;
                background: transparent;
            }}
            AnimatedBackgroundTile:hover {{
                border-color: #106ebe;
            }}
        """
        )

    def set_selected(self, selected: bool):
        """Set the selection state of this tile."""
        self.is_selected = selected
        self._setup_styling()
        self.update()

    def mousePressEvent(self, event):
        """Handle mouse click to select this background."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.background_type)
        super().mousePressEvent(event)

    def _animate(self):
        """Update animation frame and repaint."""
        self.animation_frame += 1
        self.update()

    def paintEvent(self, event):
        """Paint the animated background preview."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create animated preview based on background type
        if self.background_type == "Aurora":
            self._paint_aurora(painter)
        elif self.background_type == "AuroraBorealis":
            self._paint_aurora_borealis(painter)
        elif self.background_type == "Starfield":
            self._paint_starfield(painter)
        elif self.background_type == "Snowfall":
            self._paint_snowfall(painter)
        elif self.background_type == "Bubbles":
            self._paint_bubbles(painter)

        # Draw title overlay
        self._paint_title_overlay(painter)

        painter.end()

    def _paint_aurora(self, painter):
        """Paint animated aurora background."""
        from PyQt6.QtGui import QLinearGradient, QColor
        import math

        # Animated gradient shift
        shift = math.sin(self.animation_frame * 0.02) * 0.1

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(max(0, 0 + shift), QColor("#1a0f3d"))
        gradient.setColorAt(min(1, 0.3 + shift), QColor("#2d1b69"))
        gradient.setColorAt(min(1, 0.7 + shift), QColor("#40e0d0"))
        gradient.setColorAt(min(1, 1 + shift), QColor("#ff6b9d"))
        painter.fillRect(self.rect(), gradient)

        # Add some sparkles
        painter.setPen(QColor(255, 255, 255, 150))
        for i in range(5):
            x = (
                50 + i * 30 + math.sin(self.animation_frame * 0.05 + i) * 20
            ) % self.width()
            y = (
                30 + i * 25 + math.cos(self.animation_frame * 0.03 + i) * 15
            ) % self.height()
            painter.drawEllipse(int(x), int(y), 2, 2)

    def _paint_aurora_borealis(self, painter):
        """Paint animated aurora borealis background."""
        from PyQt6.QtGui import QLinearGradient, QColor
        import math

        # Animated light wave effect
        wave_offset = math.sin(self.animation_frame * 0.03) * 0.2

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(max(0, 0 + wave_offset), QColor("#0a0a20"))  # Deep blue
        gradient.setColorAt(min(1, 0.3 + wave_offset), QColor("#1a2040"))  # Medium blue
        gradient.setColorAt(min(1, 0.6 + wave_offset), QColor("#20ff80"))  # Green
        gradient.setColorAt(min(1, 0.8 + wave_offset), QColor("#80ffff"))  # Light blue
        gradient.setColorAt(min(1, 1 + wave_offset), QColor("#ffffff"))  # White
        painter.fillRect(self.rect(), gradient)

        # Add flowing light waves
        painter.setPen(QColor(255, 255, 255, 100))
        for i in range(3):
            wave_y = (
                self.height() * 0.3
                + math.sin(self.animation_frame * 0.04 + i * 2) * self.height() * 0.2
            )
            painter.drawLine(0, int(wave_y), self.width(), int(wave_y))

    def _paint_starfield(self, painter):
        """Paint animated starfield background."""
        from PyQt6.QtGui import QRadialGradient, QColor
        import math

        gradient = QRadialGradient(
            self.width() / 2, self.height() / 2, self.width() / 2
        )
        gradient.setColorAt(0, QColor("#000033"))
        gradient.setColorAt(1, QColor("#000000"))
        painter.fillRect(self.rect(), gradient)

        # Twinkling stars
        import random

        random.seed(42)  # Consistent star positions
        for i in range(15):
            x = random.randint(10, self.width() - 10)
            y = random.randint(10, self.height() - 10)
            # Twinkling effect
            alpha = int(100 + 155 * abs(math.sin(self.animation_frame * 0.1 + i)))
            painter.setPen(QColor(255, 255, 255, alpha))
            painter.drawPoint(x, y)

    def _paint_snowfall(self, painter):
        """Paint animated snowfall background."""
        from PyQt6.QtGui import QLinearGradient, QColor
        import math

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#87CEEB"))
        gradient.setColorAt(1, QColor("#4682B4"))
        painter.fillRect(self.rect(), gradient)

        # Falling snowflakes
        painter.setPen(QColor(255, 255, 255, 200))
        for i in range(8):
            x = (i * 25 + math.sin(self.animation_frame * 0.02 + i) * 10) % self.width()
            y = (self.animation_frame * 2 + i * 20) % (self.height() + 20)
            painter.drawEllipse(int(x), int(y), 3, 3)

    def _paint_bubbles(self, painter):
        """Paint animated bubbles background."""
        from PyQt6.QtGui import QRadialGradient, QColor
        import math

        gradient = QRadialGradient(
            self.width() / 2, self.height() / 2, self.width() / 2
        )
        gradient.setColorAt(0, QColor("#006994"))
        gradient.setColorAt(1, QColor("#003d5c"))
        painter.fillRect(self.rect(), gradient)

        # Floating bubbles
        painter.setPen(QColor(100, 200, 255, 150))
        for i in range(6):
            x = (
                30 + i * 30 + math.sin(self.animation_frame * 0.03 + i) * 15
            ) % self.width()
            y = self.height() - (self.animation_frame + i * 30) % (self.height() + 30)
            size = 8 + int(3 * math.sin(self.animation_frame * 0.05 + i))
            painter.drawEllipse(int(x), int(y), size, size)

    def _paint_title_overlay(self, painter):
        """Paint the background type title overlay."""
        from PyQt6.QtGui import QColor

        # Semi-transparent overlay at bottom
        overlay_height = 30
        painter.fillRect(
            0,
            self.height() - overlay_height,
            self.width(),
            overlay_height,
            QColor(0, 0, 0, 120),
        )

        # Title text
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        painter.drawText(
            self.rect().adjusted(0, 0, 0, -5),
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom,
            self.background_type,
        )


class BackgroundTab(QWidget):
    """Background settings tab with animated preview tiles."""

    background_changed = pyqtSignal(str, str)  # setting_name, value

    def __init__(self, background_service: IBackgroundService, parent=None):
        super().__init__(parent)
        self.background_service = background_service
        self.tiles = {}
        self.current_selection = None
        self._setup_ui()
        self._load_settings()

    def __del__(self):
        """Destructor to ensure proper cleanup."""
        self.cleanup()

    def cleanup(self):
        """Clean up all animated tiles and their resources."""
        for tile in self.tiles.values():
            if hasattr(tile, "cleanup"):
                tile.cleanup()
        self.tiles.clear()

    def closeEvent(self, event):
        """Handle widget close event."""
        self.cleanup()
        super().closeEvent(event)

    def _setup_ui(self):
        """Set up the user interface."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("Background Settings")
        title.setObjectName("section_title")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Description
        description = QLabel(
            "Click on a background preview to select it. The background will be applied immediately."
        )
        description.setWordWrap(True)
        description.setStyleSheet(
            "color: #888; font-style: italic; margin-bottom: 10px;"
        )
        main_layout.addWidget(description)

        # Preview tiles section
        preview_section = self._create_preview_section()
        main_layout.addWidget(preview_section)

        main_layout.addStretch()
        self._apply_styling()

    def _create_preview_section(self) -> QGroupBox:
        """Create the animated preview tiles section."""
        section = QGroupBox("Choose Your Background")
        section.setObjectName("settings_section")
        layout = QVBoxLayout(section)
        layout.setSpacing(20)

        # Grid layout for tiles
        tiles_layout = QGridLayout()
        tiles_layout.setSpacing(20)

        # Create animated tiles for each background
        backgrounds = self.background_service.get_available_backgrounds()
        for i, bg_type in enumerate(backgrounds):
            tile = AnimatedBackgroundTile(bg_type)
            tile.clicked.connect(self._on_tile_clicked)
            self.tiles[bg_type] = tile

            # Arrange in 2x2 grid
            row = i // 2
            col = i % 2
            tiles_layout.addWidget(tile, row, col)

        # Center the grid
        tiles_container = QWidget()
        tiles_container.setLayout(tiles_layout)

        container_layout = QHBoxLayout()
        container_layout.addStretch()
        container_layout.addWidget(tiles_container)
        container_layout.addStretch()

        layout.addLayout(container_layout)

        return section

    def _load_settings(self):
        """Load current settings and update tile selection."""
        current_background = self.background_service.get_current_background()
        self._select_tile(current_background)

    def _select_tile(self, background_type: str):
        """Select a specific tile and deselect others."""
        # Deselect all tiles
        for tile in self.tiles.values():
            tile.set_selected(False)

        # Select the specified tile
        if background_type in self.tiles:
            self.tiles[background_type].set_selected(True)
            self.current_selection = background_type

    def _on_tile_clicked(self, background_type: str):
        """Handle tile click to change background."""
        if self.background_service.set_background(background_type):
            self._select_tile(background_type)
            self.background_changed.emit("background_type", background_type)
            # Note: Logging is handled by the main application's settings change handler

    def _apply_styling(self):
        """Apply custom styling to the tab."""
        self.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                border: 2px solid #333;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """
        )
