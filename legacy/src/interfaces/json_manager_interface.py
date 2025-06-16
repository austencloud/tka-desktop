from typing import Dict, Any, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class IJsonManager(Protocol):
    """Interface for the JSON manager."""

    def save_sequence(self, sequence_data: List[Dict[str, Any]]) -> bool:
        """Save the current sequence to the default location."""
        ...

    def load_sequence(self, file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """Load a sequence from the specified file path or the default location."""
        ...

    def get_updater(self):
        """Get the JSON sequence updater."""
        ...
