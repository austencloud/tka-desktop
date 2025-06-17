import os
from pathlib import Path
from typing import Optional
import pandas as pd


class DataPathHandler:
    """Centralized handler for data file paths and loading operations."""

    _instance: Optional["DataPathHandler"] = None
    _data_dir: Optional[Path] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data_dir = cls._instance._resolve_data_directory()
        return cls._instance

    def __init__(self):
        pass

    def _resolve_data_directory(self) -> Path:
        """Resolve the root data directory path."""
        current_file = Path(__file__)
        return current_file.parent.parent.parent.parent / "data"

    @property
    def data_dir(self) -> Path:
        """Get the data directory path."""
        if self._data_dir is None:
            self._data_dir = self._resolve_data_directory()
        return self._data_dir

    @property
    def diamond_csv_path(self) -> Path:
        """Get the diamond pictograph CSV file path."""
        return self.data_dir / "DiamondPictographDataframe.csv"

    @property
    def box_csv_path(self) -> Path:
        """Get the box pictograph CSV file path."""
        return self.data_dir / "BoxPictographDataframe.csv"

    def load_diamond_dataset(self) -> Optional[pd.DataFrame]:
        """Load diamond pictograph dataset."""
        if self.diamond_csv_path.exists():
            return pd.read_csv(self.diamond_csv_path)
        return None

    def load_box_dataset(self) -> Optional[pd.DataFrame]:
        """Load box pictograph dataset."""
        if self.box_csv_path.exists():
            return pd.read_csv(self.box_csv_path)
        return None

    def load_combined_dataset(self) -> pd.DataFrame:
        """Load and combine both diamond and box datasets."""
        diamond_df = self.load_diamond_dataset()
        box_df = self.load_box_dataset()

        datasets = [df for df in [diamond_df, box_df] if df is not None]

        if datasets:
            return pd.concat(datasets, ignore_index=True)
        return pd.DataFrame()

    def validate_data_files(self) -> dict:
        """Check if data files exist and return status."""
        return {
            "diamond_exists": self.diamond_csv_path.exists(),
            "box_exists": self.box_csv_path.exists(),
            "diamond_path": str(self.diamond_csv_path),
            "box_path": str(self.box_csv_path),
            "data_dir": str(self.data_dir),
        }
