"""
TypeSafe Serialization for Modern Kinetic Constructor

Ensures data integrity for cross-language communication and provides
validation for all domain model serialization operations.
"""

from typing import Any, Dict, Type, TypeVar, get_type_hints, Union
import json
import logging
from dataclasses import is_dataclass
from datetime import datetime

T = TypeVar("T")
logger = logging.getLogger(__name__)


class SerializationError(Exception):
    """Raised when serialization/deserialization fails."""

    pass


class TypeSafeSerializer:
    """
    Ensures data integrity for cross-language communication.

    Features:
    - Full type information preservation
    - Version tracking for schema evolution
    - Validation of serialized data
    - Cross-language compatibility
    """

    @staticmethod
    def serialize(obj: Any) -> Dict[str, Any]:
        """
        Serialize with full type information.

        Args:
            obj: Object to serialize (must be a dataclass)

        Returns:
            Dictionary with type metadata and serialized data

        Raises:
            SerializationError: If object cannot be serialized
        """
        if not is_dataclass(obj):
            raise SerializationError(
                f"Cannot serialize {type(obj)} - only dataclasses supported"
            )

        try:
            # Get base serialization from object's to_dict method
            if hasattr(obj, "to_dict"):
                result = obj.to_dict()
            else:
                raise SerializationError(f"{type(obj)} must implement to_dict() method")

            # Add type metadata
            result["__type__"] = f"{obj.__class__.__module__}.{obj.__class__.__name__}"
            result["__version__"] = getattr(obj, "__version__", "1.0")
            result["__serialized_at__"] = datetime.utcnow().isoformat()

            # Validate serialized data
            TypeSafeSerializer._validate_serialized_data(result)

            return result

        except Exception as e:
            logger.error(f"Serialization failed for {type(obj)}: {e}")
            raise SerializationError(f"Failed to serialize {type(obj)}: {e}")

    @staticmethod
    def deserialize(data: Dict[str, Any], expected_type: Type[T]) -> T:
        """
        Deserialize with type validation.

        Args:
            data: Serialized data dictionary
            expected_type: Expected type for deserialization

        Returns:
            Deserialized object of expected type

        Raises:
            SerializationError: If deserialization fails or type mismatch
        """
        if not isinstance(data, dict):
            raise SerializationError("Serialized data must be a dictionary")

        # Validate type metadata
        if "__type__" not in data:
            raise SerializationError("Missing type information in serialized data")

        type_name = data["__type__"]
        expected_type_name = f"{expected_type.__module__}.{expected_type.__name__}"

        if not type_name.endswith(expected_type.__name__):
            raise SerializationError(
                f"Type mismatch: expected {expected_type_name}, got {type_name}"
            )

        # Check version compatibility
        version = data.get("__version__", "1.0")
        if not TypeSafeSerializer._is_version_compatible(version):
            logger.warning(f"Potentially incompatible version: {version}")

        try:
            # Remove metadata before deserialization
            clean_data = {k: v for k, v in data.items() if not k.startswith("__")}

            # Use object's from_dict method
            if hasattr(expected_type, "from_dict"):
                return expected_type.from_dict(clean_data)
            else:
                raise SerializationError(
                    f"{expected_type} must implement from_dict() method"
                )

        except Exception as e:
            logger.error(f"Deserialization failed for {expected_type}: {e}")
            raise SerializationError(f"Failed to deserialize {expected_type}: {e}")

    @staticmethod
    def serialize_to_json(obj: Any, indent: int = 2) -> str:
        """
        Serialize object to JSON string.

        Args:
            obj: Object to serialize
            indent: JSON indentation level

        Returns:
            JSON string representation
        """
        serialized = TypeSafeSerializer.serialize(obj)
        return json.dumps(serialized, indent=indent, ensure_ascii=False)

    @staticmethod
    def deserialize_from_json(json_str: str, expected_type: Type[T]) -> T:
        """
        Deserialize object from JSON string.

        Args:
            json_str: JSON string to deserialize
            expected_type: Expected type for deserialization

        Returns:
            Deserialized object
        """
        try:
            data = json.loads(json_str)
            return TypeSafeSerializer.deserialize(data, expected_type)
        except json.JSONDecodeError as e:
            raise SerializationError(f"Invalid JSON: {e}")

    @staticmethod
    def validate_schema(obj: Any) -> bool:
        """
        Validate that object can be safely serialized and deserialized.

        Args:
            obj: Object to validate

        Returns:
            True if object passes validation

        Raises:
            SerializationError: If validation fails
        """
        if not is_dataclass(obj):
            raise SerializationError("Object must be a dataclass")

        if not hasattr(obj, "to_dict"):
            raise SerializationError("Object must implement to_dict() method")

        if not hasattr(obj.__class__, "from_dict"):
            raise SerializationError(
                "Object class must implement from_dict() class method"
            )

        # Test round-trip serialization
        try:
            serialized = TypeSafeSerializer.serialize(obj)
            deserialized = TypeSafeSerializer.deserialize(serialized, type(obj))

            # Verify equality (if object implements __eq__)
            if hasattr(obj, "__eq__"):
                if obj != deserialized:
                    raise SerializationError(
                        "Round-trip serialization failed - objects not equal"
                    )

            return True

        except Exception as e:
            raise SerializationError(f"Schema validation failed: {e}")

    @staticmethod
    def _validate_serialized_data(data: Dict[str, Any]) -> None:
        """Validate serialized data structure."""
        required_metadata = ["__type__", "__version__", "__serialized_at__"]

        for field in required_metadata:
            if field not in data:
                raise SerializationError(f"Missing required metadata field: {field}")

        # Validate type string format
        type_str = data["__type__"]
        if "." not in type_str:
            raise SerializationError(f"Invalid type format: {type_str}")

    @staticmethod
    def _is_version_compatible(version: str) -> bool:
        """Check if version is compatible with current serializer."""
        # Simple version compatibility check
        # In production, implement proper semantic versioning
        try:
            major, minor = version.split(".")[:2]
            return int(major) == 1  # Compatible with legacy.x
        except (ValueError, IndexError):
            return False


