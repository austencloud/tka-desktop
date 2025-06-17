"""
Pictograph Data Service - Focused Pictograph CRUD Operations

Handles all core pictograph data operations including:
- Pictograph creation and manipulation
- Dataset management and querying
- Pictograph caching and indexing
- Category-based organization

This service provides a clean, focused interface for pictograph data operations
while maintaining the proven data management algorithms.
"""

from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import uuid

from domain.models.core_models import BeatData
from domain.models.pictograph_models import PictographData, GridData, GridMode, ArrowData


class IPictographDataService(ABC):
    """Interface for pictograph data operations."""

    @abstractmethod
    def create_pictograph(self, grid_mode: GridMode = GridMode.DIAMOND) -> PictographData:
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
    def add_to_dataset(self, pictograph: PictographData, category: str = "user_created") -> str:
        """Add pictograph to dataset."""
        pass


class PictographDataService(IPictographDataService):
    """
    Focused pictograph data service.

    Provides comprehensive pictograph data management including:
    - Pictograph creation and manipulation
    - Dataset management and querying
    - Pictograph caching and indexing
    - Category-based organization
    """

    def __init__(self):
        # Dataset management
        self._pictograph_cache: Dict[str, PictographData] = {}
        self._dataset_index: Dict[str, List[str]] = {}

    def create_pictograph(self, grid_mode: GridMode = GridMode.DIAMOND) -> PictographData:
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
            metadata={"created_by": "pictograph_data_service"},
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
        max_results = query.get("max_results", 50)

        # Search through cached pictographs
        for pictograph_id, pictograph in self._pictograph_cache.items():
            if self._matches_query(pictograph, query):
                results.append(pictograph)

                if len(results) >= max_results:
                    break

        return results

    def add_to_dataset(self, pictograph: PictographData, category: str = "user_created") -> str:
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

    def get_pictograph_by_id(self, pictograph_id: str) -> Optional[PictographData]:
        """Get pictograph by ID."""
        return self._pictograph_cache.get(pictograph_id)

    def remove_from_dataset(self, pictograph_id: str) -> bool:
        """Remove pictograph from dataset."""
        if pictograph_id not in self._pictograph_cache:
            return False

        # Remove from cache
        del self._pictograph_cache[pictograph_id]

        # Remove from all categories
        for category, ids in self._dataset_index.items():
            if pictograph_id in ids:
                ids.remove(pictograph_id)

        return True

    def get_dataset_stats(self) -> Dict[str, Any]:
        """Get dataset statistics."""
        return {
            "total_pictographs": len(self._pictograph_cache),
            "categories": {
                category: len(ids) for category, ids in self._dataset_index.items()
            },
            "cache_size": len(self._pictograph_cache),
        }

    def clear_cache(self) -> None:
        """Clear the pictograph cache."""
        self._pictograph_cache.clear()
        self._dataset_index.clear()

    # Private helper methods

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
                if arrow.motion_data and arrow.motion_data.motion_type == query_motion_type:
                    has_matching_motion = True
                    break

            if not has_matching_motion:
                return False

        # Start position matching
        if "start_position" in query:
            query_start_position = query["start_position"]
            has_matching_start = False

            for arrow in pictograph.arrows.values():
                if arrow.motion_data and arrow.motion_data.start_loc == query_start_position:
                    has_matching_start = True
                    break

            if not has_matching_start:
                return False

        return True
