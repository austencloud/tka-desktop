import random
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget


class CometManager:
    """
    Manages comet appearance and animation with realistic tail effects.
    
    Comets appear randomly from screen edges, travel across the sky with
    beautiful trailing effects, and fade out naturally.
    """
    
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
        self.comet_timer = random.randint(300, 600)  # Random appearance interval
        self.max_tail_length = 35  # Tail length limit

    def activate_comet(self):
        """Activate the comet by setting its initial position and properties."""
        self.comet_active = True
        
        # Choose random starting position from screen edges
        start_position_options = [
            (random.uniform(-0.1, 0), random.uniform(0.1, 0.9)),  # Coming from left
            (random.uniform(1.0, 1.1), random.uniform(0.1, 0.9)),  # Coming from right
            (random.uniform(0.1, 0.9), random.uniform(-0.1, 0)),  # Coming from top
            (random.uniform(0.1, 0.9), random.uniform(1.0, 1.1)),  # Coming from bottom
        ]
        start_x, start_y = random.choice(start_position_options)

        # Calculate direction vector (normalized)
        dx = random.uniform(-0.5, 0.5)
        dy = random.uniform(-0.5, 0.5)
        normalization_factor = (dx**2 + dy**2) ** 0.5
        if normalization_factor > 0:
            dx /= normalization_factor
            dy /= normalization_factor

        # Assign random color for the comet (bright colors)
        comet_color = QColor(
            random.randint(200, 255),  # Red
            random.randint(200, 255),  # Green
            random.randint(150, 255),  # Blue
        )

        self.comet = {
            "x": start_x,
            "y": start_y,
            "prev_x": start_x,
            "prev_y": start_y,
            "size": random.uniform(8, 16),
            "dx": dx,
            "dy": dy,
            "speed": random.uniform(0.015, 0.025),
            "tail": [],  # Reset tail
            "color": comet_color,
            "off_screen": False,  # Reset the off-screen state when a new comet appears
            "fading": False,  # Comet is not yet fading its tail
        }
        
        # Reset timer for next comet
        self.comet_timer = random.randint(400, 800)

    def move_comet(self):
        """Update comet position and tail animation."""
        comet = self.comet

        # If comet is fading, only fade out the tail without moving
        if comet["fading"]:
            if len(comet["tail"]) > 0:
                comet["tail"].pop(0)  # Remove points gradually
            else:
                self.comet_active = False  # Deactivate when tail is gone
                self.comet_timer = random.randint(300, 600)  # Reset timer
            return

        # Normal comet movement and tail updating
        new_x = comet["x"] + comet["dx"] * comet["speed"]
        new_y = comet["y"] + comet["dy"] * comet["speed"]

        # Add the comet's current position to the tail
        comet["tail"].append((comet["x"], comet["y"], comet["size"]))

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
        """Draw the comet and its tail with gradient effects."""
        if not self.comet_active:
            return

        comet = self.comet
        
        # Draw comet's tail with smooth gradient effect
        painter.setPen(Qt.PenStyle.NoPen)

        if len(comet["tail"]) > 1:
            tail_length = len(comet["tail"])
            for i, (tx, ty, size) in enumerate(reversed(comet["tail"])):
                # Calculate opacity for gradient effect
                opacity = (tail_length - i) / tail_length
                tail_x = int(tx * widget.width())
                tail_y = int(ty * widget.height())

                # Create fading color with opacity
                fading_color = QColor(
                    comet["color"].red(),
                    comet["color"].green(),
                    comet["color"].blue(),
                    int(255 * opacity * 0.8),  # Slightly transparent
                )
                painter.setBrush(fading_color)
                painter.setOpacity(opacity)
                
                # Draw tail segment
                tail_size = int(size * opacity * 0.7)  # Tail gets smaller
                painter.drawEllipse(
                    tail_x - tail_size//2, 
                    tail_y - tail_size//2, 
                    tail_size, 
                    tail_size
                )

        # Draw the comet head (brightest part)
        if not comet["fading"]:
            comet_x = int(comet["x"] * widget.width())
            comet_y = int(comet["y"] * widget.height())
            
            painter.setOpacity(1.0)
            painter.setBrush(comet["color"])
            comet_size = int(comet["size"])
            painter.drawEllipse(
                comet_x - comet_size//2, 
                comet_y - comet_size//2, 
                comet_size, 
                comet_size
            )
        
        # Reset opacity for other drawing operations
        painter.setOpacity(1.0)
