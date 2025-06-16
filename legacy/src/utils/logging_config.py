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
        default_level: The minimum logging level to display (default: ERROR for minimal noise)

    Returns:
        The configured root logger
    """
    # Force ERROR level by default to minimize startup noise
    log_level = logging.ERROR if default_level is None else default_level

    # Override any environment settings that would increase verbosity
    if log_level < logging.ERROR:
        log_level = logging.ERROR

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler for logging to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    # Use colorized formatter for console
    console_formatter = ColorizedFormatter()
    console_handler.setFormatter(console_formatter)

    # Add the handler to the root logger
    root_logger.addHandler(console_handler)

    # Create an extremely aggressive filter to reduce all noise
    class AggressiveNoiseFilter(logging.Filter):
        def filter(self, record):
            # Block all DEBUG messages regardless of source
            if record.levelno <= logging.DEBUG:
                return False

            # Block all INFO messages during startup to reduce noise
            if record.levelno <= logging.INFO:
                return False

            # Filter out specific message patterns
            message = str(record.getMessage())

            # Block Qt/SVG property warnings
            if "unknown property" in message.lower() or "Unknown property" in message:
                return False

            # Block tab availability warnings during startup
            if "not available" in message.lower():
                return False

            # Block other common startup noise
            noise_patterns = [
                "registered",
                "initialized",
                "created successfully",
                "completed",
                "set up",
                "established",
                "getting essential widgets",
                "added",
                "stack now has",
                "create_tab called",
                "creating tab",
                "tab created",
                "adding tab",
            ]

            if any(pattern in message.lower() for pattern in noise_patterns):
                return False

            return True

    # Apply the aggressive filter
    aggressive_filter = AggressiveNoiseFilter()
    console_handler.addFilter(aggressive_filter)

    # Configure module-specific loggers to be even more restrictive
    configure_module_loggers()

    return root_logger


def configure_module_loggers():
    """Configure module-specific loggers with aggressive noise reduction."""
    # Set all major modules to ERROR level only
    module_patterns = [
        "main_window",
        "settings_manager",
        "src.core",
        "src.main_window",
        "base_widgets",
        "PyQt6",
        "matplotlib",
        "PIL",
    ]

    for pattern in module_patterns:
        logger = logging.getLogger(pattern)
        logger.setLevel(logging.ERROR)

    # Completely silence Qt warnings by capturing them at the system level
    import warnings

    warnings.filterwarnings("ignore", message=".*Unknown property.*")
    warnings.filterwarnings("ignore", message=".*transform.*")


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
