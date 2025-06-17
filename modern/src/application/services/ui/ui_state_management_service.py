"""
UI State Management Service - Unified UI State Operations

Consolidates all UI state-related services into a single cohesive service:
- Core settings management (settings_service)
- Settings dialog coordination (settings_dialog_service)
- Tab-specific settings (tab_settings_services)
- Option picker state management (option_picker_state_service)
- Graph editor state (graph_editor_service)
- Graph editor hotkeys (graph_editor_hotkey_service)

This service provides a clean, unified interface for all UI state operations
while maintaining the proven algorithms from the individual services.
"""

from typing import Dict, Any, Optional, List, Callable
from enum import Enum
from dataclasses import dataclass, field
import json
from pathlib import Path

from core.events.event_bus import get_event_bus, UIEvent, EventPriority
from core.interfaces.core_services import IUIStateManagementService


class UIComponent(Enum):
    """UI component types."""

    MAIN_WINDOW = "main_window"
    SEQUENCE_EDITOR = "sequence_editor"
    GRAPH_EDITOR = "graph_editor"
    OPTION_PICKER = "option_picker"
    SETTINGS_DIALOG = "settings_dialog"
    BEAT_FRAME = "beat_frame"
    DICTIONARY_BROWSER = "dictionary_browser"


class TabType(Enum):
    """Tab types in the application."""

    SEQUENCE_BUILDER = "sequence_builder"
    DICTIONARY = "dictionary"
    LEARN = "learn"
    WRITE = "write"
    SETTINGS = "settings"


@dataclass
class UIState:
    """Complete UI state representation."""

    # Window state
    window_geometry: Dict[str, int] = field(default_factory=dict)
    window_maximized: bool = False

    # Component visibility
    component_visibility: Dict[str, bool] = field(default_factory=dict)

    # Tab states
    active_tab: str = "sequence_builder"
    tab_states: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Graph editor state
    graph_editor_visible: bool = False
    graph_editor_height: int = 300

    # Option picker state
    option_picker_selection: Optional[str] = None
    option_picker_filters: Dict[str, Any] = field(default_factory=dict)

    # Settings
    user_settings: Dict[str, Any] = field(default_factory=dict)


