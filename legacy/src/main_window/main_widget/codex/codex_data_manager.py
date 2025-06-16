# pictograph_data_manager.py

from typing import TYPE_CHECKING, Optional
from enums.letter.letter import Letter

from data.constants import *

if TYPE_CHECKING:
    from .codex import Codex
from enums.letter.letter import Letter


RED = "red"
BLUE = "blue"
MOTION_TYPE = "motion_type"


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
                try:
                    # Get PictographDataLoader from dependency injection
                    from main_window.main_widget.pictograph_data_loader import (
                        PictographDataLoader,
                    )

                    pictograph_data_loader = self.main_widget.app_context.get_service(
                        PictographDataLoader
                    )
                    current_data = pictograph_data_loader.find_pictograph_data(
                        {
                            LETTER: letter,
                            START_POS: data[START_POS],
                            END_POS: data[END_POS],
                            f"{BLUE}_{MOTION_TYPE}": data[f"{BLUE}_{MOTION_TYPE}"],
                            f"{RED}_{MOTION_TYPE}": data[f"{RED}_{MOTION_TYPE}"],
                        }
                    )
                except (AttributeError, KeyError):
                    # Fallback if service not available
                    current_data = None
                pictograph_data[letter] = current_data
            else:
                pictograph_data[letter] = None  # Or handle as needed

        return pictograph_data

    def _get_pictograph_data(self, letter: str) -> Optional[dict]:
        """Returns the parameters for a given letter."""
        params_map = {
            "A": {
                START_POS: ALPHA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "B": {
                START_POS: ALPHA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "C": {
                START_POS: ALPHA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "D": {
                START_POS: BETA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "E": {
                START_POS: BETA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "F": {
                START_POS: BETA1,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "G": {
                START_POS: BETA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "H": {
                START_POS: BETA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "I": {
                START_POS: BETA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "J": {
                START_POS: ALPHA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "K": {
                START_POS: ALPHA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "L": {
                START_POS: ALPHA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "M": {
                START_POS: GAMMA11,
                END_POS: GAMMA1,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "N": {
                START_POS: GAMMA11,
                END_POS: GAMMA1,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "O": {
                START_POS: GAMMA11,
                END_POS: GAMMA1,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "P": {
                START_POS: GAMMA1,
                END_POS: GAMMA15,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Q": {
                START_POS: GAMMA1,
                END_POS: GAMMA15,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "R": {
                START_POS: GAMMA1,
                END_POS: GAMMA15,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "S": {
                START_POS: GAMMA13,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "T": {
                START_POS: GAMMA13,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "U": {
                START_POS: GAMMA13,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": ANTI,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "V": {
                START_POS: GAMMA13,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": PRO,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "W": {
                START_POS: GAMMA13,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "X": {
                START_POS: GAMMA13,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Y": {
                START_POS: GAMMA11,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Z": {
                START_POS: GAMMA11,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Σ": {
                START_POS: ALPHA3,
                END_POS: GAMMA13,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Δ": {
                START_POS: ALPHA3,
                END_POS: GAMMA13,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "θ": {
                START_POS: BETA5,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Ω": {
                START_POS: BETA5,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "W-": {
                START_POS: GAMMA5,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "X-": {
                START_POS: GAMMA5,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Y-": {
                START_POS: GAMMA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Z-": {
                START_POS: GAMMA3,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Σ-": {
                START_POS: BETA3,
                END_POS: GAMMA13,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Δ-": {
                START_POS: BETA3,
                END_POS: GAMMA13,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "θ-": {
                START_POS: ALPHA5,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": PRO,
            },
            "Ω-": {
                START_POS: ALPHA5,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": ANTI,
            },
            "Φ": {
                START_POS: BETA7,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Ψ": {
                START_POS: ALPHA1,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Λ": {
                START_POS: GAMMA7,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Φ-": {
                START_POS: ALPHA3,
                END_POS: ALPHA7,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Ψ-": {
                START_POS: BETA1,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "Λ-": {
                START_POS: GAMMA15,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": DASH,
                f"{RED}_{MOTION_TYPE}": DASH,
            },
            "α": {
                START_POS: ALPHA3,
                END_POS: ALPHA3,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": STATIC,
            },
            "β": {
                START_POS: BETA5,
                END_POS: BETA5,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": STATIC,
            },
            "Γ": {
                START_POS: GAMMA11,
                END_POS: GAMMA11,
                f"{BLUE}_{MOTION_TYPE}": STATIC,
                f"{RED}_{MOTION_TYPE}": STATIC,
            },
            # Add more letters and their parameters as needed
        }

        return params_map.get(letter)

    def get_pictograph_data(self) -> dict[str, Optional[dict]]:
        """Returns the initialized pictograph data."""
        return self.pictograph_data
