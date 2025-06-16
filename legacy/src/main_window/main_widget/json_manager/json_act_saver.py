# json_act_saver.py

import json
import os
from PyQt6.QtCore import QDir


class JsonActSaver:
    def __init__(self):
        self.current_act_json = os.path.join(QDir.currentPath(), "current_act.json")

    def save_act(self, act_data: dict):
        """Save the act data to the current_act.json file."""
        acts_dir = os.path.join(QDir.currentPath(), "acts")
        os.makedirs(acts_dir, exist_ok=True)

        with open(self.current_act_json, "w", encoding="utf-8") as f:
            json.dump(act_data, f, indent=4, ensure_ascii=False)
