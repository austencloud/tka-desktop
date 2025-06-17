import os
from typing import Dict, Any, Optional, List
import logging


class CacheManager:
    def __init__(self, cache_path: str):
        self.cache_path = cache_path
        self.logger = logging.getLogger(__name__)
        os.makedirs(cache_path, exist_ok=True)

    def get_cache_file_path(self, filename: str) -> str:
        return os.path.join(self.cache_path, filename)

    def cache_exists(self, filename: str) -> bool:
        return os.path.exists(self.get_cache_file_path(filename))

    def clear_cache(self) -> None:
        for filename in os.listdir(self.cache_path):
            file_path = os.path.join(self.cache_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                self.logger.error(f"Error deleting cache file {filename}: {e}")


class AssetManager:
    def __init__(self, assets_path: str):
        self.assets_path = assets_path

    def get_asset_path(self, filename: str) -> str:
        return os.path.join(self.assets_path, filename)

    def asset_exists(self, filename: str) -> bool:
        return os.path.exists(self.get_asset_path(filename))

    def list_assets(self, extension: Optional[str] = None) -> List[str]:
        assets = []
        for filename in os.listdir(self.assets_path):
            if extension is None or filename.endswith(extension):
                assets.append(filename)
        return assets
