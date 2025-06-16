"""
Domain models for Modern Generate Tab.

These immutable data classes represent the core business entities
for sequence generation, following Modern's clean architecture principles.
"""

from typing import Optional, Set, List
from dataclasses import dataclass, replace

from ...core.interfaces.generation_services import (
    GenerationMode,
    PropContinuity,
    LetterType,
    SliceSize,
    CAPType,
    GenerationMetadata,
    ValidationResult,
)


@dataclass(frozen=True)
class GenerationConfig:
    """Immutable configuration for sequence generation"""

    mode: GenerationMode = GenerationMode.FREEFORM
    length: int = 16
    level: int = 1
    turn_intensity: float = 1.0
    prop_continuity: PropContinuity = PropContinuity.CONTINUOUS
    letter_types: Optional[Set[LetterType]] = None
    slice_size: SliceSize = SliceSize.HALVED
    cap_type: Optional[CAPType] = CAPType.STRICT_ROTATED
    start_position_key: Optional[str] = None

    def __post_init__(self):
        if self.letter_types is None:
            object.__setattr__(
                self,
                "letter_types",
                {
                    LetterType.TYPE1,
                    LetterType.TYPE2,
                    LetterType.TYPE3,
                    LetterType.TYPE4,
                    LetterType.TYPE5,
                    LetterType.TYPE6,
                },
            )

    def with_updates(self, **kwargs) -> "GenerationConfig":
        """Create a new config with updated values"""
        return replace(self, **kwargs)

    def is_valid(self) -> bool:
        """Check if configuration is valid"""
        return (
            4 <= self.length <= 32
            and 1 <= self.level <= 6
            and 0.5 <= self.turn_intensity <= 3.0
            and self.letter_types is not None
            and len(self.letter_types) > 0
        )


@dataclass(frozen=True)
class GenerationResult:
    """Result of a sequence generation operation"""

    success: bool
    sequence_data: Optional[List[dict]] = None
    start_position_data: Optional[dict] = None
    metadata: Optional[GenerationMetadata] = None
    error_message: Optional[str] = None
    warnings: Optional[List[str]] = None

    def __post_init__(self):
        if self.warnings is None:
            object.__setattr__(self, "warnings", [])


@dataclass(frozen=True)
class GenerationState:
    """Current state of the generation UI"""

    config: GenerationConfig
    is_generating: bool = False
    last_result: Optional[GenerationResult] = None
    validation_errors: Optional[List[str]] = None

    def __post_init__(self):
        if self.validation_errors is None:
            object.__setattr__(self, "validation_errors", [])

    def with_config(self, config: GenerationConfig) -> "GenerationState":
        """Create new state with updated config"""
        return replace(self, config=config)

    def with_result(self, result: GenerationResult) -> "GenerationState":
        """Create new state with generation result"""
        return replace(self, last_result=result, is_generating=False)

    def start_generation(self) -> "GenerationState":
        """Create new state marking generation as started"""
        return replace(self, is_generating=True)
