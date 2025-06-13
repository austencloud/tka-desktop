"""
Service implementations for V2 Generate Tab.

These services adapt V1's generation logic to V2's clean architecture,
providing dependency injection and immutable data flow.
"""

import logging
import random
import time
from typing import Optional, Dict, Any, List, Set

from ...domain.models.generation_models import (
    GenerationConfig,
    GenerationResult,
    GenerationMetadata,
    ValidationResult,
)
from ...core.interfaces.generation_services import (
    IGenerationService,
    ISequenceConfigurationService,
    IGenerationValidationService,
    IGenerationHistoryService,
    GenerationMode,
    PropContinuity,
    LetterType,
)


class GenerationService(IGenerationService):

    def __init__(
        self,
        validation_service: IGenerationValidationService,
        history_service: IGenerationHistoryService,
    ):
        self._validation_service = validation_service
        self._history_service = history_service
        self._logger = logging.getLogger(__name__)

        self._letter_type_mappings = {
            LetterType.TYPE1: [
                "A",
                "B",
                "C",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
                "M",
                "N",
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
            ],
            LetterType.TYPE2: ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"],
            LetterType.TYPE3: ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
            LetterType.TYPE4: ["Φ", "Ψ", "Λ"],
            LetterType.TYPE5: ["Φ-", "Ψ-", "Λ-"],
            LetterType.TYPE6: ["α", "β", "Γ"],
        }

    def generate_freeform_sequence(self, config: GenerationConfig) -> GenerationResult:
        start_time = time.time()

        validation = self._validation_service.validate_complete_config(config)
        if not validation.is_valid:
            error_msg = f"Invalid configuration: {', '.join(validation.errors or [])}"
            return GenerationResult(success=False, error_message=error_msg)

        try:
            sequence_data, start_pos_data = self._generate_freeform_internal(config)

            generation_time = int((time.time() - start_time) * 1000)
            metadata = GenerationMetadata(
                generation_time_ms=generation_time,
                algorithm_used="freeform_v1_adapted",
                parameters_hash=str(hash(str(config))),
                warnings=validation.warnings,
            )

            result = GenerationResult(
                success=True,
                sequence_data=sequence_data,
                start_position_data=start_pos_data,
                metadata=metadata,
                warnings=validation.warnings,
            )

            self._history_service.record_generation(config, result)
            return result

        except Exception as e:
            self._logger.error(f"Freeform generation failed: {e}")
            return GenerationResult(success=False, error_message=str(e))

    def generate_circular_sequence(self, config: GenerationConfig) -> GenerationResult:
        start_time = time.time()

        validation = self._validation_service.validate_complete_config(config)
        if not validation.is_valid:
            error_msg = f"Invalid configuration: {', '.join(validation.errors or [])}"
            return GenerationResult(success=False, error_message=error_msg)

        try:
            sequence_data, start_pos_data = self._generate_circular_internal(config)

            generation_time = int((time.time() - start_time) * 1000)
            metadata = GenerationMetadata(
                generation_time_ms=generation_time,
                algorithm_used="circular_v1_adapted",
                parameters_hash=str(hash(str(config))),
                warnings=validation.warnings,
            )

            result = GenerationResult(
                success=True,
                sequence_data=sequence_data,
                start_position_data=start_pos_data,
                metadata=metadata,
                warnings=validation.warnings,
            )

            self._history_service.record_generation(config, result)
            return result

        except Exception as e:
            self._logger.error(f"Circular generation failed: {e}")
            return GenerationResult(success=False, error_message=str(e))

    def auto_complete_sequence(self, current_sequence: Any) -> GenerationResult:
        config = GenerationConfig(
            mode=GenerationMode.FREEFORM, length=8, level=2, turn_intensity=1.0
        )

        return self.generate_freeform_sequence(config)

    def validate_generation_parameters(
        self, config: GenerationConfig
    ) -> ValidationResult:
        return self._validation_service.validate_complete_config(config)

    def _generate_freeform_internal(
        self, config: GenerationConfig
    ) -> tuple[List[dict], dict]:
        sequence_data = []
        start_pos_data = self._generate_start_position(config)

        available_letters = []
        if config.letter_types:
            for letter_type in config.letter_types:
                available_letters.extend(
                    self._letter_type_mappings.get(letter_type, [])
                )

        for i in range(config.length):
            beat_data = self._generate_beat(config, i, sequence_data, available_letters)
            sequence_data.append(beat_data)

        return sequence_data, start_pos_data

    def _generate_circular_internal(
        self, config: GenerationConfig
    ) -> tuple[List[dict], dict]:
        sequence_data = []
        start_pos_data = self._generate_start_position(config)

        available_letters = []
        if config.letter_types:
            for letter_type in config.letter_types:
                available_letters.extend(
                    self._letter_type_mappings.get(letter_type, [])
                )

        for i in range(config.length):
            beat_data = self._generate_circular_beat(
                config, i, sequence_data, available_letters
            )
            sequence_data.append(beat_data)

        return sequence_data, start_pos_data

    def _generate_start_position(self, config: GenerationConfig) -> dict:
        available_letters = []
        if config.letter_types:
            for letter_type in config.letter_types:
                available_letters.extend(
                    self._letter_type_mappings.get(letter_type, [])
                )

        if not available_letters:
            available_letters = ["A", "B", "C", "D"]

        return {
            "letter": random.choice(available_letters),
            "start_ori": random.choice(["in", "out"]),
            "end_ori": random.choice(["in", "out"]),
            "sequence_start_position": True,
        }

    def _generate_beat(
        self,
        config: GenerationConfig,
        beat_index: int,
        existing_beats: List[dict],
        available_letters: List[str],
    ) -> dict:
        if not available_letters:
            available_letters = ["A", "B", "C", "D"]

        return {
            "beat": beat_index + 1,
            "letter": random.choice(available_letters),
            "start_ori": random.choice(["in", "out"]),
            "end_ori": random.choice(["in", "out"]),
            "motion_type": random.choice(["pro", "anti"]),
            "turns": config.turn_intensity,
            "duration": 1,
        }

    def _generate_circular_beat(
        self,
        config: GenerationConfig,
        beat_index: int,
        existing_beats: List[dict],
        available_letters: List[str],
    ) -> dict:
        if not available_letters:
            available_letters = ["A", "B", "C", "D"]

        return {
            "beat": beat_index + 1,
            "letter": random.choice(available_letters),
            "start_ori": random.choice(["in", "out"]),
            "end_ori": random.choice(["in", "out"]),
            "motion_type": random.choice(["pro", "anti"]),
            "turns": config.turn_intensity,
            "duration": 1,
        }


