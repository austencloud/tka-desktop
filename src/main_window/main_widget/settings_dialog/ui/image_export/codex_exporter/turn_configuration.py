from typing import TYPE_CHECKING, Dict, Any, Optional, List, Tuple
from typing import Dict, List, Optional, Set, Tuple


class TurnConfiguration:

    @staticmethod
    def get_turn_combinations() -> List[Tuple[int, int]]:
        return [(red, blue) for red in range(4) for blue in range(4)]

    @staticmethod
    def get_turn_directory_name(red_turns: int, blue_turns: int) -> str:
        return f"red{red_turns}_blue{blue_turns}"

    @staticmethod
    def get_hybrid_filename(
        letter: str, red_turns: int, blue_turns: int, motion_type: Optional[str] = None
    ) -> str:
        """Get the filename for a hybrid pictograph.

        Args:
            letter: The letter
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
            motion_type: The motion type, which can be:
                - "pro_turns" (pro hand has turns, anti hand has 0 turns)
                - "anti_turns" (pro hand has 0 turns, anti hand has turns)

        Returns:
            The filename
        """
        if red_turns == blue_turns:
            # If turns are the same, we only need one version
            return f"{letter}.png"
        else:
            # If turns are different, we need to specify which hand has turns
            if motion_type == "pro_turns":
                return f"{letter}_pro_turns.png"
            elif motion_type == "anti_turns":
                return f"{letter}_anti_turns.png"
            else:
                # Fallback for backward compatibility
                return f"{letter}_{motion_type}.png"

    @staticmethod
    def get_non_hybrid_filename(letter: str) -> str:
        return f"{letter}.png"

    # Group letters by their start/end positions to reduce repetition in definition
    _POSITION_GROUPS: Dict[Tuple[str, str], List[str]] = {
        ("alpha1", "alpha3"): ["A", "B", "C"],
        ("beta1", "alpha3"): ["D", "E", "F"],
        ("beta3", "beta5"): ["G", "H", "I"],
        ("alpha3", "beta5"): ["J", "K", "L"],
        ("gamma11", "gamma1"): ["M", "N", "O"],
        ("gamma1", "gamma15"): ["P", "Q", "R"],
        ("gamma13", "gamma11"): ["S", "T", "U", "V"],
    }

    # Create the reverse map (letter -> positions) for efficient lookups
    # This is generated once when the class is defined.
    _LETTER_POSITIONS_MAP: Dict[str, Tuple[str, str]] = {
        letter: positions
        for positions, letters in _POSITION_GROUPS.items()
        for letter in letters
    }

    # Define hybrid letters using a set for efficient O(1) average time complexity lookup
    _HYBRID_LETTERS: Set[str] = {"C", "F", "I", "L", "O", "R", "U", "V"}

    @staticmethod
    def is_hybrid_letter(letter: str) -> bool:
        """Checks if a letter corresponds to a hybrid motion."""
        return letter in TurnConfiguration._HYBRID_LETTERS

    @staticmethod
    def get_letter_positions(letter: str) -> Optional[Tuple[str, str]]:
        """Returns the start and end positions for a given letter using an efficient map lookup."""
        # O(1) average time complexity lookup
        return TurnConfiguration._LETTER_POSITIONS_MAP.get(letter)
