"""
Logger for UI-related operations.

This module provides specialized loggers for UI components,
with appropriate formatting and filtering.
"""
import logging
from utils.logging_config import get_logger

# Create loggers for different UI components
main_logger = get_logger('main_window')
widget_logger = get_logger('main_window.main_widget')
sequence_logger = get_logger('main_window.main_widget.sequence_workbench')
export_logger = get_logger('main_window.main_widget.sequence_workbench.sequence_beat_frame.image_export_manager')

def log_ui_event(component: str, event_type: str, details: str = None):
    """
    Log a UI event.
    
    Args:
        component: The UI component that triggered the event
        event_type: The type of event (click, resize, etc.)
        details: Additional details about the event
    """
    if widget_logger.isEnabledFor(logging.DEBUG):
        msg = f"UI Event: {component} - {event_type}"
        if details:
            msg += f" - {details}"
        widget_logger.debug(msg)

def log_sequence_operation(operation: str, sequence_name: str = None, details: str = None):
    """
    Log a sequence-related operation.
    
    Args:
        operation: The operation being performed (load, save, etc.)
        sequence_name: The name of the sequence (if applicable)
        details: Additional details about the operation
    """
    msg = f"Sequence {operation}"
    if sequence_name:
        msg += f": {sequence_name}"
    if details:
        msg += f" - {details}"
    
    sequence_logger.info(msg)

def log_export_operation(operation: str, target: str = None, details: str = None):
    """
    Log an export operation.
    
    Args:
        operation: The export operation being performed
        target: The export target (file, directory, etc.)
        details: Additional details about the operation
    """
    msg = f"Export {operation}"
    if target:
        msg += f" to {target}"
    if details:
        msg += f" - {details}"
    
    export_logger.info(msg)

def log_startup(component: str, status: str = "started"):
    """
    Log a component startup event.
    
    Args:
        component: The component that is starting up
        status: The status of the startup (started, completed, failed)
    """
    main_logger.info(f"{component} {status}")

def log_performance(operation: str, duration_ms: float):
    """
    Log a performance metric.
    
    Args:
        operation: The operation being measured
        duration_ms: The duration in milliseconds
    """
    if duration_ms > 100:  # Only log slow operations
        widget_logger.warning(f"Performance: {operation} took {duration_ms:.2f}ms")
    else:
        widget_logger.debug(f"Performance: {operation} took {duration_ms:.2f}ms")
