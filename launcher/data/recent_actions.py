from typing import List, Dict, Optional
from datetime import datetime
from PyQt6.QtWidgets import QListWidgetItem


class RecentAction:
    def __init__(self, name: str, timestamp: Optional[datetime] = None):
        self.name = name
        self.timestamp = timestamp or datetime.now()

    def __str__(self):
        return f"{self.name} - {self.timestamp.strftime('%H:%M:%S')}"


class RecentActionsManager:
    def __init__(self, max_items: int = 10):
        self.max_items = max_items
        self._actions: List[RecentAction] = []

    def add_action(self, action_name: str) -> None:
        existing_names = [action.name for action in self._actions]
        if action_name not in existing_names:
            new_action = RecentAction(action_name)
            self._actions.insert(0, new_action)

            if len(self._actions) > self.max_items:
                self._actions = self._actions[: self.max_items]

    def get_actions(self) -> List[RecentAction]:
        return self._actions.copy()

    def clear(self) -> None:
        self._actions.clear()

    def create_list_items(self) -> List[QListWidgetItem]:
        return [QListWidgetItem(str(action)) for action in self._actions]
