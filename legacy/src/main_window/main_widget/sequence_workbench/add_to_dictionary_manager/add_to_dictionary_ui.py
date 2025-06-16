from typing import TYPE_CHECKING
from .dictionary_service import DictionaryService

if TYPE_CHECKING:
    from main_window.main_widget.sequence_workbench.sequence_workbench import (
        SequenceWorkbench,
    )


class AddToDictionaryUI:
    """
    User interface component for adding sequences to the dictionary.
    This class serves as a thin wrapper around the DictionaryService,
    bridging between UI events and the service layer.
    """

    def __init__(self, sequence_workbench: "SequenceWorkbench"):
        """
        Initialize the UI component.

        Args:
            sequence_workbench: The sequence workbench that contains this component
        """
        self.sequence_workbench = sequence_workbench
        self.dictionary_service: "DictionaryService" = (
            sequence_workbench.dictionary_service
        )

    def add_to_dictionary(self) -> None:
        """
        Callback for the "Add to Dictionary" button.
        Delegates to the dictionary service which contains the core logic.
        """
        # Simply delegate to the service layer which contains all the logic
        self.dictionary_service.add_to_dictionary()