class SequenceConfigurationService(ISequenceConfigurationService):

    def __init__(self):
        self._current_config = GenerationConfig()
        self._presets: Dict[str, GenerationConfig] = {}
        self._logger = logging.getLogger(__name__)

    def get_current_config(self) -> GenerationConfig:
        return self._current_config

    def update_config(self, updates: Dict[str, Any]) -> None:
        try:
            self._current_config = self._current_config.with_updates(**updates)
        except Exception as e:
            self._logger.error(f"Failed to update config: {e}")
            raise

    def save_config_as_preset(self, name: str) -> None:
        self._presets[name] = self._current_config

    def load_config_preset(self, name: str) -> GenerationConfig:
        if name not in self._presets:
            raise ValueError(f"Preset '{name}' not found")
        config = self._presets[name]
        self._current_config = config
        return config

    def get_default_config(self) -> GenerationConfig:
        return GenerationConfig()

    def get_preset_names(self) -> List[str]:
        return list(self._presets.keys())


class GenerationValidationService(IGenerationValidationService):

    def validate_length(self, length: int, mode: GenerationMode) -> ValidationResult:
        errors = []
        warnings = []
        suggestions = []

        if length < 4:
            errors.append("Sequence length must be at least 4 beats")
        elif length > 32:
            errors.append("Sequence length cannot exceed 32 beats")
        elif length > 24:
            warnings.append("Large sequences may take longer to generate")

        if mode == GenerationMode.CIRCULAR and length % 4 != 0:
            suggestions.append(
                "Circular sequences work best with lengths divisible by 4"
            )

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
        )

    def validate_level(self, level: int, length: int) -> ValidationResult:
        errors = []
        warnings = []
        suggestions = []

        if level < 1:
            errors.append("Level must be at least 1")
        elif level > 6:
            errors.append("Level cannot exceed 6")

        if level > 4 and length < 8:
            warnings.append("High levels work better with longer sequences")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
        )

    def validate_turn_intensity(self, intensity: float, level: int) -> ValidationResult:
        errors = []
        warnings = []
        suggestions = []

        if intensity < 0.5:
            errors.append("Turn intensity must be at least 0.5")
        elif intensity > 3.0:
            errors.append("Turn intensity cannot exceed 3.0")

        if intensity > 2.0 and level < 3:
            warnings.append("High turn intensity works better with higher levels")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
        )

    def validate_letter_combination(
        self, letters: Set[LetterType], mode: GenerationMode
    ) -> ValidationResult:
        errors = []
        warnings = []
        suggestions = []

        if len(letters) == 0:
            errors.append("At least one letter type must be selected")
        elif len(letters) == 1:
            warnings.append("Single letter type sequences may be repetitive")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
        )

    def validate_complete_config(self, config: GenerationConfig) -> ValidationResult:
        all_errors = []
        all_warnings = []
        all_suggestions = []

        validations = [
            self.validate_length(config.length, config.mode),
            self.validate_level(config.level, config.length),
            self.validate_turn_intensity(config.turn_intensity, config.level),
            self.validate_letter_combination(config.letter_types or set(), config.mode),
        ]

        for validation in validations:
            if validation.errors:
                all_errors.extend(validation.errors)
            if validation.warnings:
                all_warnings.extend(validation.warnings)
            if validation.suggestions:
                all_suggestions.extend(validation.suggestions)

        return ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings,
            suggestions=all_suggestions,
        )


