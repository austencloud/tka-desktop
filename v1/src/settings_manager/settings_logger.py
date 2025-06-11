"""
Logger for the settings manager module.

This module provides a specialized logger for settings-related operations,
with appropriate formatting and filtering.
"""

import logging
from utils.logging_config import get_logger

# Create a logger for the settings module
logger = get_logger("settings_manager")


def log_setting_get(setting_name: str, raw_value, parsed_value=None):
    """
    Log a setting retrieval operation.

    Args:
        setting_name: The name of the setting being retrieved
        raw_value: The raw value from the settings store
        parsed_value: The parsed/converted value (if applicable)
    """
    if logger.isEnabledFor(logging.DEBUG):
        if parsed_value is not None and parsed_value != raw_value:
            logger.debug(
                f"Get setting: {setting_name} = {parsed_value} (raw: {raw_value})"
            )
        else:
            logger.debug(f"Get setting: {setting_name} = {raw_value}")


def log_setting_set(setting_name: str, value):
    """
    Log a setting update operation.

    Args:
        setting_name: The name of the setting being updated
        value: The new value
    """
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"Set setting: {setting_name} = {value}")


def log_settings_load(source: str, success: bool, error=None):
    """
    Log a settings load operation.

    Args:
        source: The source of the settings (file path, etc.)
        success: Whether the operation was successful
        error: Error message if the operation failed
    """
    if success:
        logger.info(f"Settings loaded successfully from {source}")
    else:
        logger.error(f"Failed to load settings from {source}: {error}")


def log_settings_save(destination: str, success: bool, error=None):
    """
    Log a settings save operation.

    Args:
        destination: The destination of the settings (file path, etc.)
        success: Whether the operation was successful
        error: Error message if the operation failed
    """
    if success:
        logger.info(f"Settings saved successfully to {destination}")
    else:
        logger.error(f"Failed to save settings to {destination}: {error}")
