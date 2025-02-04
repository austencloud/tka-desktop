import sys
import logging
import traceback
from PyQt6.QtCore import qInstallMessageHandler, QtMsgType


class QtDebugMessageHandler:
    """
    Intercepts Qt debug/warning/error messages and optionally raises
    exceptions or prints stack traces for specific warnings.
    """

    def __init__(self):
        """
        Optionally store patterns or flags here if you want to dynamically toggle
        which warnings raise exceptions.
        """
        # E.g. we can store the strings we want to treat as errors:
        self.error_patterns = [
            "QFont::setPointSize: Point size <= 0 (0)",
            "QPainter::begin: A paint device can only be painted by",
        ]

    def install(self):
        """Call this once at startup to install the custom handler."""
        qInstallMessageHandler(self._handle_message)

    def _handle_message(self, msg_type, context, message):
        """
        This method is called whenever Qt logs a debug/warning/error message.
        Raise an exception or show a traceback if the message matches our patterns.
        """
        # Check if any known error pattern is in the message
        # for pattern in self.error_patterns:
        #     if pattern in message:
                # Option A: Print stack trace, then raise an error
                # print("==== Intercepted Qt Warning ====")
                # print(f"Message: {message}")
                # print("Stack trace:\n", "".join(traceback.format_stack()))
                # raise RuntimeError(f"Qt Warning: {message}")

                # If you prefer not to crash your app:
                # print("Stack trace:\n", "".join(traceback.format_stack()))
                # break  # or return instead of raising

        # If no patterns match, let other messages pass without interruption
        pass
