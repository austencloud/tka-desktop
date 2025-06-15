"""
Pictograph Management Service

Consolidated pictograph management service that handles all pictograph-related
operations including creation, updates, dataset management, and data conversion.

REPLACES AND CONSOLIDATES:
- Various pictograph service wrappers
- Fragmented pictograph logic across multiple files

PROVIDES:
- Unified pictograph management interface
- Dataset operations and querying
- V1 to V2 data conversion
- Context-aware pictograph configuration
- CSV data loading and pictograph creation
"""

from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod
from enum import Enum
import uuid
from pathlib import Path

import pandas as pd

from domain.models.core_models import (
    BeatData,
    MotionData,
    MotionType,
    Location,
    RotationDirection,
    GlyphData,
    VTGMode,
    ElementalType,
    LetterType,
)
from domain.models.pictograph_models import (
    PictographData,
    GridData,
    GridMode,
    ArrowData,
    PropData,
)


class IPictographManagementService(ABC):
    """Unified interface for all pictograph management operations."""

    @abstractmethod
    def create_pictograph(
        self, grid_mode: GridMode = GridMode.DIAMOND
    ) -> PictographData:
        """Create a new blank pictograph."""
        pass

    @abstractmethod
    def create_from_beat(self, beat_data: BeatData) -> PictographData:
        """Create pictograph from beat data."""
        pass

    @abstractmethod
    def update_pictograph_arrows(
        self, pictograph: PictographData, arrows: Dict[str, ArrowData]
    ) -> PictographData:
        """Update arrows in pictograph."""
        pass

    @abstractmethod
    def search_dataset(self, query: Dict[str, Any]) -> List[PictographData]:
        """Search pictograph dataset with query."""
        pass

    @abstractmethod
    def convert_v1_to_v2(self, v1_data: Dict[str, Any]) -> PictographData:
        """Convert V1 pictograph data to V2 format."""
        pass


class PictographContext(Enum):
    """Pictograph context types."""

    SEQUENCE_EDITOR = "sequence_editor"
    STANDALONE_VIEWER = "standalone_viewer"
    DICTIONARY_BROWSER = "dictionary_browser"
    COMPARISON_VIEW = "comparison_view"


