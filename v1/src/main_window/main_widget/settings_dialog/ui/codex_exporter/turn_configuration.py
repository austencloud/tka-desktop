from typing import Dict, List, Optional, Set, Tuple
import os


class TurnConfiguration:

    @staticmethod
    def get_turn_combinations() -> List[Tuple[float, float]]:
        """Get all possible turn combinations.

        Returns:
            A list of (red_turns, blue_turns) tuples
        """
        turn_values = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        return [(red, blue) for red in turn_values for blue in turn_values]

    @staticmethod
    def get_turn_directory_name(
        red_turns: float, blue_turns: float, letter: str = None
    ) -> str:
        """Get the directory name for a turn combination.

        Args:
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
            letter: The letter (optional, used to determine Type1/Type2)

        Returns:
            The directory name
        """
        # Format turn values with .0 for whole numbers and .5 for half turns
        red_turns_str = f"{red_turns:.1f}".replace(".0", "")
        blue_turns_str = f"{blue_turns:.1f}".replace(".0", "")

        # Create the master folder name with turn values in parentheses
        master_dir = f"({red_turns_str},{blue_turns_str})"

        # If letter is provided, add Type1/Type2 subfolder
        if letter and TurnConfiguration.is_type2_letter(letter):
            return os.path.join(master_dir, "Type2")
        elif letter and TurnConfiguration.is_type3_letter(letter):
            return os.path.join(master_dir, "Type3")
        elif letter:
            return os.path.join(master_dir, "Type1")
        else:
            return master_dir

    @staticmethod
    def get_hybrid_filename(
        letter: str,
        red_turns: float,
        blue_turns: float,
        motion_type: Optional[str] = None,
    ) -> str:
        """Get the filename for a hybrid pictograph.

        Args:
            letter: The letter
            red_turns: The number of turns for the red hand
            blue_turns: The number of turns for the blue hand
            motion_type: The motion type, which can be:
                - "pro_red" (red=pro, blue=anti)
                - "pro_blue" (red=anti, blue=pro)
                - "normal" (for S, T, U, V: red=red_turns, blue=blue_turns)
                - "swapped" (for S, T, U, V: red=blue_turns, blue=red_turns)
                - "same" (for Type 2: clockwise rotation)
                - "opp" (for Type 2: counter-clockwise rotation)
                - "pro_turns" (legacy: pro hand has turns, anti hand has 0 turns)
                - "anti_turns" (legacy: pro hand has 0 turns, anti hand has turns)

        Returns:
            The filename
        """
        # Format turn values with .0 for whole numbers and .5 for half turns
        red_turns_str = f"{red_turns:.1f}".replace(".0", "")
        blue_turns_str = f"{blue_turns:.1f}".replace(".0", "")

        # Handle Type 2 letters differently
        if TurnConfiguration.is_type2_letter(
            letter
        ) or TurnConfiguration.is_type3_letter(letter):
            if red_turns == blue_turns:
                # If turns are the same, we only need one version
                return f"{letter}.png"
            elif motion_type in ["same", "opp"]:
                # For Type 2 letters with rotation direction variants
                return f"{letter}_{motion_type}_{red_turns_str}_{blue_turns_str}.png"
            else:
                # Default for Type 2
                return f"{letter}_{red_turns_str}_{blue_turns_str}.png"
        else:
            # Original Type 1 handling
            if red_turns == blue_turns:
                # If turns are the same, we only need one version
                return f"{letter}.png"
            else:
                # If turns are different, we need to specify which variation
                if motion_type == "pro_red":
                    return f"{letter}_red_pro_blue_anti.png"
                elif motion_type == "pro_blue":
                    return f"{letter}_red_anti_blue_pro.png"
                elif motion_type == "normal":
                    # For S, T, U, V: normal turn order
                    return f"{letter}_turns_{red_turns_str}_{blue_turns_str}.png"
                elif motion_type == "swapped":
                    # For S, T, U, V: swapped turn order
                    return (
                        f"{letter}_turns_{blue_turns_str}_{red_turns_str}_swapped.png"
                    )
                elif motion_type == "pro_turns":
                    # Legacy support
                    return f"{letter}_pro_turns.png"
                elif motion_type == "anti_turns":
                    # Legacy support
                    return f"{letter}_anti_turns.png"
                else:
                    # Fallback for backward compatibility
                    return f"{letter}_{motion_type}.png"

    @staticmethod
    def get_non_hybrid_filename(letter: str) -> str:
        return f"{letter}.png"

    # Group letters by their start/end positions to reduce repetition in definition
    _POSITION_GROUPS: Dict[Tuple[str, str], List[str]] = {
        # Type 1 letters
        ("alpha1", "alpha3"): ["A", "B", "C"],
        ("beta1", "alpha3"): ["D", "E", "F"],
        ("beta3", "beta5"): ["G", "H", "I"],
        ("alpha3", "beta5"): ["J", "K", "L"],
        ("gamma11", "gamma1"): ["M", "N", "O"],
        ("gamma1", "gamma15"): ["P", "Q", "R"],
        ("gamma13", "gamma11"): ["S", "T", "U", "V"],
        # Type 2 letters
        ("gamma13", "alpha3"): ["W", "X"],
        ("gamma11", "beta5"): ["Y", "Z"],
        ("alpha3", "gamma13"): ["Σ", "Δ"],
        ("beta7", "gamma13"): ["θ", "Ω"],
        # Type 3 letters
        ("gamma5", "alpha3"): ["W-", "X-"],
        ("gamma3", "beta5"): ["Y-", "Z-"],
        ("beta3", "gamma13"): ["Σ-", "Δ-"],
        ("alpha7", "gamma13"): ["θ-", "Ω-"],
    }

    # Create the reverse map (letter -> positions) for efficient lookups
    # This is generated once when the class is defined.
    _LETTER_POSITIONS_MAP: Dict[str, Tuple[str, str]] = {
        letter: positions
        for positions, letters in _POSITION_GROUPS.items()
        for letter in letters
    }

    # Define hybrid letters using a set for efficient O(1) average time complexity lookup
    _HYBRID_LETTERS: Set[str] = {
        "C",
        "F",
        "I",
        "L",
        "O",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "Σ",
        "Δ",
        "θ",
        "Ω",
    }

    # Define Type 2 letters that need special handling
    _TYPE2_LETTERS: Set[str] = {"W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"}
    _TYPE3_LETTERS: Set[str] = {"W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"}

    @staticmethod
    def is_hybrid_letter(letter: str) -> bool:
        """Checks if a letter corresponds to a hybrid motion."""
        return letter in TurnConfiguration._HYBRID_LETTERS

    @staticmethod
    def is_type2_letter(letter: str) -> bool:
        """Checks if a letter is a Type 2 letter (W, X, Y, Z, Σ, Δ, θ, Ω)."""
        return letter in TurnConfiguration._TYPE2_LETTERS

    @staticmethod
    def is_type3_letter(letter: str) -> bool:
        """Checks if a letter is a Type 3 letter (W-, X-, Y-, Z-, Σ-, Δ-, θ-, Ω-)."""
        return letter in TurnConfiguration._TYPE3_LETTERS

    @staticmethod
    def get_letter_positions(letter: str) -> Optional[Tuple[str, str]]:
        """Returns the start and end positions for a given letter using an efficient map lookup."""
        # O(1) average time complexity lookup
        return TurnConfiguration._LETTER_POSITIONS_MAP.get(letter)
