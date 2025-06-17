import random
import math
from PyQt6.QtGui import QPainter, QPixmap, QCursor, QColor, QRadialGradient
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPoint
from ..asset_utils import get_image_path


class UFOManager:
    """
    Enhanced UFO manager that combines legacy modular logic with modern improvements.

    Supports two behavior modes:
    1. Wandering UFO: Always visible, wanders around with pauses (legacy simple behavior)
    2. Fly-by UFO: Periodic appearances from off-screen with straight-line movement (legacy modular behavior)
    """

    def __init__(self, behavior_mode="wandering"):
        # Try to load UFO image
        ufo_image_path = get_image_path("backgrounds/ufo.png")
        self.ufo_image = QPixmap(ufo_image_path)

        # Check if image loaded successfully
        self.use_image = not self.ufo_image.isNull()

        if not self.use_image:
            print("UFO image not found, using procedural UFO")

        # Behavior mode: "wandering" or "flyby"
        self.behavior_mode = behavior_mode

        # Initialize UFO based on behavior mode
        if behavior_mode == "flyby":
            self._init_flyby_ufo()
        else:
            self._init_wandering_ufo()

        # Common properties
        self.cursor_over_ufo = False

    def _init_wandering_ufo(self):
        """Initialize UFO for wandering behavior (always visible)."""
        self.ufo = {
            "x": random.uniform(0.1, 0.9),
            "y": random.uniform(0.1, 0.9),
            "size": random.uniform(40, 60),
            "speed": random.uniform(0.003, 0.008),
            "dx": random.uniform(-0.5, 0.5),
            "dy": random.uniform(-0.5, 0.5),
            "paused": False,
            "pause_duration": random.randint(100, 300),
            "glow_phase": 0,
            "active": True,  # Always visible in wandering mode
        }

        self.pause_timer = random.randint(50, 150)

    def _init_flyby_ufo(self):
        """Initialize UFO for fly-by behavior (periodic appearances)."""
        self.ufo = {
            "x": 0,
            "y": 0,
            "size": random.uniform(40, 60),
            "speed": random.uniform(0.01, 0.02),
            "dx": 0,
            "dy": 0,
            "glow_phase": 0,
            "active": False,  # Starts inactive
            "fly_off": False,
        }

        # Appearance management (from legacy UFOAppearanceManager)
        self.appearance_timer = random.randint(100, 300)  # Frames until next appearance
        self.active_duration = 0  # How long UFO stays active
        self.entering = False

    def animate_ufo(self):
        """Update UFO animation and movement based on behavior mode."""
        if self.behavior_mode == "flyby":
            self._manage_flyby_appearance()
            if self.ufo["active"]:
                self._move_flyby_ufo()
        else:
            self._move_wandering_ufo()

        self._update_glow()

    def _manage_flyby_appearance(self):
        """Handle UFO appearance and disappearance for fly-by mode."""
        if not self.ufo["active"]:
            # Count down the appearance timer
            self.appearance_timer -= 1
            if self.appearance_timer <= 0:
                # UFO is about to appear
                self.ufo["active"] = True
                self.ufo["fly_off"] = False
                self.entering = True
                self._set_offscreen_entry()
                self.appearance_timer = random.randint(500, 1000)  # Reset timer
                self.active_duration = random.randint(300, 500)  # Stay active duration
        else:
            # UFO is active, count down active duration
            self.active_duration -= 1
            if self.active_duration <= 0 or self.ufo["fly_off"]:
                # Deactivate UFO
                self.ufo["active"] = False
                self.appearance_timer = random.randint(500, 1000)

    def _set_offscreen_entry(self):
        """Initialize UFO entry from off-screen for straight fly-by."""
        entry_side = random.choice(["left", "right", "top", "bottom"])

        if entry_side == "left":
            self.ufo["x"] = -0.1
            self.ufo["y"] = random.uniform(0.2, 0.8)
            self.ufo["dx"] = random.uniform(0.01, 0.02)
            self.ufo["dy"] = 0
        elif entry_side == "right":
            self.ufo["x"] = 1.1
            self.ufo["y"] = random.uniform(0.2, 0.8)
            self.ufo["dx"] = -random.uniform(0.01, 0.02)
            self.ufo["dy"] = 0
        elif entry_side == "top":
            self.ufo["x"] = random.uniform(0.2, 0.8)
            self.ufo["y"] = -0.1
            self.ufo["dx"] = 0
            self.ufo["dy"] = random.uniform(0.01, 0.02)
        elif entry_side == "bottom":
            self.ufo["x"] = random.uniform(0.2, 0.8)
            self.ufo["y"] = 1.1
            self.ufo["dx"] = 0
            self.ufo["dy"] = -random.uniform(0.01, 0.02)

    def _move_flyby_ufo(self):
        """Move UFO in straight line for fly-by behavior."""
        if self.ufo["active"] and not self.ufo["fly_off"]:
            self.ufo["x"] += self.ufo["dx"] * self.ufo["speed"]
            self.ufo["y"] += self.ufo["dy"] * self.ufo["speed"]

            # Check if UFO has moved out of bounds
            if (
                self.ufo["x"] < -0.1
                or self.ufo["x"] > 1.1
                or self.ufo["y"] < -0.1
                or self.ufo["y"] > 1.1
            ):
                self.ufo["active"] = False

    def _move_wandering_ufo(self):
        """Move UFO with wandering behavior (pauses, direction changes)."""
        ufo = self.ufo

        if ufo["paused"]:
            # Decrease the pause duration
            ufo["pause_duration"] -= 1
            if ufo["pause_duration"] <= 0:
                # Resume movement after pausing
                ufo["paused"] = False
                ufo["dx"] = random.uniform(-0.5, 0.5)
                ufo["dy"] = random.uniform(-0.5, 0.5)
                ufo["speed"] = random.uniform(0.003, 0.008)
                self.pause_timer = random.randint(100, 200)
        else:
            # Move the UFO
            ufo["x"] += ufo["dx"] * ufo["speed"]
            ufo["y"] += ufo["dy"] * ufo["speed"]

            # Handle UFO reaching the screen edges (bounce off the edges)
            if ufo["x"] < 0.05 or ufo["x"] > 0.95:
                ufo["dx"] *= -1  # Reverse direction horizontally
                ufo["x"] = max(0.05, min(0.95, ufo["x"]))  # Keep in bounds
            if ufo["y"] < 0.05 or ufo["y"] > 0.95:
                ufo["dy"] *= -1  # Reverse direction vertically
                ufo["y"] = max(0.05, min(0.95, ufo["y"]))  # Keep in bounds

            # Randomly pause the UFO after some time
            self.pause_timer -= 1
            if self.pause_timer <= 0:
                ufo["paused"] = True
                ufo["pause_duration"] = random.randint(100, 300)

    def _update_glow(self):
        """Update the glow effect for the UFO."""
        self.ufo["glow_phase"] += 0.05
        if self.ufo["glow_phase"] > 2 * math.pi:
            self.ufo["glow_phase"] = 0

    def draw_ufo(self, painter: QPainter, widget: QWidget, cursor_position: QPoint):
        """Draw the UFO with glow effects and cursor interaction."""
        # Only draw if UFO is active
        if not self.ufo["active"]:
            return

        ufo = self.ufo

        ufo_x = int(ufo["x"] * widget.width())
        ufo_y = int(ufo["y"] * widget.height())
        ufo_size = int(ufo["size"])

        # Check cursor interaction
        cursor_x, cursor_y = cursor_position.x(), cursor_position.y()
        distance_to_cursor = math.sqrt(
            (ufo_x - cursor_x) ** 2 + (ufo_y - cursor_y) ** 2
        )
        self.cursor_over_ufo = distance_to_cursor < ufo_size // 2

        if self.cursor_over_ufo:
            widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            widget.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

        # Draw glow effect
        self._draw_ufo_glow(painter, ufo_x, ufo_y, ufo_size)

        if self.use_image and not self.ufo_image.isNull():
            # Draw UFO from image
            scaled_ufo = self.ufo_image.scaled(
                ufo_size,
                ufo_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawPixmap(
                ufo_x - scaled_ufo.width() // 2,
                ufo_y - scaled_ufo.height() // 2,
                scaled_ufo,
            )
        else:
            # Draw procedural UFO
            self._draw_procedural_ufo(painter, ufo_x, ufo_y, ufo_size)

    def _draw_ufo_glow(self, painter: QPainter, x: int, y: int, size: int):
        """Draw a pulsing glow around the UFO."""
        glow_intensity = (math.sin(self.ufo["glow_phase"]) + 1) / 2
        glow_size = int(size * (1.5 + glow_intensity * 0.5))

        # Create radial gradient for glow
        gradient = QRadialGradient(x, y, glow_size // 2)
        glow_color = QColor(100, 255, 100, int(30 * glow_intensity))  # Green glow
        gradient.setColorAt(0, glow_color)
        gradient.setColorAt(1, QColor(0, 0, 0, 0))  # Transparent edge

        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(
            x - glow_size // 2, y - glow_size // 2, glow_size, glow_size
        )

    def _draw_procedural_ufo(self, painter: QPainter, x: int, y: int, size: int):
        """Draw a procedural UFO when image is not available."""
        # UFO body (dome)
        dome_gradient = QRadialGradient(x, y - size // 4, size // 3)
        dome_gradient.setColorAt(0, QColor(200, 200, 220))  # Light metallic
        dome_gradient.setColorAt(1, QColor(120, 120, 140))  # Darker edge

        painter.setBrush(dome_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(x - size // 3, y - size // 2, size * 2 // 3, size // 2)

        # UFO base (saucer)
        base_gradient = QRadialGradient(x, y, size // 2)
        base_gradient.setColorAt(0, QColor(180, 180, 200))
        base_gradient.setColorAt(1, QColor(100, 100, 120))

        painter.setBrush(base_gradient)
        painter.drawEllipse(x - size // 2, y - size // 6, size, size // 3)

        # Add some lights
        light_color = QColor(255, 255, 0, 200)  # Yellow lights
        painter.setBrush(light_color)
        light_size = size // 12

        # Draw lights around the edge
        for i in range(6):
            angle = i * math.pi / 3
            light_x = x + int((size // 2 - light_size) * math.cos(angle))
            light_y = y + int((size // 6) * math.sin(angle))
            painter.drawEllipse(
                light_x - light_size // 2,
                light_y - light_size // 2,
                light_size,
                light_size,
            )

    def set_behavior_mode(self, mode):
        """Change UFO behavior mode at runtime."""
        if mode != self.behavior_mode:
            self.behavior_mode = mode
            if mode == "flyby":
                self._init_flyby_ufo()
            else:
                self._init_wandering_ufo()