class PictographManagementService(IPictographManagementService):
    """
    Unified pictograph management service consolidating all pictograph operations.

    Provides comprehensive pictograph management including:
    - Pictograph creation and manipulation
    - Dataset management and querying
    - Data conversion between V1 and V2 formats
    - Context-aware configuration
    - Glyph data handling
    """

    def __init__(self):
        # Dataset management
        self._pictograph_cache: Dict[str, PictographData] = {}
        self._dataset_index: Dict[str, List[str]] = {}

        # CSV data loading
        self._csv_data = None
        # Path from v2/src/application/services/core/ to project root data/
        self._data_path = (
            Path(__file__).parent.parent.parent.parent.parent.parent
            / "data"
            / "DiamondPictographDataframe.csv"
        )

        # Context configuration
        self._context_configs = self._load_context_configs()

        # Glyph data
        self._glyph_mappings = self._load_glyph_mappings()

        # V1 conversion mappings
        self._v1_conversion_rules = self._load_v1_conversion_rules()

    def create_pictograph(
        self, grid_mode: GridMode = GridMode.DIAMOND
    ) -> PictographData:
        """Create a new blank pictograph."""
        grid_data = GridData(
            grid_mode=grid_mode,
            center_x=200.0,
            center_y=200.0,
            radius=100.0,
        )

        return PictographData(
            grid_data=grid_data,
            arrows={},
            props={},
            is_blank=True,
            metadata={"created_by": "pictograph_management_service"},
        )

    def create_from_beat(self, beat_data: BeatData) -> PictographData:
        """Create pictograph from beat data."""
        pictograph = self.create_pictograph()

        # Add arrows based on beat motions
        arrows = {}

        if beat_data.blue_motion:
            arrows["blue"] = ArrowData(
                color="blue",
                motion_data=beat_data.blue_motion,
                is_visible=True,
            )

        if beat_data.red_motion:
            arrows["red"] = ArrowData(
                color="red",
                motion_data=beat_data.red_motion,
                is_visible=True,
            )

        return pictograph.update(
            arrows=arrows,
            is_blank=len(arrows) == 0,
            metadata={
                "created_from_beat": beat_data.beat_number,
                "letter": beat_data.letter,
            },
        )

    def update_pictograph_arrows(
        self, pictograph: PictographData, arrows: Dict[str, ArrowData]
    ) -> PictographData:
        """Update arrows in pictograph."""
        return pictograph.update(
            arrows=arrows,
            is_blank=len(arrows) == 0,
        )

    def search_dataset(self, query: Dict[str, Any]) -> List[PictographData]:
        """Search pictograph dataset with query."""
        results = []

        # Extract search criteria
        letter = query.get("letter")
        motion_type = query.get("motion_type")
        start_position = query.get("start_position")
        max_results = query.get("max_results", 50)

        # Search through cached pictographs
        for pictograph_id, pictograph in self._pictograph_cache.items():
            if self._matches_query(pictograph, query):
                results.append(pictograph)

                if len(results) >= max_results:
                    break

        return results

    def convert_v1_to_v2(self, v1_data: Dict[str, Any]) -> PictographData:
        """Convert V1 pictograph data to V2 format."""
        # Create base pictograph
        pictograph = self.create_pictograph()

        # Convert V1 arrows to V2 format
        arrows = {}

        if "blue_arrow" in v1_data:
            blue_motion = self._convert_v1_motion(v1_data["blue_arrow"])
            if blue_motion:
                arrows["blue"] = ArrowData(
                    color="blue",
                    motion_data=blue_motion,
                    is_visible=True,
                )

        if "red_arrow" in v1_data:
            red_motion = self._convert_v1_motion(v1_data["red_arrow"])
            if red_motion:
                arrows["red"] = ArrowData(
                    color="red",
                    motion_data=red_motion,
                    is_visible=True,
                )

        # Convert metadata
        metadata = {
            "converted_from_v1": True,
            "original_v1_id": v1_data.get("id"),
            "conversion_timestamp": str(uuid.uuid4()),
        }

        return pictograph.update(
            arrows=arrows,
            is_blank=len(arrows) == 0,
            metadata=metadata,
        )

    def configure_for_context(
        self, pictograph: PictographData, context: PictographContext
    ) -> PictographData:
        """Configure pictograph for specific context."""
        context_config = self._context_configs.get(context, {})

        # Apply context-specific modifications
        metadata = pictograph.metadata.copy()
        metadata.update(
            {
                "context": context.value,
                "context_config": context_config,
            }
        )

        return pictograph.update(metadata=metadata)

    def get_glyph_for_pictograph(self, pictograph: PictographData) -> Optional[str]:
        """Get glyph representation for pictograph."""
        # Generate glyph key based on pictograph content
        glyph_key = self._generate_glyph_key(pictograph)
        return self._glyph_mappings.get(glyph_key)

    def add_to_dataset(
        self, pictograph: PictographData, category: str = "user_created"
    ) -> str:
        """Add pictograph to dataset."""
        pictograph_id = str(uuid.uuid4())

        # Cache the pictograph
        self._pictograph_cache[pictograph_id] = pictograph

        # Update dataset index
        if category not in self._dataset_index:
            self._dataset_index[category] = []
        self._dataset_index[category].append(pictograph_id)

        return pictograph_id

    def get_dataset_categories(self) -> List[str]:
        """Get all available dataset categories."""
        return list(self._dataset_index.keys())

    def get_pictographs_by_category(self, category: str) -> List[PictographData]:
        """Get all pictographs in a category."""
        pictograph_ids = self._dataset_index.get(category, [])
        return [
            self._pictograph_cache[pid]
            for pid in pictograph_ids
            if pid in self._pictograph_cache
        ]

    def load_csv_data(
        self, file_path: Path, category: str = "user_created"
    ) -> List[PictographData]:
        """Load pictograph data from a CSV file and add to dataset."""
        pictographs = []

        # Read CSV file
        try:
            df = pd.read_csv(file_path)

            for _, row in df.iterrows():
                # Convert each row to pictograph
                pictograph = self._convert_row_to_pictograph(row)
                if pictograph:
                    pictograph_id = self.add_to_dataset(pictograph, category)
                    pictographs.append(pictograph)

        except Exception as e:
            print(f"Error reading CSV file {file_path}: {e}")

        return pictographs

    def _load_csv_data(self) -> pd.DataFrame:
        """Load CSV data if not already loaded."""
        if self._csv_data is None:
            self._csv_data = pd.read_csv(self._data_path)
        return self._csv_data

    def get_specific_pictograph(
        self, letter: str, index: int = 0
    ) -> Optional[BeatData]:
        """Get a specific pictograph by letter and index from CSV data."""
        df = self._load_csv_data()

        # Filter by letter
        letter_data = df[df["letter"] == letter]

        if letter_data.empty or index >= len(letter_data):
            return None

        row = letter_data.iloc[index]
        return self._create_beat_data_from_csv_row(row)

    def get_pictographs_by_letter(self, letter: str) -> List[BeatData]:
        """Get all pictographs for a specific letter."""
        df = self._load_csv_data()
        letter_data = df[df["letter"] == letter]

        return [
            self._create_beat_data_from_csv_row(row)
            for _, row in letter_data.iterrows()
        ]

    def get_start_position_pictograph(
        self, position_key: str, grid_mode: str = "diamond"
    ) -> Optional[BeatData]:
        """Get start position pictograph by position key and grid mode."""
        # Map position keys to letters (from V1 start position mapping)
        position_to_letter = {
            "alpha1_alpha1": "A",
            "beta5_beta5": "B",
            "gamma11_gamma11": "C",
            "alpha2_alpha2": "A",
            "beta4_beta4": "B",
            "gamma12_gamma12": "C",
        }

        letter = position_to_letter.get(position_key)
        if not letter:
            print(f"⚠️ Unknown position key: {position_key}")
            return None

        # Get the first pictograph for this letter
        pictographs = self.get_pictographs_by_letter(letter)
        if pictographs:
            return pictographs[0]
        else:
            print(f"⚠️ No pictographs found for letter: {letter}")
            return None

    def _create_beat_data_from_csv_row(self, row) -> BeatData:
        """Convert a CSV row to BeatData object."""
        # Map CSV values to enums
        motion_type_map = {
            "pro": MotionType.PRO,
            "anti": MotionType.ANTI,
            "static": MotionType.STATIC,
            "dash": MotionType.DASH,
            "float": MotionType.FLOAT,
        }
        rotation_map = {
            "cw": RotationDirection.CLOCKWISE,
            "ccw": RotationDirection.COUNTER_CLOCKWISE,
            "no_rot": RotationDirection.NO_ROTATION,
        }
        location_map = {
            "n": Location.NORTH,
            "e": Location.EAST,
            "s": Location.SOUTH,
            "w": Location.WEST,
            "ne": Location.NORTHEAST,
            "se": Location.SOUTHEAST,
            "sw": Location.SOUTHWEST,
            "nw": Location.NORTHWEST,
        }

        # Create motion data if motion type exists
        blue_motion = None
        if row["blue_motion_type"] in motion_type_map:
            blue_motion = MotionData(
                motion_type=motion_type_map[row["blue_motion_type"]],
                prop_rot_dir=rotation_map.get(
                    row["blue_prop_rot_dir"], RotationDirection.CLOCKWISE
                ),
                start_loc=location_map[row["blue_start_loc"]],
                end_loc=location_map[row["blue_end_loc"]],
            )

        red_motion = None
        if row["red_motion_type"] in motion_type_map:
            red_motion = MotionData(
                motion_type=motion_type_map[row["red_motion_type"]],
                prop_rot_dir=rotation_map.get(
                    row["red_prop_rot_dir"], RotationDirection.CLOCKWISE
                ),
                start_loc=location_map[row["red_start_loc"]],
                end_loc=location_map[row["red_end_loc"]],
            )

        # Create initial beat data
        beat_data = BeatData(
            beat_number=1,
            letter=row["letter"],
            blue_motion=blue_motion,
            red_motion=red_motion,
        )

        # Generate glyph data
        glyph_data = self._generate_glyph_data(beat_data)

        # Return beat data with glyph data
        return beat_data.update(glyph_data=glyph_data)

    # Private helper methods

    def _generate_glyph_data(self, beat_data: BeatData) -> Optional[GlyphData]:
        """Generate glyph data for beat data."""
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
            show_elemental=letter_type == LetterType.TYPE1 if letter_type else False,
            show_vtg=letter_type == LetterType.TYPE1 if letter_type else False,
            show_tka=True,
            show_positions=letter_type != LetterType.TYPE6 if letter_type else True,
        )

    def _matches_query(self, pictograph: PictographData, query: Dict[str, Any]) -> bool:
        """Check if pictograph matches search query."""
        # Letter matching
        if "letter" in query:
            letter = pictograph.metadata.get("letter", "").lower()
            query_letter = query["letter"].lower()
            if query_letter not in letter:
                return False

        # Motion type matching
        if "motion_type" in query:
            query_motion_type = query["motion_type"]
            has_matching_motion = False

            for arrow in pictograph.arrows.values():
                if (
                    arrow.motion_data
                    and arrow.motion_data.motion_type == query_motion_type
                ):
                    has_matching_motion = True
                    break

            if not has_matching_motion:
                return False

        return True

    def _convert_v1_motion(
        self, v1_motion_data: Dict[str, Any]
    ) -> Optional[MotionData]:
        """Convert V1 motion data to V2 MotionData."""
        try:
            from domain.models.core_models import (
                MotionType,
                RotationDirection,
                Location,
            )

            # Map V1 motion types to V2 (direct mapping - same values)
            v1_type = v1_motion_data.get("motion_type", "").lower()
            motion_type_map = {
                "pro": MotionType.PRO,
                "anti": MotionType.ANTI,
                "static": MotionType.STATIC,
                "dash": MotionType.DASH,
                "float": MotionType.FLOAT,
            }

            motion_type = motion_type_map.get(v1_type, MotionType.PRO)

            # Map rotation directions
            v1_rotation = v1_motion_data.get("rotation", "").lower()
            rotation_map = {
                "cw": RotationDirection.CLOCKWISE,
                "ccw": RotationDirection.COUNTER_CLOCKWISE,
                "no_rot": RotationDirection.NO_ROTATION,
            }

            rotation = rotation_map.get(v1_rotation, RotationDirection.CLOCKWISE)

            # Map locations (simplified)
            start_loc = Location.NORTH  # Default
            end_loc = Location.SOUTH  # Default

            return MotionData(
                motion_type=motion_type,
                prop_rot_dir=rotation,
                start_loc=start_loc,
                end_loc=end_loc,
                turns=v1_motion_data.get("turns", 1.0),
            )

        except Exception:
            return None

    def _generate_glyph_key(self, pictograph: PictographData) -> str:
        """Generate glyph key for pictograph."""
        # Simplified glyph key generation
        key_parts = []

        for color in ["blue", "red"]:
            if color in pictograph.arrows:
                arrow = pictograph.arrows[color]
                if arrow.motion_data:
                    key_parts.append(f"{color}_{arrow.motion_data.motion_type.value}")

        return "_".join(key_parts) if key_parts else "blank"

    def _determine_letter_type(self, letter: str) -> Optional[LetterType]:
        """Determine the letter type from the letter string."""
        # Letter type mapping from old glyph service
        letter_type_map = {
            # Type 1 letters (show elemental and VTG)
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
            "W": LetterType.TYPE1,
            "X": LetterType.TYPE1,
            "Y": LetterType.TYPE1,
            "Z": LetterType.TYPE1,
            # Type 6 letters (don't show positions)
            "α": LetterType.TYPE6,
            "β": LetterType.TYPE6,
            "Γ": LetterType.TYPE6,
        }
        return letter_type_map.get(letter)

    def _determine_vtg_mode(self, beat_data: BeatData) -> Optional[VTGMode]:
        """Determine VTG mode from beat data."""
        blue_motion = beat_data.blue_motion
        red_motion = beat_data.red_motion

        if not blue_motion or not red_motion:
            return None

        # Simplified VTG determination
        same_direction = self._motions_same_direction(blue_motion, red_motion)
        motion_pattern = self._determine_motion_pattern(blue_motion, red_motion)

        if motion_pattern == "split":
            return VTGMode.SPLIT_SAME if same_direction else VTGMode.SPLIT_OPP
        elif motion_pattern == "together":
            return VTGMode.TOG_SAME if same_direction else VTGMode.TOG_OPP
        elif motion_pattern == "quarter":
            return VTGMode.QUARTER_SAME if same_direction else VTGMode.QUARTER_OPP

        return VTGMode.SPLIT_SAME  # Default

    def _motions_same_direction(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> bool:
        """Check if motions are in same direction."""
        return blue_motion.prop_rot_dir == red_motion.prop_rot_dir

    def _determine_motion_pattern(
        self, blue_motion: MotionData, red_motion: MotionData
    ) -> str:
        """Determine motion pattern (split, together, quarter)."""
        # Simplified pattern determination
        blue_start = blue_motion.start_loc
        red_start = red_motion.start_loc

        # Check if starting positions are opposite
        opposite_pairs = [
            (Location.NORTH, Location.SOUTH),
            (Location.EAST, Location.WEST),
            (Location.NORTHEAST, Location.SOUTHWEST),
            (Location.NORTHWEST, Location.SOUTHEAST),
        ]

        for pair in opposite_pairs:
            if (blue_start, red_start) in [pair, pair[::-1]]:
                return "split"

        # Check if starting positions are adjacent
        if blue_start == red_start:
            return "together"

        return "quarter"  # Default

    def _determine_positions(
        self, beat_data: BeatData
    ) -> Tuple[Optional[str], Optional[str]]:
        """Determine start and end positions from beat data."""
        # Extract from metadata if available
        start_pos = beat_data.metadata.get("start_pos")
        end_pos = beat_data.metadata.get("end_pos")

        if start_pos and end_pos:
            return start_pos, end_pos

        # Generate from motion data if available
        if beat_data.blue_motion and beat_data.red_motion:
            start_pos = f"{beat_data.blue_motion.start_loc.value}_{beat_data.red_motion.start_loc.value}"
            end_pos = f"{beat_data.blue_motion.end_loc.value}_{beat_data.red_motion.end_loc.value}"
            return start_pos, end_pos

        return None, None

    def _vtg_to_elemental(self, vtg_mode: Optional[VTGMode]) -> Optional[ElementalType]:
        """Convert VTG mode to elemental type."""
        if not vtg_mode:
            return None

        vtg_to_elemental_map = {
            VTGMode.SPLIT_SAME: ElementalType.FIRE,
            VTGMode.SPLIT_OPP: ElementalType.WATER,
            VTGMode.TOG_SAME: ElementalType.AIR,
            VTGMode.TOG_OPP: ElementalType.EARTH,
            VTGMode.QUARTER_SAME: ElementalType.FIRE,
            VTGMode.QUARTER_OPP: ElementalType.WATER,
        }

        return vtg_to_elemental_map.get(vtg_mode)

    def _load_context_configs(self) -> Dict[PictographContext, Dict[str, Any]]:
        """Load context-specific configurations."""
        return {
            PictographContext.SEQUENCE_EDITOR: {
                "show_grid": True,
                "show_arrows": True,
                "interactive": True,
            },
            PictographContext.STANDALONE_VIEWER: {
                "show_grid": False,
                "show_arrows": True,
                "interactive": False,
            },
            PictographContext.DICTIONARY_BROWSER: {
                "show_grid": False,
                "show_arrows": True,
                "interactive": False,
                "compact_view": True,
            },
        }

    def _load_glyph_mappings(self) -> Dict[str, str]:
        """Load glyph mappings for pictographs."""
        return {
            "blue_pro_red_anti": "⚡",
            "blue_static_red_static": "⬜",
            "blue_dash_red_dash": "⚊",
            "blank": "○",
        }

    def _load_v1_conversion_rules(self) -> Dict[str, Any]:
        """Load V1 to V2 conversion rules."""
        return {
            "motion_type_mappings": {
                "pro": "pro",
                "anti": "anti",
                "static": "static",
                "dash": "dash",
                "float": "float",
            },
            "location_mappings": {
                "n": "north",
                "ne": "northeast",
                "e": "east",
                "se": "southeast",
                "s": "south",
                "sw": "southwest",
                "w": "west",
                "nw": "northwest",
            },
        }

    def _convert_row_to_pictograph(self, row: pd.Series) -> Optional[PictographData]:
        """Convert a CSV row to PictographData."""
        try:
            # Extract arrow data
            arrows = {}

            if "blue_arrow" in row and pd.notna(row["blue_arrow"]):
                blue_motion = self._convert_v1_motion(eval(row["blue_arrow"]))
                if blue_motion:
                    arrows["blue"] = ArrowData(
                        color="blue",
                        motion_data=blue_motion,
                        is_visible=True,
                    )

            if "red_arrow" in row and pd.notna(row["red_arrow"]):
                red_motion = self._convert_v1_motion(eval(row["red_arrow"]))
                if red_motion:
                    arrows["red"] = ArrowData(
                        color="red",
                        motion_data=red_motion,
                        is_visible=True,
                    )

            # Create pictograph
            pictograph = self.create_pictograph()
            return pictograph.update(
                arrows=arrows,
                is_blank=len(arrows) == 0,
                metadata={
                    "letter": row.get("letter"),
                    "beat_number": row.get("beat_number"),
                    "context": row.get("context"),
                },
            )

        except Exception as e:
            print(f"Error converting row to pictograph: {e}")
            return None
