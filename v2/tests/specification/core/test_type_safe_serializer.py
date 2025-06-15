"""
TEST LIFECYCLE: specification
CREATED: 2025-06-14
PURPOSE: Contract testing for TypeSafeSerializer cross-language serialization
SCOPE: Domain model serialization, type validation, round-trip integrity
EXPECTED_DURATION: permanent
"""

import pytest
import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from datetime import datetime

from core.serialization.type_safe_serializer import (
    TypeSafeSerializer,
    BatchSerializer,
    SerializationError,
)
from domain.models.core_models import (
    BeatData,
    SequenceData,
    MotionData,
    MotionType,
    RotationDirection,
    Location,
)


@dataclass(frozen=True)
class TestDomainModel:
    """Test domain model for serialization testing."""

    id: str
    name: str
    value: int
    optional_field: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "optional_field": self.optional_field,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TestDomainModel":
        return cls(
            id=data["id"],
            name=data["name"],
            value=data["value"],
            optional_field=data.get("optional_field"),
        )


class TestTypeValidation:
    """Test type validation and metadata handling."""

    def test_serialize_adds_type_metadata(self):
        """Test that serialization adds required type metadata."""
        model = TestDomainModel("test-id", "test-name", 42)

        result = TypeSafeSerializer.serialize(model)

        assert "__type__" in result
        assert "__version__" in result
        assert "__serialized_at__" in result
        assert result["__type__"].endswith("TestDomainModel")
        assert result["__version__"] == "1.0"

        # Verify timestamp is valid ISO format
        datetime.fromisoformat(result["__serialized_at__"])

    def test_serialize_preserves_original_data(self):
        """Test that serialization preserves original object data."""
        model = TestDomainModel("test-id", "test-name", 42, "optional")

        result = TypeSafeSerializer.serialize(model)

        assert result["id"] == "test-id"
        assert result["name"] == "test-name"
        assert result["value"] == 42
        assert result["optional_field"] == "optional"

    def test_serialize_rejects_non_dataclass(self):
        """Test that serialization rejects non-dataclass objects."""
        with pytest.raises(SerializationError, match="only dataclasses supported"):
            TypeSafeSerializer.serialize("not a dataclass")

    def test_serialize_requires_to_dict_method(self):
        """Test that serialization requires to_dict method."""

        @dataclass
        class ModelWithoutToDict:
            value: int

        model = ModelWithoutToDict(42)

        with pytest.raises(SerializationError, match="must implement to_dict"):
            TypeSafeSerializer.serialize(model)


class TestDeserialization:
    """Test deserialization and type validation."""

    def test_deserialize_validates_type_metadata(self):
        """Test that deserialization validates type metadata."""
        data = {"id": "test", "name": "test", "value": 42}

        with pytest.raises(SerializationError, match="Missing type information"):
            TypeSafeSerializer.deserialize(data, TestDomainModel)

    def test_deserialize_validates_type_match(self):
        """Test that deserialization validates type matching."""
        data = {
            "__type__": "wrong.module.WrongType",
            "__version__": "1.0",
            "id": "test",
            "name": "test",
            "value": 42,
        }

        with pytest.raises(SerializationError, match="Type mismatch"):
            TypeSafeSerializer.deserialize(data, TestDomainModel)

    def test_deserialize_requires_from_dict_method(self):
        """Test that deserialization requires from_dict method."""

        @dataclass
        class ModelWithoutFromDict:
            value: int

        data = {
            "__type__": f"{ModelWithoutFromDict.__module__}.{ModelWithoutFromDict.__name__}",
            "__version__": "1.0",
            "value": 42,
        }

        with pytest.raises(SerializationError, match="must implement from_dict"):
            TypeSafeSerializer.deserialize(data, ModelWithoutFromDict)

    def test_deserialize_handles_version_warnings(self, caplog):
        """Test that deserialization handles version compatibility."""
        data = {
            "__type__": f"{TestDomainModel.__module__}.{TestDomainModel.__name__}",
            "__version__": "2.0",  # Future version
            "id": "test",
            "name": "test",
            "value": 42,
        }

        # Should still work but log warning
        result = TypeSafeSerializer.deserialize(data, TestDomainModel)
        assert isinstance(result, TestDomainModel)
        assert "Potentially incompatible version" in caplog.text


