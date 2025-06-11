from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .ufo_manager import UFOManager


class UFOMovementManager:
    def __init__(self, ufo_manager: "UFOManager"):
        self.ufo_manager = ufo_manager  # Access the UFOManager instance

    def move_ufo(self):
        """Move the UFO based on its movement type."""
        ufo = self.ufo_manager.ufo  # Access the UFOManager's ufo dictionary
        appearance_manager = self.ufo_manager.ufo_appearance_manager

        if ufo["active"] and not ufo["fly_off"]:
            ufo["x"] += ufo["dx"] * ufo["speed"]
            ufo["y"] += ufo["dy"] * ufo["speed"]

            # If the UFO moves out of bounds, mark it as inactive
            if ufo["x"] < -0.1 or ufo["x"] > 1.1 or ufo["y"] < -0.1 or ufo["y"] > 1.1:
                appearance_manager.active = False  # UFO has exited the screen
                ufo["active"] = False  # Deactivate UFO
