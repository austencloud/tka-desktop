from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.editable_label import EditableLabel


class EditableLabelManager:
    """Manages the currently active EditableLabel to ensure only one is open at a time."""

    _current_editable = None  # Track the currently active EditableLabel

    @classmethod
    def set_active(cls, editable_label: "EditableLabel"):
        """Set a new active EditableLabel and close the previous one if needed."""
        if cls._current_editable and cls._current_editable != editable_label:
            cls._current_editable._hide_edit()  # Hide the previous active label
        cls._current_editable = editable_label

    @classmethod
    def clear_active(cls):
        """Clear the currently active EditableLabel."""
        cls._current_editable = None
