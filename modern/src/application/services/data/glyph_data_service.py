"""
Glyph Data Service for Kinetic Constructor

This service determines glyph information (VTG mode, elemental type, letter type, etc.)
from beat data and motion information, following validated glyph classification logic.
"""

from typing import Optional, Dict, Any
from domain.models.core_models import (
    BeatData,
    GlyphData,
    VTGMode,
    ElementalType,
    LetterType,
    MotionData,
    Location,
)


class GlyphDataService:
    """Service for determining glyph data from beat information."""

    # Complete mapping from letters to letter types
    LETTER_TYPE_MAP = {
        # TYPE1 letters (Dual-Shift: A-V)
        "A": LetterType.TYPE1,
        "B": LetterType.TYPE1,
        "C": LetterType.TYPE1,
        "D": LetterType.TYPE1,
        "E": LetterType.TYPE1,
        "F": LetterType.TYPE1,
        "G": LetterType.TYPE1,
        "H": LetterType.TYPE1,
        "I": LetterType.TYPE1,
        "J": LetterType.TYPE1,
        "K": LetterType.TYPE1,
        "L": LetterType.TYPE1,
        "M": LetterType.TYPE1,
        "N": LetterType.TYPE1,
        "O": LetterType.TYPE1,
        "P": LetterType.TYPE1,
        "Q": LetterType.TYPE1,
        "R": LetterType.TYPE1,
        "S": LetterType.TYPE1,
        "T": LetterType.TYPE1,
        "U": LetterType.TYPE1,
        "V": LetterType.TYPE1,
        # TYPE2 letters (Shift: W,X,Y,Z,Σ,Δ,θ,Ω)
        "W": LetterType.TYPE2,
        "X": LetterType.TYPE2,
        "Y": LetterType.TYPE2,
        "Z": LetterType.TYPE2,
        "Σ": LetterType.TYPE2,
        "Δ": LetterType.TYPE2,
        "θ": LetterType.TYPE2,
        "Ω": LetterType.TYPE2,
        # TYPE3 letters (Cross-Shift: W-,X-,Y-,Z-,Σ-,Δ-,θ-,Ω-)
        "W-": LetterType.TYPE3,
        "X-": LetterType.TYPE3,
        "Y-": LetterType.TYPE3,
        "Z-": LetterType.TYPE3,
        "Σ-": LetterType.TYPE3,
        "Δ-": LetterType.TYPE3,
        "θ-": LetterType.TYPE3,
        "Ω-": LetterType.TYPE3,
        # TYPE4 letters (Dash: Φ,Ψ,Λ)
        "Φ": LetterType.TYPE4,
        "Ψ": LetterType.TYPE4,
        "Λ": LetterType.TYPE4,
        # TYPE5 letters (Dual-Dash: Φ-,Ψ-,Λ-)
        "Φ-": LetterType.TYPE5,
        "Ψ-": LetterType.TYPE5,
        "Λ-": LetterType.TYPE5,
        # TYPE6 letters (Static: α,β,Γ)
        "α": LetterType.TYPE6,
        "β": LetterType.TYPE6,
        "Γ": LetterType.TYPE6,
    }

    def determine_glyph_data(self, beat_data: BeatData) -> Optional[GlyphData]:
        """
        Determine glyph data from beat information.

        Args:
            beat_data: The beat data to analyze

        Returns:
            GlyphData with determined glyph information, or None if no glyphs needed
        """
        if beat_data.is_blank or not beat_data.letter:
            return None

        # Determine letter type
        letter_type = self._determine_letter_type(beat_data.letter)

        # Determine VTG mode
        vtg_mode = self._determine_vtg_mode(beat_data)

        # Determine if letter has dash
        has_dash = "-" in beat_data.letter if beat_data.letter else False

        # Determine start and end positions
        start_position, end_position = self._determine_positions(beat_data)

        return GlyphData(
            vtg_mode=vtg_mode,
            elemental_type=self._vtg_to_elemental(vtg_mode),
            letter_type=letter_type,
            has_dash=has_dash,
            turns_data=None,  # TODO: Implement turns data parsing
            start_position=start_position,
            end_position=end_position,
            show_elemental=letter_type == LetterType.TYPE1,
            show_vtg=letter_type == LetterType.TYPE1,
            show_tka=True,
            show_positions=letter_type != LetterType.TYPE6,  # Don't show for α, β, Γ
        )

    def _determine_letter_type(self, letter: str) -> Optional[LetterType]:
        """Determine the letter type from the letter string."""
        # Use the full letter string (not just first character) for compound letters like "W-"
        return self.LETTER_TYPE_MAP.get(letter)

    def _determine_vtg_mode(self, beat_data: BeatData) -> Optional[VTGMode]:
        """
        Determine VTG mode from motion data.

        This is a simplified implementation. The full logic is quite complex
        and involves grid mode checking, position analysis, etc.
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return None

        blue_motion = beat_data.blue_motion
        red_motion = beat_data.red_motion

        # Simplified VTG determination based on motion patterns
        # This would need to be expanded with the full classification logic

        # Check if motions are in same or opposite directions
        same_direction = self._motions_same_direction(blue_motion, red_motion)

        # Check if motions are split, together, or quarter
        motion_pattern = self._determine_motion_pattern(blue_motion, red_motion)

        if motion_pattern == "split":
            return VTGMode.SPLIT_SAME if same_direction else VTGMode.SPLIT_OPP
        elif motion_pattern == "together":
            return VTGMode.TOG_SAME if same_direction else VTGMode.TOG_OPP
        elif motion_pattern == "quarter":
            return VTGMode.QUARTER_SAME if same_direction else VTGMode.QUARTER_OPP

        return VTGMode.SPLIT_SAME  # Default fallback

    def _motions_same_direction(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if two motions are in the same direction."""
        # Simplified check - would need full directional logic
        return blue_motion.prop_rot_dir == red_motion.prop_rot_dir

    def _determine_motion_pattern(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> str:
        """Determine if motions are split, together, or quarter pattern."""
        # Simplified pattern detection - would need full pattern analysis logic
        blue_start = blue_motion.start_loc
        red_start = red_motion.start_loc

        # Basic pattern detection based on starting locations
        opposite_locations = {
            Location.NORTH: Location.SOUTH,
            Location.SOUTH: Location.NORTH,
            Location.EAST: Location.WEST,
            Location.WEST: Location.EAST,
        }

        if red_start == opposite_locations.get(blue_start):
            return "split"
        elif blue_start == red_start:
            return "together"
        else:
            return "quarter"

    def _vtg_to_elemental(self, vtg_mode: Optional[VTGMode]) -> Optional[ElementalType]:
        """Convert VTG mode to elemental type."""
        if not vtg_mode:
            return None

        mapping = {
            VTGMode.SPLIT_SAME: ElementalType.WATER,
            VTGMode.SPLIT_OPP: ElementalType.FIRE,
            VTGMode.TOG_SAME: ElementalType.EARTH,
            VTGMode.TOG_OPP: ElementalType.AIR,
            VTGMode.QUARTER_SAME: ElementalType.SUN,
            VTGMode.QUARTER_OPP: ElementalType.MOON,
        }
        return mapping.get(vtg_mode)

    def _determine_positions(
        self, beat_data: BeatData
    ) -> tuple[Optional[str], Optional[str]]:
        """Determine start and end positions from motion data."""
        if not beat_data.blue_motion or not beat_data.red_motion:
            return None, None

        # For now, use blue motion's start and end locations
        # This would need more sophisticated logic in the full implementation
        blue_motion = beat_data.blue_motion

        # Map locations to position names
        location_to_position = {
            Location.NORTH: "alpha",
            Location.EAST: "beta",
            Location.SOUTH: "gamma",
            Location.WEST: "alpha",  # Simplified mapping
        }

        start_pos = location_to_position.get(blue_motion.start_loc)
        end_pos = location_to_position.get(blue_motion.end_loc)

        return start_pos, end_pos
