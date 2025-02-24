import traceback
from PyQt6.QtCore import qInstallMessageHandler

class PaintEventSuppressor:
    @staticmethod
    def my_message_handler(msg_type, context, message):
        # Suppress all QPainter-related warnings
        if "QPainter" in message or "Painter" in message:
            return  # Ignore and move on

        # Print other messages if needed
        print(message)  # Or log them if necessary

    @staticmethod
    def install_message_handler():
        qInstallMessageHandler(PaintEventSuppressor.my_message_handler)
