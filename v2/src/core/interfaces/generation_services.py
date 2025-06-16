"""
Interface definitions for Modern Generate Tab services.

These interfaces define the contracts for generation-related services,
following Modern's dependency injection and clean architecture patterns.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List, Set, Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from domain.models.generation_models import GenerationConfig, GenerationResult


class GenerationMode(Enum):
    FREEFORM = "freeform"
    CIRCULAR = "circular"


class PropContinuity(Enum):
    CONTINUOUS = "continuous"
    RANDOM = "random"


class LetterType(Enum):
    TYPE1 = "Type1"  # Dual-Shift: A-V
    TYPE2 = "Type2"  # Shift: W,X,Y,Z,Σ,Δ,θ,Ω
    TYPE3 = "Type3"  # Cross-Shift: W-,X-,Y-,Z-,Σ-,Δ-,θ-,Ω-
    TYPE4 = "Type4"  # Dash: Φ,Ψ,Λ
    TYPE5 = "Type5"  # Dual-Dash: Φ-,Ψ-,Λ-
    TYPE6 = "Type6"  # Static: α,β,Γ


class SliceSize(Enum):
    QUARTERED = "quartered"
    HALVED = "halved"


class CAPType(Enum):
    STRICT_ROTATED = "strict_rotated"
    STRICT_MIRRORED = "strict_mirrored"
    STRICT_SWAPPED = "strict_swapped"
    STRICT_COMPLEMENTARY = "strict_complementary"
    SWAPPED_COMPLEMENTARY = "swapped_complementary"
    ROTATED_COMPLEMENTARY = "rotated_complementary"
    MIRRORED_SWAPPED = "mirrored_swapped"
    MIRRORED_COMPLEMENTARY = "mirrored_complementary"
    ROTATED_SWAPPED = "rotated_swapped"
    MIRRORED_ROTATED = "mirrored_rotated"
    MIRRORED_COMPLEMENTARY_ROTATED = "mirrored_complementary_rotated"


@dataclass(frozen=True)
class GenerationMetadata:
    generation_time_ms: int
    algorithm_used: str
    parameters_hash: str
    warnings: Optional[List[str]] = None


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    suggestions: Optional[List[str]] = None


class IGenerationService(ABC):

    @abstractmethod
    def generate_freeform_sequence(self, config: GenerationConfig) -> GenerationResult:
        pass

    @abstractmethod
    def generate_circular_sequence(self, config: GenerationConfig) -> GenerationResult:
        pass

    @abstractmethod
    def auto_complete_sequence(self, current_sequence: Any) -> GenerationResult:
        pass

    @abstractmethod
    def validate_generation_parameters(
        self, config: GenerationConfig
    ) -> ValidationResult:
        pass


class ISequenceConfigurationService(ABC):

    @abstractmethod
    def get_current_config(self) -> GenerationConfig:
        pass

    @abstractmethod
    def update_config(self, updates: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def save_config_as_preset(self, name: str) -> None:
        pass

    @abstractmethod
    def load_config_preset(self, name: str) -> GenerationConfig:
        pass

    @abstractmethod
    def get_default_config(self) -> GenerationConfig:
        pass

    @abstractmethod
    def get_preset_names(self) -> List[str]:
        pass


class IGenerationValidationService(ABC):

    @abstractmethod
    def validate_length(self, length: int, mode: GenerationMode) -> ValidationResult:
        pass

    @abstractmethod
    def validate_level(self, level: int, length: int) -> ValidationResult:
        pass

    @abstractmethod
    def validate_turn_intensity(self, intensity: float, level: int) -> ValidationResult:
        pass

    @abstractmethod
    def validate_letter_combination(
        self, letters: Set[LetterType], mode: GenerationMode
    ) -> ValidationResult:
        pass

    @abstractmethod
    def validate_complete_config(self, config: GenerationConfig) -> ValidationResult:
        pass


class IGenerationHistoryService(ABC):

    @abstractmethod
    def record_generation(
        self, config: GenerationConfig, result: GenerationResult
    ) -> None:
        pass

    @abstractmethod
    def get_recent_configs(self, limit: int = 10) -> List[GenerationConfig]:
        pass

    @abstractmethod
    def get_generation_stats(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def clear_history(self) -> None:
        pass
