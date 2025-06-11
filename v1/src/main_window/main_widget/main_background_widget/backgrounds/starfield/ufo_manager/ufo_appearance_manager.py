import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ufo_manager import UFOManager


class UFOAppearanceManager:
    def __init__(self, ufo_manager: "UFOManager"):
        self.ufo_manager = ufo_manager  # Access the UFOManager instance
        self.appearance_timer = 5
        self.active = False  # If the UFO is visible
        self.entering = False  # UFO is entering the screen

    def manage_appearance(self):
        """Handle UFO appearance and disappearance."""
        ufo = self.ufo_manager.ufo  # Access the UFOManager's ufo dictionary

        # If UFO is not active, manage the timer for its next appearance
        if not self.active:
            # Count down the appearance timer
            self.appearance_timer -= 1
            if self.appearance_timer <= 0:
                # UFO is about to appear
                self.active = True
                ufo["active"] = True  # UFO is now active
                ufo["fly_off"] = False  # Reset fly-off state
                self.entering = True  # UFO is entering from off-screen
                self.set_offscreen_entry(ufo)
                self.appearance_timer = random.randint(500, 1000)  # Reset the timer
                self.active_duration = random.randint(
                    300, 500
                )  # Ensure the UFO stays for a while

        # If UFO is active, handle its movement and active time
        elif self.active:
            ufo["active"] = True  # Ensure UFO state is updated
            self.active_duration -= 1  # Count down the active duration
            if self.active_duration <= 0 or ufo["fly_off"]:
                # Once the active duration is over, deactivate the UFO
                self.active = False
                ufo["active"] = False  # Set UFO state to inactive
                self.appearance_timer = random.randint(500, 1000)  # Reset the timer
                print("UFO is now inactive, disappearing.")

    def set_offscreen_entry(self, ufo):
        """Initialize the UFO's entry from off-screen for a straight fly-by."""
        entry_side = random.choice(["left", "right", "top", "bottom"])
        if entry_side == "left":
            ufo["x"] = -0.1  # Start off-screen to the left
            ufo["y"] = random.uniform(0.2, 0.8)  # Fly across the middle
            ufo["dx"] = random.uniform(0.01, 0.02)  # Move right
            ufo["dy"] = 0  # Fly in a straight line horizontally
        elif entry_side == "right":
            ufo["x"] = 1.1  # Start off-screen to the right
            ufo["y"] = random.uniform(0.2, 0.8)
            ufo["dx"] = -random.uniform(0.01, 0.02)  # Move left
            ufo["dy"] = 0  # Fly in a straight line horizontally
        elif entry_side == "top":
            ufo["x"] = random.uniform(0.2, 0.8)  # Fly across the middle
            ufo["y"] = -0.1  # Start off-screen above
            ufo["dy"] = random.uniform(0.01, 0.02)  # Move down
            ufo["dx"] = 0  # Fly in a straight line vertically
        elif entry_side == "bottom":
            ufo["x"] = random.uniform(0.2, 0.8)
            ufo["y"] = 1.1  # Start off-screen below
            ufo["dy"] = -random.uniform(0.01, 0.02)  # Move up
            ufo["dx"] = 0  # Fly in a straight line vertically
