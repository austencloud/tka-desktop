from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

from core.dependency_injection.di_container import DIContainer
from domain.models.core_models import SequenceData
from application.services.ui.ui_state_management_service import UIStateManagementService

# Import refactored components
from .layout_manager import ConstructTabLayoutManager
from .start_position_handler import StartPositionHandler
from .option_picker_manager import OptionPickerManager
from .sequence_manager import SequenceManager
from .signal_coordinator import SignalCoordinator
from .data_conversion_service import DataConversionService


class ConstructTabWidget(QWidget):
    """
    Refactored ConstructTabWidget using composition and dependency injection.

    This streamlined version coordinates between specialized component classes:
    - LayoutManager: Handles UI layout and panel creation
    - StartPositionHandler: Manages start position selection
    - OptionPickerManager: Handles option picker operations
    - SequenceManager: Manages sequence operations
    - SignalCoordinator: Coordinates signals between components
    - DataConversionService: Handles data conversions and caching
    """

    sequence_created = pyqtSignal(object)  # SequenceData object
    sequence_modified = pyqtSignal(object)  # SequenceData object
    start_position_set = pyqtSignal(
        str
    )  # Emits position key when start position is set

    def __init__(
        self,
        container: DIContainer,
        parent: Optional[QWidget] = None,
        progress_callback=None,
    ):
        super().__init__(parent)
        self.container = container
        self.progress_callback = progress_callback
        self.state_service = UIStateManagementService()

        # Initialize component services
        self._initialize_components()

        # Setup UI and connect signals
        self._setup_ui_with_progress()
        self._connect_external_signals()

    def _initialize_components(self):
        """Initialize all component services using dependency injection"""

        # Data conversion service (no dependencies)
        self.data_conversion_service = DataConversionService()

        # Layout manager
        self.layout_manager = ConstructTabLayoutManager(
            self.container, self.progress_callback
        )

        # Start position handler
        self.start_position_handler = StartPositionHandler(
            self.data_conversion_service, workbench_setter=self._get_workbench_setter()
        )

        # Sequence manager
        self.sequence_manager = SequenceManager(
            workbench_getter=self._get_workbench_getter(),
            workbench_setter=self._get_workbench_setter(),
        )

        # Option picker manager (will be initialized after layout)
        self.option_picker_manager = None

        # Signal coordinator (will be initialized after all components)
        self.signal_coordinator = None

    def _setup_ui_with_progress(self):
        """Setup UI using the layout manager"""
        # Delegate UI setup to layout manager
        self.layout_manager.setup_ui(self)

        # Initialize option picker manager after layout is created
        self.option_picker_manager = OptionPickerManager(
            self.layout_manager.option_picker, self.data_conversion_service
        )

        # Initialize signal coordinator after all components are ready
        self.signal_coordinator = SignalCoordinator(
            self.layout_manager,
            self.start_position_handler,
            self.option_picker_manager,
            self.sequence_manager,
        )

    def _connect_external_signals(self):
        """Connect external signals from the signal coordinator to this widget"""
        if (
            self.signal_coordinator
        ):  # Forward signals from signal coordinator to external listeners
            self.signal_coordinator.sequence_created.connect(self.sequence_created.emit)
            self.signal_coordinator.sequence_modified.connect(
                self.sequence_modified.emit
            )
            self.signal_coordinator.start_position_set.connect(
                self.start_position_set.emit
            )

            # NOTE: Workbench signals are already connected in signal_coordinator._setup_signal_connections()
            # No need for additional external connections here

    def _get_workbench_getter(self):
        """Get a function that returns the workbench"""

        def get_workbench():
            return getattr(self.layout_manager, "workbench", None)

        return get_workbench

    def _get_workbench_setter(self):
        """Get a function that can set data on the workbench"""

        def set_workbench_data(data):
            workbench = getattr(self.layout_manager, "workbench", None)
            if workbench:
                if hasattr(data, "beats"):  # SequenceData
                    workbench.set_sequence(data)
                else:  # BeatData (start position)
                    workbench.set_start_position(data)

        return set_workbench_data

    # Public interface methods
    def clear_sequence(self):
        """Clear the current sequence and reset to start position picker"""
        if self.signal_coordinator:
            self.signal_coordinator.clear_sequence()

    def force_picker_update(self):
        """Force an update of the picker state based on current sequence state"""
        if self.signal_coordinator:
            self.signal_coordinator.force_picker_state_update()

    @property
    def workbench(self):
        """Access to the workbench component"""
        return getattr(self.layout_manager, "workbench", None)
