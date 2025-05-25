"""
Tab manager responsible for managing all application tabs.

This component follows SRP by focusing solely on tab-related functionality.
"""

from typing import TYPE_CHECKING, Dict, Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QObject, pyqtSignal
import logging

from core.application_context import ApplicationContext

if TYPE_CHECKING:
    from .main_widget_coordinator import MainWidgetCoordinator

logger = logging.getLogger(__name__)


class TabManager(QObject):
    """
    Manages all application tabs with clear separation of concerns.

    Responsibilities:
    - Create and manage tab instances
    - Handle tab switching logic
    - Maintain tab state
    - Provide tab access interface
    """

    tab_changed = pyqtSignal(str)  # tab_name
    tab_ready = pyqtSignal(str)  # tab_name

    def __init__(
        self, coordinator: "MainWidgetCoordinator", app_context: ApplicationContext
    ):
        super().__init__(coordinator)

        self.coordinator = coordinator
        self.app_context = app_context
        self._tabs: Dict[str, QWidget] = {}
        self._current_tab: Optional[str] = None
        self._tab_factories = {}

        # Register tab factories
        self._register_tab_factories()

    def _register_tab_factories(self) -> None:
        """Register factories for creating different tab types."""
        # Import tab factories
        try:
            from main_window.main_widget.construct_tab.construct_tab_factory import (
                ConstructTabFactory,
            )
            from main_window.main_widget.generate_tab.generate_tab_factory import (
                GenerateTabFactory,
            )
            from main_window.main_widget.browse_tab.browse_tab_factory import (
                BrowseTabFactory,
            )
            from main_window.main_widget.learn_tab.learn_tab_factory import (
                LearnTabFactory,
            )
            from main_window.main_widget.write_tab.write_tab_factory import (
                WriteTabFactory,
            )
            from main_window.main_widget.sequence_card_tab.utils.tab_factory import (
                SequenceCardTabFactory,
            )

            self._tab_factories = {
                "construct": ConstructTabFactory,
                "generate": GenerateTabFactory,
                "browse": BrowseTabFactory,
                "learn": LearnTabFactory,
                "write": WriteTabFactory,
                "sequence_card": SequenceCardTabFactory,
            }

        except ImportError as e:
            logger.error(f"Failed to import tab factory: {e}")

    def initialize_tabs(self) -> None:
        """Initialize all tabs lazily."""
        logger.info("TabManager.initialize_tabs() called")

        try:
            # First populate the stacks with essential widgets
            logger.info("Populating stacks with essential widgets...")
            self._populate_stacks_with_essential_widgets()

            # Get the default tab from settings
            settings_manager = self.app_context.settings_manager
            default_tab = getattr(
                settings_manager.global_settings, "current_tab", "construct"
            )
            logger.info(f"Default tab from settings: {default_tab}")

            # Create the default tab first
            logger.info(f"Creating default tab: {default_tab}")
            tab_widget = self._create_tab(default_tab)
            if tab_widget:
                logger.info(
                    f"Default tab created successfully: {type(tab_widget).__name__}"
                )
            else:
                logger.error(f"Failed to create default tab: {default_tab}")

            # Switch to the default tab
            logger.info(f"Switching to default tab: {default_tab}")
            success = self.switch_to_tab(default_tab)
            if success:
                logger.info(f"Successfully switched to tab: {default_tab}")
            else:
                logger.error(f"Failed to switch to tab: {default_tab}")

            logger.info(
                f"TabManager initialization completed with default: {default_tab}"
            )

        except Exception as e:
            logger.error(f"TabManager initialization failed: {e}")
            import traceback

            traceback.print_exc()

    def _populate_stacks_with_essential_widgets(self) -> None:
        """Populate the stacks with essential widgets that should always be available."""
        try:
            print("DEBUG: Getting essential widgets from widget manager...")
            logger.info("Getting essential widgets from widget manager...")

            # Get essential widgets from widget manager
            sequence_workbench = self.coordinator.widget_manager.get_widget(
                "sequence_workbench"
            )
            codex = self.coordinator.widget_manager.get_widget("codex")

            print(f"DEBUG: sequence_workbench widget: {sequence_workbench}")
            print(f"DEBUG: codex widget: {codex}")
            logger.info(f"sequence_workbench widget: {sequence_workbench}")
            logger.info(f"codex widget: {codex}")

            # Add to left stack (index 0 and 1 are reserved for these)
            if sequence_workbench:
                self.coordinator.left_stack.addWidget(sequence_workbench)  # Index 0
                print("DEBUG: ✅ Added sequence_workbench to left stack")
                logger.info("✅ Added sequence_workbench to left stack")
            else:
                print(
                    "DEBUG: ❌ sequence_workbench widget is None - not added to stack"
                )
                logger.warning(
                    "❌ sequence_workbench widget is None - not added to stack"
                )

            if codex:
                self.coordinator.left_stack.addWidget(codex)  # Index 1
                print("DEBUG: ✅ Added codex to left stack")
                logger.info("✅ Added codex to left stack")
            else:
                print("DEBUG: ❌ codex widget is None - not added to stack")
                logger.warning("❌ codex widget is None - not added to stack")

            print(
                f"DEBUG: Left stack now has {self.coordinator.left_stack.count()} widgets"
            )
            print(
                f"DEBUG: Right stack now has {self.coordinator.right_stack.count()} widgets"
            )
            logger.info(
                f"Left stack now has {self.coordinator.left_stack.count()} widgets"
            )
            logger.info(
                f"Right stack now has {self.coordinator.right_stack.count()} widgets"
            )

        except Exception as e:
            print(f"DEBUG: Failed to populate stacks with essential widgets: {e}")
            logger.error(f"Failed to populate stacks with essential widgets: {e}")
            import traceback

            traceback.print_exc()

    def _create_tab(self, tab_name: str) -> Optional[QWidget]:
        """
        Create a tab instance if it doesn't exist.

        Args:
            tab_name: Name of the tab to create

        Returns:
            The tab widget or None if creation failed
        """
        print(f"DEBUG: _create_tab called for: {tab_name}")

        if tab_name in self._tabs:
            print(f"DEBUG: Tab {tab_name} already exists, returning existing")
            return self._tabs[tab_name]

        if tab_name not in self._tab_factories:
            print(f"DEBUG: ❌ No factory registered for tab: {tab_name}")
            logger.error(f"No factory registered for tab: {tab_name}")
            return None

        try:
            factory = self._tab_factories[tab_name]
            print(f"DEBUG: Creating tab {tab_name} using factory {factory.__name__}")

            # Debug app_context services
            print(f"DEBUG: app_context: {self.app_context}")
            print(
                f"DEBUG: app_context.settings_manager: {self.app_context.settings_manager}"
            )
            print(f"DEBUG: app_context.json_manager: {self.app_context.json_manager}")

            # Create tab with dependency injection
            tab_widget = factory.create(
                parent=self.coordinator, app_context=self.app_context
            )

            print(
                f"DEBUG: ✅ Tab {tab_name} created successfully: {type(tab_widget).__name__}"
            )

            self._tabs[tab_name] = tab_widget

            # Add to appropriate stack
            print(f"DEBUG: Adding tab {tab_name} to stack...")
            self._add_tab_to_stack(tab_name, tab_widget)

            self.tab_ready.emit(tab_name)
            logger.info(f"Created tab: {tab_name}")

            return tab_widget

        except Exception as e:
            print(f"DEBUG: ❌ Failed to create tab {tab_name}: {e}")
            logger.error(f"Failed to create tab {tab_name}: {e}")
            return None

    def _add_tab_to_stack(self, tab_name: str, tab_widget: QWidget) -> None:
        """Add tab to the appropriate stack widget."""
        # Note: Left stack indices 0 and 1 are reserved for sequence_workbench and codex
        # Tab-specific widgets start from index 2 onwards

        if tab_name == "construct":
            # Construct tab components go to right stack
            if hasattr(tab_widget, "start_pos_picker"):
                self.coordinator.right_stack.addWidget(
                    tab_widget.start_pos_picker
                )  # Index 0
            if hasattr(tab_widget, "advanced_start_pos_picker"):
                self.coordinator.right_stack.addWidget(
                    tab_widget.advanced_start_pos_picker
                )  # Index 1
            if hasattr(tab_widget, "option_picker"):
                self.coordinator.right_stack.addWidget(
                    tab_widget.option_picker
                )  # Index 2
        elif tab_name == "generate":
            self.coordinator.right_stack.addWidget(tab_widget)  # Index 3
        elif tab_name == "learn":
            self.coordinator.right_stack.addWidget(tab_widget)  # Index 4
        elif tab_name == "browse":
            # Browse tab has multiple components
            if hasattr(tab_widget, "sequence_picker"):
                if hasattr(tab_widget.sequence_picker, "filter_stack"):
                    self.coordinator.left_stack.addWidget(
                        tab_widget.sequence_picker.filter_stack
                    )  # Index 2
                self.coordinator.left_stack.addWidget(
                    tab_widget.sequence_picker
                )  # Index 3
                if hasattr(tab_widget, "sequence_viewer"):
                    self.coordinator.right_stack.addWidget(
                        tab_widget.sequence_viewer
                    )  # Index 5
        elif tab_name == "sequence_card":
            self.coordinator.right_stack.addWidget(tab_widget)  # Index 6
        else:
            # Default: add to right stack
            self.coordinator.right_stack.addWidget(tab_widget)

    def switch_to_tab(self, tab_name: str) -> bool:
        """
        Switch to a specific tab.

        Args:
            tab_name: Name of the tab to switch to

        Returns:
            True if successful, False otherwise
        """
        # Create tab if it doesn't exist
        tab_widget = self._create_tab(tab_name)
        if not tab_widget:
            return False

        # Update current tab
        old_tab = self._current_tab
        self._current_tab = tab_name

        # Switch stack widgets
        self._switch_stack_widgets(tab_name, tab_widget)

        # Emit signal
        self.tab_changed.emit(tab_name)

        logger.info(f"Switched from {old_tab} to {tab_name}")
        return True

    def _switch_stack_widgets(self, tab_name: str, tab_widget: QWidget) -> None:
        """Switch the stack widgets to show the correct tab."""
        # Switch left stack based on tab
        if tab_name == "construct":
            # Show sequence_workbench (index 0) for construct tab
            self.coordinator.left_stack.setCurrentIndex(0)
            # Show construct tab's start_pos_picker (index 0) on right stack
            self.coordinator.right_stack.setCurrentIndex(0)
        elif tab_name == "generate":
            # Show sequence_workbench (index 0) for generate tab
            self.coordinator.left_stack.setCurrentIndex(0)
            # Show generate tab (index 3) on right stack
            self.coordinator.right_stack.setCurrentIndex(3)
        elif tab_name == "learn":
            # Show sequence_workbench (index 0) for learn tab
            self.coordinator.left_stack.setCurrentIndex(0)
            # Show learn tab (index 4) on right stack
            self.coordinator.right_stack.setCurrentIndex(4)
        elif tab_name == "browse":
            # Show browse tab's filter_stack (index 2) on left stack
            self.coordinator.left_stack.setCurrentIndex(2)
            # Show browse tab's sequence_viewer (index 5) on right stack
            self.coordinator.right_stack.setCurrentIndex(5)
        elif tab_name == "sequence_card":
            # Show sequence_workbench (index 0) for sequence card tab
            self.coordinator.left_stack.setCurrentIndex(0)
            # Show sequence card tab (index 6) on right stack
            self.coordinator.right_stack.setCurrentIndex(6)
        else:
            # Default: show sequence_workbench on left, tab widget on right
            self.coordinator.left_stack.setCurrentIndex(0)
            if tab_widget in [
                self.coordinator.right_stack.widget(i)
                for i in range(self.coordinator.right_stack.count())
            ]:
                self.coordinator.right_stack.setCurrentWidget(tab_widget)

    def get_tab_widget(self, tab_name: str) -> Optional[QWidget]:
        """
        Get a tab widget by name.

        Args:
            tab_name: Name of the tab

        Returns:
            The tab widget or None if not found
        """
        return self._tabs.get(tab_name)

    def get_current_tab(self) -> Optional[str]:
        """Get the name of the currently active tab."""
        return self._current_tab

    def is_tab_created(self, tab_name: str) -> bool:
        """Check if a tab has been created."""
        return tab_name in self._tabs

    def get_available_tabs(self) -> list[str]:
        """Get list of available tab names."""
        return list(self._tab_factories.keys())

    def on_widget_ready(self, widget_name: str) -> None:
        """Handle widget ready events that might affect tabs."""
        # Update tabs that depend on specific widgets
        if widget_name == "sequence_workbench":
            # Some tabs might need the sequence workbench
            for tab_name, tab_widget in self._tabs.items():
                if hasattr(tab_widget, "on_sequence_workbench_ready"):
                    tab_widget.on_sequence_workbench_ready()

    def cleanup(self) -> None:
        """Cleanup tab resources."""
        for tab_name, tab_widget in self._tabs.items():
            if hasattr(tab_widget, "cleanup"):
                try:
                    tab_widget.cleanup()
                except Exception as e:
                    logger.error(f"Error cleaning up tab {tab_name}: {e}")

        self._tabs.clear()
        self._current_tab = None
        logger.info("Tab manager cleaned up")
