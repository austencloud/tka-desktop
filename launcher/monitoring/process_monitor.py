from PyQt6.QtCore import QThread, pyqtSignal
from typing import Optional, Dict, Any


class ProcessMonitor(QThread):
    status_update = pyqtSignal(str, dict)

    def __init__(self, process_manager_ref=None):
        super().__init__()
        self.running = True
        self.process_manager_ref = process_manager_ref

    def run(self):
        while self.running:
            active_count = 0
            if self.process_manager_ref:
                active_count = len(self.process_manager_ref.get_active_processes())

            status = {
                "cpu": "Normal",
                "memory": "Available",
                "active_processes": active_count,
            }
            self.status_update.emit("System Status", status)
            self.msleep(2000)

    def stop(self):
        self.running = False
