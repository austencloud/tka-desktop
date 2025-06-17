"""
Motion Generation Service - Focused Motion Generation Operations

Handles all motion generation logic including:
- Valid motion combination generation from datasets
- Letter-specific motion generation
- End location calculation
- Motion dataset management

This service provides a clean, focused interface for motion generation
while maintaining the proven generation algorithms.
"""

from typing import List, Dict, Any, Tuple, Optional, Union, TYPE_CHECKING
from abc import ABC, abstractmethod
import logging
import uuid
from datetime import datetime

from domain.models.core_models import (
    MotionData,
    MotionType,
    Location,
    RotationDirection,
)

# Event-driven architecture imports
if TYPE_CHECKING:
    from core.events import IEventBus

try:
    from core.events import (
        IEventBus,
        get_event_bus,
        EventPriority,
        BeatUpdatedEvent,
        MotionGeneratedEvent,
        MotionValidatedEvent,
    )

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    # For tests or when event system is not available
    IEventBus = None
    get_event_bus = None
    EventPriority = None
    EVENT_SYSTEM_AVAILABLE = False

try:
    from src.core.decorators import handle_service_errors
    from src.core.monitoring import monitor_performance
    from src.core.exceptions import ServiceOperationError, ValidationError
except ImportError:
    # For tests, create dummy decorators if imports fail
    def handle_service_errors(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    def monitor_performance(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    class ServiceOperationError(Exception):
        pass

    class ValidationError(Exception):
        pass


logger = logging.getLogger(__name__)


class IMotionGenerationService(ABC):
    """Interface for motion generation operations."""

    @abstractmethod
    def get_valid_motion_combinations(
        self, motion_type: MotionType, location: Location
    ) -> List[MotionData]:
        """Get all valid motion combinations for a given type and location."""
        pass

    @abstractmethod
    def generate_motion_combinations_for_letter(
        self, letter: str
    ) -> List[Tuple[MotionData, MotionData]]:
        """Generate valid motion combinations for a specific letter."""
        pass

    @abstractmethod
    def calculate_end_location(
        self, start_loc: Location, motion_type: MotionType, turns: float
    ) -> Location:
        """Calculate end location based on motion type and turns."""
        pass


class MotionGenerationService(IMotionGenerationService):
    """
    Focused motion generation service.

    Provides comprehensive motion generation including:
    - Valid motion combination generation from datasets
    - Letter-specific motion generation
    - End location calculation
    - Motion dataset management
    """

    def __init__(
        self,
        validation_service=None,
        event_bus: Optional[Any] = None,
    ):
        # Motion generation datasets
        self._motion_datasets = self._load_motion_datasets()
        self._letter_specific_rules = self._load_letter_specific_rules()

        # Optional validation service for filtering
        self._validation_service = validation_service

        # NEW: Event system integration
        self.event_bus = event_bus or (get_event_bus() if get_event_bus else None)
        self._subscription_ids: List[str] = []

        # Subscribe to relevant events
        if self.event_bus:
            self._setup_event_subscriptions()

    @handle_service_errors("get_valid_motion_combinations")
    @monitor_performance("motion_combination_generation")
    def get_valid_motion_combinations(
        self, motion_type: MotionType, location: Location
    ) -> List[MotionData]:
        """Get all valid motion combinations for a given type and location."""
        combinations = []

        # Get base motions from dataset
        base_motions = self._motion_datasets.get(motion_type, [])

        for base_motion in base_motions:
            # Create variations with different locations and rotations
            for rot_dir in RotationDirection:
                for turns in [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
                    motion = MotionData(
                        motion_type=motion_type,
                        prop_rot_dir=rot_dir,
                        start_loc=location,
                        end_loc=self.calculate_end_location(
                            location, motion_type, turns
                        ),
                        turns=turns,
                    )

                    if self._is_valid_single_motion(motion):
                        combinations.append(motion)

        return combinations

    @handle_service_errors("generate_motion_combinations_for_letter")
    @monitor_performance("letter_motion_generation")
    def generate_motion_combinations_for_letter(
        self, letter: str
    ) -> List[Tuple[MotionData, MotionData]]:
        """Generate valid motion combinations for a specific letter."""
        combinations = []

        # Get letter-specific rules
        letter_rules = self._letter_specific_rules.get(letter.lower(), {})

        # Get allowed motion types for this letter
        allowed_blue_types = letter_rules.get("blue_motion_types", list(MotionType))
        allowed_red_types = letter_rules.get("red_motion_types", list(MotionType))

        # Generate combinations
        for blue_type in allowed_blue_types:
            for red_type in allowed_red_types:
                blue_motions = self.get_valid_motion_combinations(
                    blue_type, Location.NORTH
                )
                red_motions = self.get_valid_motion_combinations(
                    red_type, Location.NORTH
                )

                for blue_motion in blue_motions:
                    for red_motion in red_motions:
                        # Use validation service if available
                        if self._validation_service:
                            if self._validation_service.validate_motion_combination(
                                blue_motion, red_motion
                            ):
                                combinations.append((blue_motion, red_motion))
                        else:
                            # Basic validation without external service
                            combinations.append((blue_motion, red_motion))

        return combinations[:50]  # Limit to prevent excessive combinations

    @handle_service_errors("calculate_end_location")
    def calculate_end_location(
        self, start_loc: Location, motion_type: MotionType, turns: float
    ) -> Location:
        """Calculate end location based on motion type and turns."""
        if motion_type == MotionType.STATIC:
            return start_loc

        # For other motion types, calculate based on turns
        # This is a simplified calculation - real implementation would be more complex
        location_order = [
            Location.NORTH,
            Location.NORTHEAST,
            Location.EAST,
            Location.SOUTHEAST,
            Location.SOUTH,
            Location.SOUTHWEST,
            Location.WEST,
            Location.NORTHWEST,
        ]

        try:
            start_index = location_order.index(start_loc)
            offset = int(turns * 2) % len(location_order)  # 2 positions per turn
            end_index = (start_index + offset) % len(location_order)
            return location_order[end_index]
        except ValueError:
            return start_loc

    # NEW: Event-driven methods

    def _setup_event_subscriptions(self):
        """Subscribe to events that require motion generation."""
        if not self.event_bus or not EventPriority:
            return

        # Subscribe to beat update events that might need motion generation
        sub_id = self.event_bus.subscribe(
            "sequence.beat_updated",
            self._on_beat_updated,
            priority=EventPriority.NORMAL,
        )
        self._subscription_ids.append(sub_id)

    def _on_beat_updated(self, event: BeatUpdatedEvent):
        """Handle beat updated event by generating motion if needed."""
        if not self.event_bus:
            return

        logger.info(
            f"Motion service responding to beat update: beat {event.beat_number}, field {event.field_changed}"
        )

        try:
            # Check if the update requires motion generation
            if self._should_generate_motion_for_update(event):
                self._generate_motion_for_beat_update(event)

        except Exception as e:
            logger.error(f"Failed to generate motion for beat update: {e}")

    def _should_generate_motion_for_update(self, event: BeatUpdatedEvent) -> bool:
        """Determine if motion generation is needed for this beat update."""
        # Generate motion when letter changes (might need new motion combinations)
        if event.field_changed == "letter":
            return True

        # Generate motion when motion fields are cleared/reset
        if (
            event.field_changed in ["blue_motion", "red_motion"]
            and event.new_value is None
        ):
            return True

        return False

    def _generate_motion_for_beat_update(self, event: BeatUpdatedEvent):
        """Generate appropriate motion for the updated beat."""
        if not self.event_bus:
            return

        # If letter was updated, generate new motion combinations
        if event.field_changed == "letter" and event.new_value:
            letter = str(event.new_value)
            combinations = self.generate_motion_combinations_for_letter(letter)

            if combinations:
                # Take the first valid combination
                blue_motion, red_motion = combinations[0]

                # Publish motion generated events
                self.event_bus.publish(
                    MotionGeneratedEvent(
                        event_id=str(uuid.uuid4()),
                        timestamp=datetime.now(),
                        source="MotionGenerationService",
                        sequence_id=event.sequence_id,
                        beat_number=event.beat_number,
                        color="blue",
                        motion_data=blue_motion.to_dict(),
                        generation_method="letter_based_auto",
                    )
                )

                self.event_bus.publish(
                    MotionGeneratedEvent(
                        event_id=str(uuid.uuid4()),
                        timestamp=datetime.now(),
                        source="MotionGenerationService",
                        sequence_id=event.sequence_id,
                        beat_number=event.beat_number,
                        color="red",
                        motion_data=red_motion.to_dict(),
                        generation_method="letter_based_auto",
                    )
                )

                logger.info(
                    f"Generated motion for letter '{letter}' in beat {event.beat_number}"
                )

    def generate_motion_with_events(
        self,
        sequence_id: str,
        beat_number: int,
        letter: str,
        generation_method: str = "manual",
    ) -> Tuple[MotionData, MotionData]:
        """Generate motion and publish events."""
        combinations = self.generate_motion_combinations_for_letter(letter)

        if not combinations:
            raise ValueError(
                f"No valid motion combinations found for letter '{letter}'"
            )

        blue_motion, red_motion = combinations[0]

        # Publish events if event bus is available
        if self.event_bus:
            self.event_bus.publish(
                MotionGeneratedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="MotionGenerationService",
                    sequence_id=sequence_id,
                    beat_number=beat_number,
                    color="blue",
                    motion_data=blue_motion.to_dict(),
                    generation_method=generation_method,
                )
            )

            self.event_bus.publish(
                MotionGeneratedEvent(
                    event_id=str(uuid.uuid4()),
                    timestamp=datetime.now(),
                    source="MotionGenerationService",
                    sequence_id=sequence_id,
                    beat_number=beat_number,
                    color="red",
                    motion_data=red_motion.to_dict(),
                    generation_method=generation_method,
                )
            )

        return blue_motion, red_motion

    def cleanup(self):
        """Clean up event subscriptions when service is destroyed."""
        if self.event_bus:
            for sub_id in self._subscription_ids:
                self.event_bus.unsubscribe(sub_id)
            self._subscription_ids.clear()

    # Private validation methods

    def _is_valid_single_motion(self, motion: MotionData) -> bool:
        """Check if a single motion is valid."""
        # Basic motion validation
        if motion.turns < 0 or motion.turns > 3:
            return False

        # Motion type specific validation
        if motion.motion_type == MotionType.STATIC and motion.turns != 0:
            return False

        return True

    # Private data loading methods

    def _load_motion_datasets(self) -> Dict[MotionType, List[Dict[str, Any]]]:
        """Load motion datasets for generation."""
        # In production, this would load from JSON/database
        return {
            MotionType.PRO: [
                {
                    "base_turns": 1.0,
                    "common_locations": [
                        Location.NORTH,
                        Location.EAST,
                        Location.SOUTH,
                        Location.WEST,
                    ],
                },
                {
                    "base_turns": 2.0,
                    "common_locations": [
                        Location.NORTHEAST,
                        Location.SOUTHEAST,
                        Location.SOUTHWEST,
                        Location.NORTHWEST,
                    ],
                },
            ],
            MotionType.ANTI: [
                {
                    "base_turns": 1.0,
                    "common_locations": [
                        Location.NORTH,
                        Location.EAST,
                        Location.SOUTH,
                        Location.WEST,
                    ],
                },
                {
                    "base_turns": 2.0,
                    "common_locations": [
                        Location.NORTHEAST,
                        Location.SOUTHEAST,
                        Location.SOUTHWEST,
                        Location.NORTHWEST,
                    ],
                },
            ],
            MotionType.STATIC: [
                {"base_turns": 0.0, "common_locations": list(Location)},
            ],
            MotionType.DASH: [
                {
                    "base_turns": 0.0,
                    "common_locations": [
                        Location.NORTH,
                        Location.EAST,
                        Location.SOUTH,
                        Location.WEST,
                    ],
                },
                {
                    "base_turns": 1.0,
                    "common_locations": [
                        Location.NORTHEAST,
                        Location.SOUTHEAST,
                        Location.SOUTHWEST,
                        Location.NORTHWEST,
                    ],
                },
            ],
            MotionType.FLOAT: [
                {"base_turns": 1.0, "common_locations": list(Location)},
            ],
        }

    def _load_letter_specific_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load letter-specific motion rules."""
        # In production, this would load from JSON/database
        return {
            "a": {
                "blue_motion_types": [MotionType.PRO, MotionType.ANTI],
                "red_motion_types": [MotionType.PRO, MotionType.ANTI],
            },
            "b": {
                "blue_motion_types": [MotionType.STATIC, MotionType.DASH],
                "red_motion_types": [MotionType.STATIC, MotionType.DASH],
            },
            # Add more letter rules as needed
        }
