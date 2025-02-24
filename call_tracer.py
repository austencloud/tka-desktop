import sys

import os
from types import FrameType
from typing import Any, Callable
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.json_manager.json_manager import JsonManager
from main_window.main_widget.json_manager.special_placement_saver import (
    SpecialPlacementSaver,
)
from main_window.main_widget.special_placement_loader import SpecialPlacementLoader
from main_window.settings_manager.global_settings.app_context import AppContext
from main_window.settings_manager.settings_manager import SettingsManager
from splash_screen.splash_screen import SplashScreen
from main_window.main_window import MainWindow
from profiler import Profiler

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILE_PATH = "trace_log.txt"
log_file = open(LOG_FILE_PATH, "w")
import traceback
from PyQt6.QtCore import qInstallMessageHandler


class CallTracer:
    def __init__(self, project_dir: str, log_file):
        self.project_dir = project_dir
        self.log_file = log_file

    def trace_calls(self, frame: FrameType, event: str, arg: Any) -> Callable | None:
        if event != "call":
            return

        code = frame.f_code
        filename = code.co_filename
        func_name = code.co_name

        # Only log functions from your project directory.
        if self.project_dir not in filename:
            return

        # Skip dunder methods.
        if func_name.startswith("__") and func_name.endswith("__"):
            return

        lineno = frame.f_lineno
        rel_path = os.path.relpath(filename, self.project_dir)

        # Log every paint event to find the one causing issues
        if func_name == "paintEvent":
            log_line = f"PAINT EVENT: {func_name}() at {rel_path}:{lineno}\n"
            self.log_file.write(log_line)
            self.log_file.flush()  # Flush immediately to track real-time calls

        return self.trace_calls