class BatchSerializer:
    """Utility for serializing collections of objects efficiently."""

    @staticmethod
    def serialize_list(objects: list, object_type: Type[T]) -> Dict[str, Any]:
        """Serialize a list of objects with batch metadata."""
        if not objects:
            return {
                "__batch_type__": "list",
                "__item_type__": f"{object_type.__module__}.{object_type.__name__}",
                "__count__": 0,
                "__serialized_at__": datetime.utcnow().isoformat(),
                "items": [],
            }

        # Validate all objects are of expected type
        for obj in objects:
            if not isinstance(obj, object_type):
                raise SerializationError(f"All objects must be of type {object_type}")

        serialized_items = [TypeSafeSerializer.serialize(obj) for obj in objects]

        return {
            "__batch_type__": "list",
            "__item_type__": f"{object_type.__module__}.{object_type.__name__}",
            "__count__": len(objects),
            "__serialized_at__": datetime.utcnow().isoformat(),
            "items": serialized_items,
        }

    @staticmethod
    def deserialize_list(data: Dict[str, Any], object_type: Type[T]) -> list[T]:
        """Deserialize a list of objects from batch data."""
        if data.get("__batch_type__") != "list":
            raise SerializationError("Data is not a serialized list")

        expected_type_name = f"{object_type.__module__}.{object_type.__name__}"
        actual_type_name = data.get("__item_type__")

        if actual_type_name != expected_type_name:
            raise SerializationError(
                f"Type mismatch: expected {expected_type_name}, got {actual_type_name}"
            )

        items_data = data.get("items", [])
        expected_count = data.get("__count__", 0)

        if len(items_data) != expected_count:
            raise SerializationError(
                f"Count mismatch: expected {expected_count}, got {len(items_data)}"
            )

        return [
            TypeSafeSerializer.deserialize(item_data, object_type)
            for item_data in items_data
        ]