class GenerationHistoryService(IGenerationHistoryService):

    def __init__(self):
        self._generation_history: List[tuple[GenerationConfig, GenerationResult]] = []
        self._stats: Dict[str, Any] = {
            "total_generations": 0,
            "successful_generations": 0,
            "failed_generations": 0,
            "total_generation_time_ms": 0,
        }

    def record_generation(
        self, config: GenerationConfig, result: GenerationResult
    ) -> None:
        self._generation_history.append((config, result))

        self._stats["total_generations"] += 1
        if result.success:
            self._stats["successful_generations"] += 1
            if result.metadata:
                self._stats[
                    "total_generation_time_ms"
                ] += result.metadata.generation_time_ms
        else:
            self._stats["failed_generations"] += 1

        if len(self._generation_history) > 100:
            self._generation_history = self._generation_history[-100:]

    def get_recent_configs(self, limit: int = 10) -> List[GenerationConfig]:
        recent = self._generation_history[-limit:]
        return [config for config, _ in recent]

    def get_generation_stats(self) -> Dict[str, Any]:
        stats = self._stats.copy()
        if stats["successful_generations"] > 0:
            stats["average_generation_time_ms"] = int(
                stats["total_generation_time_ms"] / stats["successful_generations"]
            )
        else:
            stats["average_generation_time_ms"] = 0

        return stats

    def clear_history(self) -> None:
        self._generation_history.clear()
        self._stats = {
            "total_generations": 0,
            "successful_generations": 0,
            "failed_generations": 0,
            "total_generation_time_ms": 0,
        }
