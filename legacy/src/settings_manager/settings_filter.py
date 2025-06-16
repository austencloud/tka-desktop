"""
Aggressive filter for settings-related logs.

This module provides a filter to drastically reduce the verbosity of settings-related logs,
suppressing almost all settings logs during normal operation.
"""

import logging
import re
from typing import Set, Pattern, List


class SettingsFilter(logging.Filter):
    """
    Aggressive filter for settings-related logs.

    This filter suppresses almost all settings logs during normal operation,
    only allowing critical settings changes to be logged.
    """

    def __init__(self, name: str = ""):
        super().__init__(name)

        # By default, filter ALL settings logs except those explicitly allowed
        self.filter_all_settings = True

        # Settings that are allowed to be logged (critical settings)
        self.allowed_settings: Set[str] = {
            # Add only critical settings here that should always be logged
            "global/prop_type",  # Prop type changes are important
            "global/grid_mode",  # Grid mode changes are important
        }

        # Patterns for messages that should always be filtered
        self.always_filter_patterns: List[Pattern] = [
            re.compile(r"Get setting:"),
            re.compile(r"Value is .+, returning:"),
            re.compile(r"Initial turns value:"),
            re.compile(r"Connected checkbox"),
            re.compile(r"Adding checkbox to layout"),
            re.compile(r"Loading directory preference"),
            re.compile(r"Saving directory preference"),
            re.compile(r"After setting, raw value is:"),
            re.compile(r"After saving, preference is:"),
        ]

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter settings logs based on configured rules.

        Args:
            record: The log record to filter

        Returns:
            True if the record should be logged, False otherwise
        """
        # Only filter settings-related logs and certain other patterns
        message = record.getMessage()

        # Filter out common settings-related messages
        for pattern in self.always_filter_patterns:
            if pattern.search(message):
                return False

        # Handle settings manager logs
        if record.name.startswith("settings_manager"):
            # If we're filtering all settings by default
            if self.filter_all_settings:
                # Check if this is a setting we want to allow
                for allowed_setting in self.allowed_settings:
                    if allowed_setting in message:
                        return True
                # Filter out all other settings logs
                return False

        return True
