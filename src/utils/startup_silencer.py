"""
Utility to silence specific loggers during application startup.

This module provides functions to temporarily silence loggers during startup
to reduce console noise, and then restore them to their normal levels later.
"""

import logging
from typing import Dict, List


class StartupSilencer:
    """
    Utility class to silence specific loggers during application startup.

    This class provides methods to temporarily silence loggers during startup
    to reduce console noise, and then restore them to their normal levels later.
    """

    def __init__(self):
        # Store original log levels to restore later
        self.original_levels: Dict[str, int] = {}

        # Loggers to silence during startup
        self.startup_loggers: List[str] = [
            # Settings-related loggers
            "settings_manager",
            # UI-related loggers
            "main_window.main_widget",
            "main_window.main_widget.sequence_card_tab",
            "main_window.main_widget.browse_tab",
            # Sequence-related loggers
            "main_window.main_widget.sequence_workbench",
            # Root logger (for other messages)
            "",
        ]

    def silence_startup_loggers(self):
        """
        Temporarily silence loggers during startup.

        This method increases the log level of specified loggers to ERROR
        to reduce console noise during application startup.
        """
        for logger_name in self.startup_loggers:
            logger = logging.getLogger(logger_name)
            # Store original level
            self.original_levels[logger_name] = logger.level
            # Set to ERROR level (only show errors)
            logger.setLevel(logging.ERROR)

    def restore_logger_levels(self):
        """
        Restore loggers to their original levels.

        This method should be called after startup is complete to restore
        normal logging behavior.
        """
        for logger_name, level in self.original_levels.items():
            logger = logging.getLogger(logger_name)
            logger.setLevel(level)

    def __enter__(self):
        """Context manager entry point."""
        self.silence_startup_loggers()
        return self

    def __exit__(self, *_):
        """Context manager exit point."""
        self.restore_logger_levels()


# Convenience function to use as a context manager
def silence_startup_logs():
    """
    Context manager to silence logs during startup.

    Usage:
        with silence_startup_logs():
            # Startup code here
    """
    return StartupSilencer()
