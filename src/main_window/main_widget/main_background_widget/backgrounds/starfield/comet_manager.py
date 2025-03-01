import random
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget


class CometManager:
    def __init__(self):
        self.comet_active = False
        self.comet = {
            "x": 0,
            "y": 0,
            "size": 15,
            "dx": 0,
            "dy": 0,
            "speed": random.uniform(0.02, 0.03),
            "tail": [],
            "color": QColor(255, 255, 255),
            "prev_x": 0,
            "prev_y": 0,
            "off_screen": False,  # Track whether the comet has moved off-screen
            "fading": False,  # Track whether the comet is in tail fading mode
        }
        self.comet_timer = 5
        self.max_tail_length = 35  # Tail length limit

    def activate_comet(self):
        """Activate the comet by setting its initial position and properties."""
        self.comet_active = True
        start_position_options = [
            (random.uniform(-0.1, 0), random.uniform(0.1, 0.9)),  # Coming from left
            (random.uniform(1.0, 1.1), random.uniform(0.1, 0.9)),  # Coming from right
        ]
        start_x, start_y = random.choice(start_position_options)

        dx = random.uniform(-0.5, 0.5)
        dy = random.uniform(-0.5, 0.5)
        normalization_factor = (dx**2 + dy**2) ** 0.5
        dx /= normalization_factor
        dy /= normalization_factor

        # Assign random color for the comet
        comet_color = QColor(
            random.randint(150, 255),  # Red
            random.randint(150, 255),  # Green
            random.randint(150, 255),  # Blue
        )

        self.comet = {
            "x": start_x,
            "y": start_y,
            "prev_x": start_x,
            "prev_y": start_y,
            "size": random.uniform(10, 20),
            "dx": dx,
            "dy": dy,
            "speed": random.uniform(0.02, 0.03),
            "tail": [],  # Reset tail
            "color": comet_color,
            "off_screen": False,  # Reset the off-screen state when a new comet appears
            "fading": False,  # Comet is not yet fading its tail
        }

    def move_comet(self):
        comet = self.comet

        # If comet is fading, only fade out the tail without moving
        if comet["fading"]:
            if len(comet["tail"]) > 0:
                comet["tail"].pop(0)  # Remove points gradually
            else:
                self.comet_active = False  # Deactivate when tail is gone
            return

        # Normal comet movement and tail updating
        new_x = comet["x"] + comet["dx"] * comet["speed"]
        new_y = comet["y"] + comet["dy"] * comet["speed"]

        # Add the comet's new position to the tail
        comet["tail"].append((new_x, new_y, comet["size"]))

        # Update comet's position
        comet["prev_x"], comet["prev_y"] = comet["x"], comet["y"]
        comet["x"], comet["y"] = new_x, new_y

        # Limit the tail length to prevent indefinite growth
        if len(comet["tail"]) > self.max_tail_length:
            comet["tail"].pop(0)

        # Check if the comet has moved off-screen
        if (
            comet["x"] < -0.2
            or comet["x"] > 1.2
            or comet["y"] < -0.2
            or comet["y"] > 1.2
        ):
            comet["off_screen"] = True

        # Once comet moves off-screen, stop adding new points and start fading
        if comet["off_screen"]:
            comet["fading"] = True  # Begin tail fading mode

    def draw_comet(self, painter: QPainter, widget: QWidget):
        if not self.comet_active:
            return

        comet = self.comet
        comet_x = int(comet["x"] * widget.width())
        comet_y = int(comet["y"] * widget.height())

        # Draw comet's tail with interpolated points for a smoother transition
        painter.setPen(Qt.PenStyle.NoPen)

        if len(comet["tail"]) > 1:
            tail_length = len(comet["tail"])
            for i, (tx, ty, size) in enumerate(reversed(comet["tail"])):
                # Smooth gradient effect
                opacity = (
                    tail_length - i
                ) / tail_length  # Decreases as we move down the tail
                tail_x = int(tx * widget.width())
                tail_y = int(ty * widget.height())

                # Apply gradient-like fading with opacity
                fading_color = QColor(
                    comet["color"].red(),
                    comet["color"].green(),
                    comet["color"].blue(),
                    int(255 * opacity),  # Adjust alpha based on opacity
                )
                painter.setBrush(fading_color)
                painter.setOpacity(opacity)
                painter.drawEllipse(
                    tail_x, tail_y, int(size * opacity), int(size * opacity)
                )

        # Draw the comet itself (brighter at the head of the tail)
        painter.setOpacity(1.0)
        painter.setBrush(comet["color"])
        painter.drawEllipse(comet_x, comet_y, int(comet["size"]), int(comet["size"]))
