"""
State manager responsible for managing application state.

This component follows SRP by focusing solely on state management.
"""

from typing import TYPE_CHECKING, Dict, Any, Optional
from PyQt6.QtCore import QObject, pyqtSignal
import logging

from core.application_context import ApplicationContext

if TYPE_CHECKING:
    from .main_widget_coordinator import MainWidgetCoordinator

logger = logging.getLogger(__name__)


class StateManager(QObject):
    """
    Manages application state with clear separation of concerns.
    
    Responsibilities:
    - Track current application state
    - Handle state persistence
    - Provide state access interface
    - Emit state change notifications
    """
    
    state_changed = pyqtSignal(dict)  # state_data
    tab_changed = pyqtSignal(str)     # tab_name
    
    def __init__(self, coordinator: "MainWidgetCoordinator", app_context: ApplicationContext):
        super().__init__(coordinator)
        
        self.coordinator = coordinator
        self.app_context = app_context
        self._current_tab: Optional[str] = None
        self._state_data: Dict[str, Any] = {}
        
        # Initialize default state
        self._initialize_default_state()
    
    def _initialize_default_state(self) -> None:
        """Initialize default application state."""
        self._state_data = {
            "current_tab": None,
            "window_geometry": None,
            "user_preferences": {},
            "session_data": {},
            "ui_state": {
                "sidebar_expanded": True,
                "panels_visible": True,
            }
        }
    
    def initialize_state(self) -> None:
        """Initialize state from settings and restore previous session."""
        try:
            settings_manager = self.app_context.settings_manager
            
            # Load current tab from settings
            current_tab = getattr(settings_manager.global_settings, 'current_tab', 'construct')
            self.set_current_tab(current_tab)
            
            # Load other state from settings
            self._load_state_from_settings()
            
            logger.info(f"Initialized state with current tab: {current_tab}")
            
        except Exception as e:
            logger.error(f"Failed to initialize state: {e}")
            # Use defaults if loading fails
    
    def _load_state_from_settings(self) -> None:
        """Load state data from settings manager."""
        try:
            settings_manager = self.app_context.settings_manager
            
            # Load UI preferences
            if hasattr(settings_manager, 'global_settings'):
                global_settings = settings_manager.global_settings
                
                self._state_data["ui_state"].update({
                    "grid_mode": getattr(global_settings, 'grid_mode', 'diamond'),
                    "prop_type": getattr(global_settings, 'prop_type', 'Staff'),
                    "background_type": getattr(global_settings, 'background_type', 'Snowfall'),
                    "grow_sequence": getattr(global_settings, 'grow_sequence', True),
                    "enable_fades": getattr(global_settings, 'enable_fades', False),
                })
            
        except Exception as e:
            logger.error(f"Failed to load state from settings: {e}")
    
    def set_current_tab(self, tab_name: str) -> None:
        """
        Set the current active tab.
        
        Args:
            tab_name: Name of the tab to set as current
        """
        old_tab = self._current_tab
        self._current_tab = tab_name
        self._state_data["current_tab"] = tab_name
        
        # Persist to settings
        self._persist_current_tab(tab_name)
        
        # Emit signals
        if old_tab != tab_name:
            self.tab_changed.emit(tab_name)
            self.state_changed.emit(self._state_data.copy())
        
        logger.debug(f"Current tab changed from {old_tab} to {tab_name}")
    
    def _persist_current_tab(self, tab_name: str) -> None:
        """Persist current tab to settings."""
        try:
            settings_manager = self.app_context.settings_manager
            if hasattr(settings_manager, 'global_settings'):
                settings_manager.global_settings.set_current_tab(tab_name)
        except Exception as e:
            logger.error(f"Failed to persist current tab: {e}")
    
    @property
    def current_tab(self) -> Optional[str]:
        """Get the current active tab."""
        return self._current_tab
    
    def get_state(self, key: str = None) -> Any:
        """
        Get state data.
        
        Args:
            key: Specific state key to get. If None, returns all state.
            
        Returns:
            The requested state data
        """
        if key is None:
            return self._state_data.copy()
        
        return self._state_data.get(key)
    
    def set_state(self, key: str, value: Any, persist: bool = True) -> None:
        """
        Set state data.
        
        Args:
            key: State key to set
            value: Value to set
            persist: Whether to persist the change to settings
        """
        old_value = self._state_data.get(key)
        self._state_data[key] = value
        
        if persist:
            self._persist_state_key(key, value)
        
        # Emit signal if value changed
        if old_value != value:
            self.state_changed.emit(self._state_data.copy())
        
        logger.debug(f"State key '{key}' changed from {old_value} to {value}")
    
    def _persist_state_key(self, key: str, value: Any) -> None:
        """Persist a specific state key to settings."""
        try:
            settings_manager = self.app_context.settings_manager
            
            # Map state keys to settings methods
            if key == "current_tab" and hasattr(settings_manager, 'global_settings'):
                settings_manager.global_settings.set_current_tab(value)
            
            # Add more state persistence mappings as needed
            
        except Exception as e:
            logger.error(f"Failed to persist state key '{key}': {e}")
    
    def update_ui_state(self, ui_updates: Dict[str, Any]) -> None:
        """
        Update UI state with multiple values.
        
        Args:
            ui_updates: Dictionary of UI state updates
        """
        ui_state = self._state_data.get("ui_state", {})
        ui_state.update(ui_updates)
        self.set_state("ui_state", ui_state)
    
    def get_ui_state(self, key: str = None) -> Any:
        """
        Get UI state data.
        
        Args:
            key: Specific UI state key. If None, returns all UI state.
            
        Returns:
            The requested UI state data
        """
        ui_state = self._state_data.get("ui_state", {})
        
        if key is None:
            return ui_state.copy()
        
        return ui_state.get(key)
    
    def save_session_data(self, session_data: Dict[str, Any]) -> None:
        """
        Save session-specific data.
        
        Args:
            session_data: Data to save for the current session
        """
        self.set_state("session_data", session_data, persist=False)
    
    def get_session_data(self) -> Dict[str, Any]:
        """Get session-specific data."""
        return self._state_data.get("session_data", {}).copy()
    
    def cleanup(self) -> None:
        """Cleanup state manager resources."""
        # Save final state
        try:
            self._persist_all_state()
        except Exception as e:
            logger.error(f"Failed to save final state: {e}")
        
        # Clear state
        self._state_data.clear()
        self._current_tab = None
        
        logger.info("State manager cleaned up")
    
    def _persist_all_state(self) -> None:
        """Persist all state data to settings."""
        # This would save all persistent state to the settings manager
        # Implementation depends on the specific settings structure
        pass
