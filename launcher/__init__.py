from .core.application import LauncherApplication
from .core.config import Config, Paths
from .core.process_manager import ProcessManager
from .data.app_definitions import AppDefinition, AppDefinitions
from .data.favorites_manager import FavoritesManager
from .data.recent_actions import RecentActionsManager
from .monitoring.process_monitor import ProcessMonitor
from .ui.main_window import LauncherWindow

__version__ = "2.0.0"
__all__ = [
    "LauncherApplication",
    "Config",
    "Paths",
    "ProcessManager",
    "AppDefinition",
    "AppDefinitions",
    "FavoritesManager",
    "RecentActionsManager",
    "ProcessMonitor",
    "LauncherWindow",
]
