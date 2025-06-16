import logging
from PyQt6.QtCore import qInstallMessageHandler


class PaintEventSuppressor:
    @staticmethod
    def my_message_handler(_msg_type, _context, message):
        # Suppress common Qt warnings that are not actionable
        if any(
            pattern in message
            for pattern in [
                "QPainter",
                "Painter",
                "Unknown property cursor",
                "Unknown property box-shadow",
                "QWidget::setMinimumSize",
                "QFont::setPointSize",
                "Section 'sequence_picker' not found",
            ]
        ):
            return  # Ignore and move on

        # Log other messages at appropriate level
        if "warning" in message.lower():
            logging.warning(f"Qt Message: {message}")
        elif "error" in message.lower():
            logging.error(f"Qt Message: {message}")
        else:
            # Don't log debug messages to console
            qt_logger = logging.getLogger("qt_messages")
            qt_logger.debug(f"Qt Message: {message}")

    @staticmethod
    def install_message_handler():
        qInstallMessageHandler(PaintEventSuppressor.my_message_handler)
