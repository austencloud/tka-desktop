import random
from PyQt6.QtGui import QPainter, QColor, QLinearGradient, QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget


class ShootingStarManager:
    def __init__(self):
        self.shooting_star = None
        self.timer = 0
        self.interval = random.randint(100, 300)

    def spawn_shooting_star(self, widget):
        """Spawn a shooting star with initial parameters."""
        start_position_options = [
            (-0.1, random.uniform(0.2, 0.8)),  # Coming from the left
            (1.1, random.uniform(0.2, 0.8)),  # Coming from the right
        ]
        start_x, start_y = random.choice(start_position_options)

        # Ensure the star travels mostly diagonally and covers a large portion of the screen
        dx = random.uniform(0.3, 0.7) * (-1 if start_x > 0 else 1)  # Control direction
        dy = random.uniform(0.3, 0.6)

        # Normalize direction vector to maintain speed consistency
        normalization_factor = (dx**2 + dy**2) ** 0.5
        dx /= normalization_factor
        dy /= normalization_factor

        self.shooting_star = {
            "x": start_x,
            "y": start_y,
            "dx": dx,
            "dy": dy,
            "size": random.uniform(5, 10),
            "speed": random.uniform(0.08, 0.13),  # Fast speed
            "tail": [],
            "prev_x": start_x,  # Store previous position for interpolation
            "prev_y": start_y,
            "tail_length": 30,  # Increase tail length for smoother follow-through
            "tail_opacity": 1.0,  # Keep track of tail opacity
            "off_screen": False,  # Track whether the star has moved off-screen
        }

    def animate_shooting_star(self):
        """Move the shooting star and manage its tail."""
        if self.shooting_star:
            star = self.shooting_star

            # Calculate movement
            new_x = star["x"] + (star["dx"] * star["speed"])
            new_y = star["y"] + (star["dy"] * star["speed"])

            # Add multiple points between the previous and new positions
            steps = 25  # Increased number of intermediate points
            for i in range(steps):
                interp_x = star["prev_x"] + (new_x - star["prev_x"]) * (i / steps)
                interp_y = star["prev_y"] + (new_y - star["prev_y"]) * (i / steps)
                star["tail"].append((interp_x, interp_y, star["size"]))

            # Update the star's current position and previous position
            star["prev_x"], star["prev_y"] = star["x"], star["y"]
            star["x"], star["y"] = new_x, new_y

            # Check if the star has moved off-screen
            if star["x"] < -0.1 or star["x"] > 1.1 or star["y"] > 1.1:
                star["off_screen"] = True

            # Limit the tail length and fade it out gradually after the star is off-screen
            if star["off_screen"]:
                star["tail_opacity"] -= 0.05  # Gradually reduce opacity
                if star["tail_opacity"] <= 0:  # Remove star after tail fades
                    self.shooting_star = None

            # Limit the tail length
            if len(star["tail"]) > star["tail_length"]:
                star["tail"].pop(0)

    def draw_shooting_star(self, painter: QPainter, widget: "QWidget"):
        """Draw the shooting star and its smooth tail."""
        if not self.shooting_star:
            return

        star = self.shooting_star

        # Draw the tail using gradient fading effect
        tail_length = len(star["tail"])
        for i, (tx, ty, size) in enumerate(star["tail"]):
            opacity = (i + 1) / tail_length * star["tail_opacity"]  # Tail fades out

            # Create a gradient for smooth fading
            gradient = QLinearGradient(
                int(tx * widget.width()),
                int(ty * widget.height()),
                int(star["x"] * widget.width()),
                int(star["y"] * widget.height()),
            )
            gradient.setColorAt(0.0, QColor(255, 255, 255, int(255 * opacity)))
            gradient.setColorAt(1.0, QColor(255, 255, 255, 0))

            painter.setBrush(QBrush(gradient))
            tail_x = int(tx * widget.width())
            tail_y = int(ty * widget.height())
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setOpacity(opacity)
            painter.drawEllipse(
                tail_x, tail_y, int(size * opacity), int(size * opacity)
            )

        # Draw the shooting star at the head of the tail, if still visible
        if not star["off_screen"]:
            star_x = int(star["x"] * widget.width())
            star_y = int(star["y"] * widget.height())
            painter.setOpacity(1.0)
            painter.setBrush(QColor(255, 255, 255))
            painter.drawEllipse(
                star_x,
                star_y,
                int(star["size"]),
                int(star["size"]),
            )

    def manage_shooting_star(self, widget):
        """Handle the timing of shooting star appearances."""
        self.timer += 1
        if not self.shooting_star and self.timer >= self.interval:
            self.spawn_shooting_star(widget)
            self.timer = 0
            self.interval = random.randint(100, 300)  # Randomize the interval
