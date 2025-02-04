# act.py
import json


class Act:
    def __init__(self):
        self.events = []

    def to_json(self):
        return json.dumps(self.events, indent=2)

    @staticmethod
    def from_json(json_str):
        act = Act()
        act.events = json.loads(json_str)
        return act

    def save_to_file(self, file_path):
        with open(file_path, "w") as f:
            f.write(self.to_json())

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, "r") as f:
            json_str = f.read()
        return Act.from_json(json_str)
