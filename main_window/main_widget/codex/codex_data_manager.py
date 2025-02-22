# pictograph_data_manager.py

from typing import TYPE_CHECKING, Optional
from Enums.letters import Letter

if TYPE_CHECKING:
    from .codex import Codex
from Enums.letters import Letter


class CodexDataManager:
    """Manages the initialization and retrieval of pictograph data."""

    def __init__(self, codex: "Codex"):
        self.main_widget = codex.main_widget
        self.pictograph_data: dict[str, Optional[dict]] = (
            self._initialize_pictograph_data()
        )

    def _initialize_pictograph_data(self) -> dict[str, Optional[dict]]:
        """Initializes the pictograph data for all letters."""
        letters = [letter.value for letter in Letter]

        pictograph_data = {}
        for letter in letters:
            data = self._get_pictograph_data(letter)
            if data:
                current_data = (
                    self.main_widget.pictograph_data_loader.find_pictograph_data(
                        {
                            "letter": letter,
                            "start_pos": data["start_pos"],
                            "end_pos": data["end_pos"],
                            "blue_motion_type": data["blue_motion_type"],
                            "red_motion_type": data["red_motion_type"],
                        }
                    )
                )
                pictograph_data[letter] = current_data
            else:
                pictograph_data[letter] = None  # Or handle as needed

        return pictograph_data

    def _get_pictograph_data(self, letter: str) -> Optional[dict]:
        """Returns the parameters for a given letter."""
        params_map = {
            "A": {
                "start_pos": "alpha1",
                "end_pos": "alpha3",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "B": {
                "start_pos": "alpha1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "C": {
                "start_pos": "alpha1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "D": {
                "start_pos": "beta1",
                "end_pos": "alpha3",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "E": {
                "start_pos": "beta1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "F": {
                "start_pos": "beta1",
                "end_pos": "alpha3",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "G": {
                "start_pos": "beta3",
                "end_pos": "beta5",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "H": {
                "start_pos": "beta3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "I": {
                "start_pos": "beta3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "J": {
                "start_pos": "alpha3",
                "end_pos": "beta5",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "K": {
                "start_pos": "alpha3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "L": {
                "start_pos": "alpha3",
                "end_pos": "beta5",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "M": {
                "start_pos": "gamma13",
                "end_pos": "gamma3",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "N": {
                "start_pos": "gamma13",
                "end_pos": "gamma3",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "O": {
                "start_pos": "gamma13",
                "end_pos": "gamma3",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "P": {
                "start_pos": "gamma3",
                "end_pos": "gamma9",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "Q": {
                "start_pos": "gamma3",
                "end_pos": "gamma9",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "R": {
                "start_pos": "gamma3",
                "end_pos": "gamma9",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "S": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "pro",
                "red_motion_type": "pro",
            },
            "T": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "anti",
                "red_motion_type": "anti",
            },
            "U": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "anti",
                "red_motion_type": "pro",
            },
            "V": {
                "start_pos": "gamma13",
                "end_pos": "gamma11",
                "blue_motion_type": "pro",
                "red_motion_type": "anti",
            },
            "W": {
                "start_pos": "gamma13",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "X": {
                "start_pos": "gamma13",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "Y": {
                "start_pos": "gamma11",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "Z": {
                "start_pos": "gamma11",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "Σ": {
                "start_pos": "alpha3",
                "end_pos": "gamma13",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "Δ": {
                "start_pos": "alpha3",
                "end_pos": "gamma13",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "θ": {
                "start_pos": "beta5",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "pro",
            },
            "Ω": {
                "start_pos": "beta5",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "anti",
            },
            "W-": {
                "start_pos": "gamma5",
                "end_pos": "alpha3",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "X-": {
                "start_pos": "gamma5",
                "end_pos": "alpha3",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "Y-": {
                "start_pos": "gamma3",
                "end_pos": "beta5",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "Z-": {
                "start_pos": "gamma3",
                "end_pos": "beta5",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "Σ-": {
                "start_pos": "beta3",
                "end_pos": "gamma13",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "Δ-": {
                "start_pos": "beta3",
                "end_pos": "gamma13",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "θ-": {
                "start_pos": "alpha5",
                "end_pos": "gamma11",
                "blue_motion_type": "dash",
                "red_motion_type": "pro",
            },
            "Ω-": {
                "start_pos": "alpha5",
                "end_pos": "gamma11",
                "blue_motion_type": "dash",
                "red_motion_type": "anti",
            },
            "Φ": {
                "start_pos": "beta7",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "dash",
            },
            "Ψ": {
                "start_pos": "alpha1",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "dash",
            },
            "Λ": {
                "start_pos": "gamma7",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "dash",
            },
            "Φ-": {
                "start_pos": "alpha3",
                "end_pos": "alpha7",
                "blue_motion_type": "dash",
                "red_motion_type": "dash",
            },
            "Ψ-": {
                "start_pos": "beta1",
                "end_pos": "beta5",
                "blue_motion_type": "dash",
                "red_motion_type": "dash",
            },
            "Λ-": {
                "start_pos": "gamma15",
                "end_pos": "gamma11",
                "blue_motion_type": "dash",
                "red_motion_type": "dash",
            },
            "α": {
                "start_pos": "alpha3",
                "end_pos": "alpha3",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            "β": {
                "start_pos": "beta5",
                "end_pos": "beta5",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            "Γ": {
                "start_pos": "gamma11",
                "end_pos": "gamma11",
                "blue_motion_type": "static",
                "red_motion_type": "static",
            },
            # Add more letters and their parameters as needed
        }

        return params_map.get(letter)

    def get_pictograph_data(self) -> dict[str, Optional[dict]]:
        """Returns the initialized pictograph data."""
        return self.pictograph_data
