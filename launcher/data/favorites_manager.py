from typing import List
import json
from pathlib import Path


class FavoritesManager:
    def __init__(self, favorites_file: str = "launcher_favorites.json"):
        self.favorites_file = Path(favorites_file)
        self._favorites = self.load_favorites()

    def load_favorites(self) -> List[str]:
        try:
            if self.favorites_file.exists():
                with open(self.favorites_file, "r") as f:
                    return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return []

    def save_favorites(self) -> None:
        with open(self.favorites_file, "w") as f:
            json.dump(self._favorites, f, indent=2)

    def add_favorite(self, item: str) -> None:
        if item not in self._favorites:
            self._favorites.append(item)
            self.save_favorites()

    def remove_favorite(self, item: str) -> None:
        if item in self._favorites:
            self._favorites.remove(item)
            self.save_favorites()

    def is_favorite(self, item: str) -> bool:
        return item in self._favorites

    def get_all(self) -> List[str]:
        return self._favorites.copy()

    def clear(self) -> None:
        self._favorites.clear()
        self.save_favorites()