class UIStateManagementService(IUIStateManagementService):
    """
    Unified UI state management service consolidating all UI state operations.

    Provides comprehensive UI state management including:
    - Settings management (get, set, save, load)
    - Tab state coordination
    - Component visibility management
    - Graph editor state management
    - Option picker state management
    - Event-driven state synchronization
    """

    def __init__(self):
        # Core state
        self._ui_state = UIState()

        # Settings file path - use modern directory
        # Navigate from: src/application/services/ui/ -> modern/
        modern_dir = Path(__file__).parent.parent.parent.parent.parent
        self._settings_file = modern_dir / "user_settings.json"

        # Event bus for state synchronization
        self._event_bus = get_event_bus()

        # Default settings
        self._default_settings = self._load_default_settings()

        # Hotkey bindings
        self._hotkey_bindings: Dict[str, Callable] = {}

        # Load saved state
        self._load_state()

        # Subscribe to UI events
        self._setup_event_subscriptions()

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._ui_state.user_settings.get(
            key, self._default_settings.get(key, default)
        )

    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self._ui_state.user_settings[key] = value
        self._save_state()

        # Publish setting change event
        event = UIEvent(
            component="settings",
            action="updated",
            state_data={"key": key, "value": value},
            source="ui_state_management_service",
        )
        self._event_bus.publish(event)

    def get_tab_state(self, tab_name: str) -> Dict[str, Any]:
        """Get state for a specific tab."""
        return self._ui_state.tab_states.get(tab_name, {})

    def update_tab_state(self, tab_name: str, state: Dict[str, Any]) -> None:
        """Update state for a specific tab."""
        if tab_name not in self._ui_state.tab_states:
            self._ui_state.tab_states[tab_name] = {}

        self._ui_state.tab_states[tab_name].update(state)
        self._save_state()

        # Publish tab state change event
        event = UIEvent(
            component="tab",
            action="state_updated",
            state_data={"tab_name": tab_name, "state": state},
            source="ui_state_management_service",
        )
        self._event_bus.publish(event)

    def set_active_tab(self, tab_name: str) -> None:
        """Set the active tab."""
        previous_tab = self._ui_state.active_tab
        self._ui_state.active_tab = tab_name
        self._save_state()

        # Publish tab change event
        event = UIEvent(
            component="tab",
            action="changed",
            state_data={"previous_tab": previous_tab, "new_tab": tab_name},
            source="ui_state_management_service",
            priority=EventPriority.HIGH,
        )
        self._event_bus.publish(event)

    def get_active_tab(self) -> str:
        """Get the active tab."""
        return self._ui_state.active_tab

    def get_graph_editor_state(self) -> Dict[str, Any]:
        """Get graph editor state."""
        return {
            "visible": self._ui_state.graph_editor_visible,
            "height": self._ui_state.graph_editor_height,
        }

    def toggle_graph_editor(self) -> bool:
        """Toggle graph editor visibility."""
        self._ui_state.graph_editor_visible = not self._ui_state.graph_editor_visible
        self._save_state()

        # Publish graph editor toggle event
        event = UIEvent(
            component="graph_editor",
            action="toggled",
            state_data={"visible": self._ui_state.graph_editor_visible},
            source="ui_state_management_service",
            priority=EventPriority.HIGH,
        )
        self._event_bus.publish(event)

        return self._ui_state.graph_editor_visible

    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings."""
        return self._ui_state.user_settings.copy()

    def clear_settings(self) -> None:
        """Clear all settings."""
        self._ui_state.user_settings.clear()
        self._save_state()

    def save_state(self) -> None:
        """Save state to persistent storage."""
        self._save_state()

    def load_state(self) -> None:
        """Load state from persistent storage."""
        self._load_state()

    def set_graph_editor_height(self, height: int) -> None:
        """Set graph editor height."""
        self._ui_state.graph_editor_height = max(
            100, min(800, height)
        )  # Clamp between 100-800
        self._save_state()

        # Publish height change event
        event = UIEvent(
            component="graph_editor",
            action="height_changed",
            state_data={"height": self._ui_state.graph_editor_height},
            source="ui_state_management_service",
        )
        self._event_bus.publish(event)

    def get_option_picker_state(self) -> Dict[str, Any]:
        """Get option picker state."""
        return {
            "selection": self._ui_state.option_picker_selection,
            "filters": self._ui_state.option_picker_filters,
        }

    def set_option_picker_selection(self, selection: Optional[str]) -> None:
        """Set option picker selection."""
        self._ui_state.option_picker_selection = selection

        # Publish selection change event
        event = UIEvent(
            component="option_picker",
            action="selection_changed",
            state_data={"selection": selection},
            source="ui_state_management_service",
        )
        self._event_bus.publish(event)

    def update_option_picker_filters(self, filters: Dict[str, Any]) -> None:
        """Update option picker filters."""
        self._ui_state.option_picker_filters.update(filters)

        # Publish filter change event
        event = UIEvent(
            component="option_picker",
            action="filters_updated",
            state_data={"filters": filters},
            source="ui_state_management_service",
        )
        self._event_bus.publish(event)

    def set_component_visibility(self, component: str, visible: bool) -> None:
        """Set component visibility."""
        self._ui_state.component_visibility[component] = visible
        self._save_state()

        # Publish visibility change event
        event = UIEvent(
            component=component,
            action="visibility_changed",
            state_data={"visible": visible},
            source="ui_state_management_service",
        )
        self._event_bus.publish(event)

    def is_component_visible(self, component: str) -> bool:
        """Check if component is visible."""
        return self._ui_state.component_visibility.get(component, True)

    def register_hotkey(self, key_combination: str, callback: Callable) -> None:
        """Register a hotkey binding."""
        self._hotkey_bindings[key_combination] = callback

    def handle_hotkey(self, key_combination: str) -> bool:
        """Handle hotkey press."""
        if key_combination in self._hotkey_bindings:
            try:
                self._hotkey_bindings[key_combination]()
                return True
            except Exception as e:
                print(f"Error handling hotkey {key_combination}: {e}")
        return False

    def get_window_geometry(self) -> Dict[str, int]:
        """Get window geometry."""
        return self._ui_state.window_geometry.copy()

    def set_window_geometry(self, geometry: Dict[str, int]) -> None:
        """Set window geometry."""
        self._ui_state.window_geometry.update(geometry)
        self._save_state()

    def is_window_maximized(self) -> bool:
        """Check if window is maximized."""
        return self._ui_state.window_maximized

    def set_window_maximized(self, maximized: bool) -> None:
        """Set window maximized state."""
        self._ui_state.window_maximized = maximized
        self._save_state()

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self._ui_state = UIState()
        self._ui_state.user_settings = self._default_settings.copy()
        self._save_state()

        # Publish reset event
        event = UIEvent(
            component="settings",
            action="reset_to_defaults",
            state_data={},
            source="ui_state_management_service",
            priority=EventPriority.HIGH,
        )
        self._event_bus.publish(event)

    def export_settings(self, file_path: Path) -> bool:
        """Export settings to file."""
        try:
            with open(file_path, "w") as f:
                json.dump(self._ui_state.user_settings, f, indent=2)
            return True
        except Exception:
            return False

    def import_settings(self, file_path: Path) -> bool:
        """Import settings from file."""
        try:
            with open(file_path, "r") as f:
                imported_settings = json.load(f)

            self._ui_state.user_settings.update(imported_settings)
            self._save_state()

            # Publish import event
            event = UIEvent(
                component="settings",
                action="imported",
                state_data={"file_path": str(file_path)},
                source="ui_state_management_service",
            )
            self._event_bus.publish(event)

            return True
        except Exception:
            return False

    # Private methods

    def _load_state(self) -> None:
        """Load state from file."""
        if self._settings_file.exists():
            try:
                with open(self._settings_file, "r") as f:
                    data = json.load(f)

                # Update UI state from loaded data
                if "user_settings" in data:
                    self._ui_state.user_settings.update(data["user_settings"])
                if "window_geometry" in data:
                    self._ui_state.window_geometry.update(data["window_geometry"])
                if "window_maximized" in data:
                    self._ui_state.window_maximized = data["window_maximized"]
                if "active_tab" in data:
                    self._ui_state.active_tab = data["active_tab"]
                if "tab_states" in data:
                    self._ui_state.tab_states.update(data["tab_states"])
                if "graph_editor_visible" in data:
                    self._ui_state.graph_editor_visible = data["graph_editor_visible"]
                if "graph_editor_height" in data:
                    self._ui_state.graph_editor_height = data["graph_editor_height"]
                if "component_visibility" in data:
                    self._ui_state.component_visibility.update(
                        data["component_visibility"]
                    )

            except Exception as e:
                print(f"Error loading UI state: {e}")

    def _save_state(self) -> None:
        """Save state to file."""
        try:
            data = {
                "user_settings": self._ui_state.user_settings,
                "window_geometry": self._ui_state.window_geometry,
                "window_maximized": self._ui_state.window_maximized,
                "active_tab": self._ui_state.active_tab,
                "tab_states": self._ui_state.tab_states,
                "graph_editor_visible": self._ui_state.graph_editor_visible,
                "graph_editor_height": self._ui_state.graph_editor_height,
                "component_visibility": self._ui_state.component_visibility,
            }

            with open(self._settings_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving UI state: {e}")

    def _load_default_settings(self) -> Dict[str, Any]:
        """Load default settings."""
        return {
            "theme": "dark",
            "background_type": "Aurora",  # Default background
            "auto_save": True,
            "auto_save_interval": 300,  # 5 minutes
            "show_grid": True,
            "show_beat_numbers": True,
            "animation_speed": 1.0,
            "sound_enabled": True,
            "sound_volume": 0.7,
            "recent_files_count": 10,
            "default_sequence_length": 16,
            "graph_editor_auto_open": False,
        }

    def _setup_event_subscriptions(self) -> None:
        """Setup event subscriptions for state synchronization."""
        # Subscribe to relevant UI events to maintain state consistency
        self._event_bus.subscribe(
            "ui.window.geometry_changed",
            self._handle_window_geometry_changed,
            priority=EventPriority.NORMAL,
        )

        self._event_bus.subscribe(
            "ui.tab.switched", self._handle_tab_switched, priority=EventPriority.NORMAL
        )

    def _handle_window_geometry_changed(self, event: UIEvent) -> None:
        """Handle window geometry change event."""
        if "geometry" in event.state_data:
            self.set_window_geometry(event.state_data["geometry"])

    def _handle_tab_switched(self, event: UIEvent) -> None:
        """Handle tab switch event."""
        if "tab_name" in event.state_data:
            self.set_active_tab(event.state_data["tab_name"])
