import json
import time
from pathlib import Path
from typing import Dict, Any, Optional


class LauncherCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_file = cache_dir / "launcher_cache.json"
        self.cache_data = self.load_cache()

    def load_cache(self) -> Dict[str, Any]:
        if self.cache_file.exists():
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {"app_stats": {}, "frequent_apps": [], "last_cleanup": 0}

    def save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache_data, f, indent=2)

    def record_app_launch(self, app_name: str, success: bool, launch_time: float):
        if "app_stats" not in self.cache_data:
            self.cache_data["app_stats"] = {}

        stats = self.cache_data["app_stats"].get(
            app_name, {"launches": 0, "successes": 0, "avg_time": 0, "last_used": 0}
        )

        stats["launches"] += 1
        if success:
            stats["successes"] += 1
        stats["avg_time"] = (stats["avg_time"] + launch_time) / 2
        stats["last_used"] = time.time()

        self.cache_data["app_stats"][app_name] = stats
        self.update_frequent_apps()
        self.save_cache()

    def get_frequent_apps(self, limit: int = 5) -> list:
        return self.cache_data.get("frequent_apps", [])[:limit]

    def update_frequent_apps(self):
        apps = self.cache_data.get("app_stats", {})
        frequent = sorted(
            apps.items(),
            key=lambda x: (x[1]["successes"], x[1]["last_used"]),
            reverse=True,
        )
        self.cache_data["frequent_apps"] = [app[0] for app in frequent[:10]]

    def get_app_stats(self, app_name: str) -> Dict[str, Any]:
        return self.cache_data.get("app_stats", {}).get(app_name, {})

    def clear_cache(self):
        self.cache_data = {
            "app_stats": {},
            "frequent_apps": [],
            "last_cleanup": time.time(),
        }
        self.save_cache()
