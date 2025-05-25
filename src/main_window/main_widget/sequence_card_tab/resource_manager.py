# src/main_window/main_widget/sequence_card_tab/tab.py
import os
import gc
import psutil
from PyQt6.QtCore import QTimer

from utils.path_helpers import (
    get_sequence_card_image_exporter_path,
)


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.sequence_card_tab.tab import SequenceCardTab


class SequenceCardResourceManager:
    def __init__(self, parent: "SequenceCardTab"):
        self.parent = parent
        self.last_dictionary_mod_time = self.get_dictionary_mod_time()
        self._setup_timers()

    def _setup_timers(self):
        self.memory_check_timer = QTimer(self.parent)
        self.memory_check_timer.timeout.connect(self._check_memory_usage)
        self.memory_check_timer.start(30000)

        self.dictionary_check_timer = QTimer(self.parent)
        self.dictionary_check_timer.timeout.connect(self.check_dictionary_changes)
        self.dictionary_check_timer.start(10000)

        self.resize_timer = QTimer(self.parent)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.parent.refresh_layout_after_resize)

    def get_dictionary_mod_time(self) -> float:
        images_path = get_sequence_card_image_exporter_path()
        latest_mod_time = 0

        if os.path.exists(images_path):
            for root, _, files in os.walk(images_path):
                for file in files:
                    if file.endswith(".png") and not file.startswith("__"):
                        file_path = os.path.join(root, file)
                        mod_time = os.path.getmtime(file_path)
                        if mod_time > latest_mod_time:
                            latest_mod_time = mod_time

        return latest_mod_time

    def check_dictionary_changes(self):
        current_mod_time = self.get_dictionary_mod_time()

        if current_mod_time > self.last_dictionary_mod_time:
            print("Sequence images changed. Reloading...")
            self.last_dictionary_mod_time = current_mod_time
            QTimer.singleShot(100, self.parent.load_sequences)

    def _check_memory_usage(self):
        try:
            process = psutil.Process()
            memory_mb = process.memory_info().rss / (1024 * 1024)

            if memory_mb > 800:
                gc.collect()

        except ImportError:
            pass
        except Exception:
            pass

    def cleanup(self):
        self.memory_check_timer.stop()
        self.dictionary_check_timer.stop()

        gc.collect()

    def has_sequence_images(self, images_path: str) -> bool:
        if not os.path.exists(images_path):
            return False

        for item in os.listdir(images_path):
            item_path = os.path.join(images_path, item)
            if os.path.isdir(item_path) and not item.startswith("__"):
                for file in os.listdir(item_path):
                    if file.endswith(".png") and not file.startswith("__"):
                        return True
        return False
