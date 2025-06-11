"""
Modern, professional logging configuration for the Kinetic Constructor application.

Features:
- Color-coded console output based on log level
- Structured JSON file logging for machine readability
- Module-specific loggers with appropriate log levels
- Configurable verbosity through environment variables
- Automatic log rotation and cleanup
"""

import logging
import os
import sys


# Define log levels with color codes for console output
class LogColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


# Define module-specific log levels
class ModuleLogLevels:
    # Default level for all modules
    DEFAULT = logging.INFO

    # Module-specific overrides
    SETTINGS = logging.INFO  # Settings-related logs
    UI = logging.WARNING  # UI-related logs (reduce verbosity)
    SEQUENCE = logging.INFO  # Sequence-related operations
    EXPORT = logging.INFO  # Export operations
    PICTOGRAPH = logging.WARNING  # Pictograph-related operations
    QT = logging.WARNING  # Qt-related messages


# Environment variable to control log level
ENV_LOG_LEVEL = "KINETIC_LOG_LEVEL"


class ColorizedFormatter(logging.Formatter):
    """Custom formatter that adds colors to console output based on log level."""

    LEVEL_COLORS = {
        logging.DEBUG: f"{LogColor.BRIGHT_BLACK}",
        logging.INFO: f"{LogColor.BRIGHT_WHITE}",
        logging.WARNING: f"{LogColor.BRIGHT_YELLOW}",
        logging.ERROR: f"{LogColor.BRIGHT_RED}",
        logging.CRITICAL: f"{LogColor.BG_RED}{LogColor.WHITE}{LogColor.BOLD}",
    }

    LEVEL_NAMES = {
        logging.DEBUG: "DEBUG",
        logging.INFO: "INFO ",
        logging.WARNING: "WARN ",
        logging.ERROR: "ERROR",
        logging.CRITICAL: "CRIT ",
    }

    def __init__(self, fmt=None, datefmt=None, style="%"):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        # Save original values
        orig_levelname = record.levelname
        orig_msg = record.msg

        # Apply color to level name
        color = self.LEVEL_COLORS.get(record.levelno, LogColor.RESET)
        level_name = self.LEVEL_NAMES.get(record.levelno, record.levelname)

        # Format the module name to be more concise
        module_parts = record.name.split(".")
        if len(module_parts) > 2:
            # For deeply nested modules, show only first and last parts
            module_name = f"{module_parts[0]}...{module_parts[-1]}"
        else:
            module_name = record.name

        # Truncate module name if too long
        if len(module_name) > 20:
            module_name = module_name[:17] + "..."

        # Pad module name for alignment
        module_name = module_name.ljust(20)

        # Create the colored prefix
        colored_prefix = f"{color}{level_name}{LogColor.RESET} [{module_name}]"

        # Set the message with the colored prefix
        record.msg = f"{colored_prefix} {record.msg}"

        # Format the record
        result = super().format(record)

        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg

        return result


# JsonFormatter removed since we're not using JSON logging anymore


def get_log_level_from_env() -> int:
    """Get log level from environment variable or use default."""
    level_name = os.environ.get(ENV_LOG_LEVEL, "INFO").upper()
    return getattr(logging, level_name, logging.INFO)


def configure_logging(default_level: int = None) -> logging.Logger:
    """
    Configure the logging system for the application.

    Args:
        default_level: The minimum logging level to display (default: from environment or INFO)

    Returns:
        The configured root logger
    """
    # Determine log level from environment or parameter
    log_level = default_level if default_level is not None else get_log_level_from_env()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler for logging to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(max(log_level, logging.INFO))  # At least INFO for console

    # Use colorized formatter for console
    console_formatter = ColorizedFormatter()
    console_handler.setFormatter(console_formatter)

    # Add the handler to the root logger
    root_logger.addHandler(console_handler)

    # Create a filter to reduce noise from certain modules
    class ModuleFilter(logging.Filter):
        def filter(self, record):
            # Filter out verbose debug messages from PyQt and other libraries
            if record.levelno <= logging.DEBUG:
                if record.name.startswith("PyQt6") or record.name.startswith("PIL"):
                    return False
            return True

    # Apply the module filter to the console handler
    module_filter = ModuleFilter()
    console_handler.addFilter(module_filter)

    # Apply the application-wide filter to the console handler
    try:
        from utils.app_log_filter import AppLogFilter

        app_filter = AppLogFilter()
        console_handler.addFilter(app_filter)
    except ImportError:
        # The filter module might not be available during initial setup
        pass

    # Configure module-specific loggers
    configure_module_loggers()

    return root_logger


def configure_module_loggers():
    """Configure module-specific loggers with appropriate log levels."""
    # Configure settings module with very aggressive filtering
    settings_logger = logging.getLogger("settings_manager")
    settings_logger.setLevel(ModuleLogLevels.SETTINGS)

    # Add settings filter to aggressively reduce noise from settings
    try:
        from settings_manager.settings_filter import SettingsFilter

        settings_filter = SettingsFilter()
        # Apply to both the logger and the console handler
        settings_logger.addFilter(settings_filter)
    except ImportError:
        # The filter module might not be available during initial setup
        pass

    # Configure UI modules with higher threshold to reduce noise
    ui_logger = logging.getLogger("main_window.main_widget")
    ui_logger.setLevel(logging.WARNING)  # Only show warnings and above for UI

    # Configure sequence modules
    sequence_logger = logging.getLogger("main_window.main_widget.sequence_workbench")
    sequence_logger.setLevel(
        logging.WARNING
    )  # Only show warnings and above for sequences

    # Configure sequence card tab with higher threshold
    card_logger = logging.getLogger("main_window.main_widget.sequence_card_tab")
    card_logger.setLevel(logging.WARNING)  # Only show warnings and above

    # Configure export modules
    export_logger = logging.getLogger(
        "main_window.main_widget.sequence_workbench.sequence_beat_frame.image_export_manager"
    )
    export_logger.setLevel(logging.WARNING)  # Only show warnings and above for exports

    # Configure pictograph modules
    pictograph_logger = logging.getLogger("base_widgets.pictograph")
    pictograph_logger.setLevel(
        logging.WARNING
    )  # Only show warnings and above for pictographs

    # Configure browse tab with higher threshold
    browse_logger = logging.getLogger("main_window.main_widget.browse_tab")
    browse_logger.setLevel(logging.WARNING)  # Only show warnings and above


# No longer needed since we're not creating log files


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    This is a convenience function to get a logger with the correct module name.

    Args:
        name: The name of the logger, typically __name__

    Returns:
        A configured logger instance
    """
    return logging.getLogger(name)


# Add a method to log with additional structured data
def log_with_data(logger, level, msg, data=None, **kwargs):
    """
    Log a message with additional structured data.

    Args:
        logger: The logger instance
        level: The log level (e.g., logging.INFO)
        msg: The log message
        data: Additional data to include in the log (dict)
        **kwargs: Additional keyword arguments for the logger
    """
    if data is not None:
        extra = kwargs.get("extra", {})
        extra["data"] = data
        kwargs["extra"] = extra

    logger.log(level, msg, **kwargs)


# Monkey patch the Logger class to add the log_with_data method
logging.Logger.log_with_data = (
    lambda self, level, msg, data=None, **kwargs: log_with_data(
        self, level, msg, data, **kwargs
    )
)