class TestRoundTripSerialization:
    """Test round-trip serialization integrity."""

    def test_simple_model_round_trip(self):
        """Test round-trip serialization of simple model."""
        original = TestDomainModel("test-id", "test-name", 42, "optional")

        # Serialize and deserialize
        serialized = TypeSafeSerializer.serialize(original)
        deserialized = TypeSafeSerializer.deserialize(serialized, TestDomainModel)

        assert deserialized == original

    def test_motion_data_round_trip(self):
        """Test round-trip serialization of MotionData."""
        original = MotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            turns=1.5,
            start_ori="in",
            end_ori="out",
        )

        serialized = TypeSafeSerializer.serialize(original)
        deserialized = TypeSafeSerializer.deserialize(serialized, MotionData)

        assert deserialized == original

    def test_beat_data_round_trip(self):
        """Test round-trip serialization of BeatData."""
        motion = MotionData(
            motion_type=MotionType.DASH,
            prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
            start_loc=Location.EAST,
            end_loc=Location.WEST,
            turns=2.0,
        )

        original = BeatData(
            beat_number=1,
            letter="A",
            duration=1.5,
            blue_motion=motion,
            red_motion=motion,
            blue_reversal=True,
            metadata={"test": "value"},
        )

        serialized = TypeSafeSerializer.serialize(original)
        deserialized = TypeSafeSerializer.deserialize(serialized, BeatData)

        assert deserialized == original

    def test_sequence_data_round_trip(self):
        """Test round-trip serialization of SequenceData."""
        beat = BeatData(letter="A", duration=1.0)
        original = SequenceData(
            name="Test Sequence",
            word="TEST",
            beats=[beat],
            start_position="alpha1",
            metadata={"author": "test"},
        )

        serialized = TypeSafeSerializer.serialize(original)
        deserialized = TypeSafeSerializer.deserialize(serialized, SequenceData)

        assert deserialized == original


class TestJSONSerialization:
    """Test JSON string serialization."""

    def test_serialize_to_json_string(self):
        """Test serialization to JSON string."""
        model = TestDomainModel("test-id", "test-name", 42)

        json_str = TypeSafeSerializer.serialize_to_json(model)

        # Should be valid JSON
        data = json.loads(json_str)
        assert data["id"] == "test-id"
        assert "__type__" in data

    def test_deserialize_from_json_string(self):
        """Test deserialization from JSON string."""
        original = TestDomainModel("test-id", "test-name", 42)

        json_str = TypeSafeSerializer.serialize_to_json(original)
        deserialized = TypeSafeSerializer.deserialize_from_json(
            json_str, TestDomainModel
        )

        assert deserialized == original

    def test_deserialize_from_invalid_json(self):
        """Test error handling for invalid JSON."""
        with pytest.raises(SerializationError, match="Invalid JSON"):
            TypeSafeSerializer.deserialize_from_json("invalid json", TestDomainModel)


class TestSchemaValidation:
    """Test schema validation functionality."""

    def test_validate_schema_success(self):
        """Test successful schema validation."""
        model = TestDomainModel("test-id", "test-name", 42)

        result = TypeSafeSerializer.validate_schema(model)
        assert result is True

    def test_validate_schema_requires_dataclass(self):
        """Test that schema validation requires dataclass."""
        with pytest.raises(SerializationError, match="must be a dataclass"):
            TypeSafeSerializer.validate_schema("not a dataclass")

    def test_validate_schema_requires_to_dict(self):
        """Test that schema validation requires to_dict method."""

        @dataclass
        class ModelWithoutToDict:
            value: int

        model = ModelWithoutToDict(42)

        with pytest.raises(SerializationError, match="must implement to_dict"):
            TypeSafeSerializer.validate_schema(model)

    def test_validate_schema_requires_from_dict(self):
        """Test that schema validation requires from_dict method."""

        @dataclass
        class ModelWithoutFromDict:
            value: int

            def to_dict(self):
                return {"value": self.value}

        model = ModelWithoutFromDict(42)

        with pytest.raises(SerializationError, match="must implement from_dict"):
            TypeSafeSerializer.validate_schema(model)


class TestBatchSerialization:
    """Test batch serialization functionality."""

    def test_serialize_empty_list(self):
        """Test serialization of empty list."""
        result = BatchSerializer.serialize_list([], TestDomainModel)

        assert result["__batch_type__"] == "list"
        assert result["__count__"] == 0
        assert result["items"] == []

    def test_serialize_list_of_models(self):
        """Test serialization of list of models."""
        models = [
            TestDomainModel("id1", "name1", 1),
            TestDomainModel("id2", "name2", 2),
        ]

        result = BatchSerializer.serialize_list(models, TestDomainModel)

        assert result["__batch_type__"] == "list"
        assert result["__count__"] == 2
        assert len(result["items"]) == 2
        assert result["items"][0]["id"] == "id1"
        assert result["items"][1]["id"] == "id2"

    def test_deserialize_list_of_models(self):
        """Test deserialization of list of models."""
        models = [
            TestDomainModel("id1", "name1", 1),
            TestDomainModel("id2", "name2", 2),
        ]

        serialized = BatchSerializer.serialize_list(models, TestDomainModel)
        deserialized = BatchSerializer.deserialize_list(serialized, TestDomainModel)

        assert len(deserialized) == 2
        assert deserialized[0] == models[0]
        assert deserialized[1] == models[1]

    def test_batch_type_validation(self):
        """Test batch type validation."""
        invalid_data = {"__batch_type__": "not_list"}

        with pytest.raises(SerializationError, match="not a serialized list"):
            BatchSerializer.deserialize_list(invalid_data, TestDomainModel)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
