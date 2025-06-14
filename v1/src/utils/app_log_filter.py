"""
Application-wide log filter.

This module provides a filter to suppress common, non-essential logs
throughout the application, creating a cleaner console output.
"""
import logging
import re
from typing import List, Pattern, Set

class AppLogFilter(logging.Filter):
    """
    Application-wide log filter to suppress common, non-essential logs.
    
    This filter aggressively reduces log output by filtering out common
    patterns and messages that don't provide essential information.
    """
    
    def __init__(self, name: str = ""):
        super().__init__(name)
        
        # Patterns for messages that should always be filtered
        self.always_filter_patterns: List[Pattern] = [
            # UI-related patterns
            re.compile(r"Unknown property cursor"),
            re.compile(r"DEBUG: MenuBarNavWidget"),
            re.compile(r"Creating new sequence card page"),
            re.compile(r"Creating new row layout"),
            re.compile(r"Using existing row layout"),
            re.compile(r"Created page with size:"),
            
            # Sequence-related patterns
            re.compile(r"Loading sequences for length:"),
            re.compile(r"Loading sequences from dictionary:"),
            re.compile(r"Found \d+ total sequences in dictionary"),
            re.compile(r"Filtered to \d+ sequences with length"),
            re.compile(r"Displaying \d+ sequences"),
        ]
        
        # Module prefixes to filter at DEBUG level
        self.debug_filter_modules: Set[str] = {
            "main_window.main_widget.sequence_card_tab",
            "main_window.main_widget.browse_tab",
        }
        
        # Specific messages to allow even if they match patterns
        self.allowed_messages: Set[str] = {
            # Add specific messages that should be allowed despite matching patterns
        }
        
    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log records based on configured rules.
        
        Args:
            record: The log record to filter
            
        Returns:
            True if the record should be logged, False otherwise
        """
        # Always allow ERROR and higher logs
        if record.levelno >= logging.ERROR:
            return True
            
        # Get the message
        message = record.getMessage()
        
        # Check if this is a specific allowed message
        for allowed_message in self.allowed_messages:
            if allowed_message in message:
                return True
                
        # Filter out common patterns
        for pattern in self.always_filter_patterns:
            if pattern.search(message):
                return False
                
        # Filter DEBUG logs from certain modules
        if record.levelno == logging.DEBUG:
            for module_prefix in self.debug_filter_modules:
                if record.name.startswith(module_prefix):
                    return False
                    
        # Special case for sequence loading messages
        if "[INFO]" in message and "not found in the current filter" in message:
            return False
            
        if "[SUCCESS]" in message and "Loaded missing sequence" in message:
            return False
            
        # Allow all other logs
        return True
