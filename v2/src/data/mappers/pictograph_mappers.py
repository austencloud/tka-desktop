from typing import Dict, Any, List, Union, Hashable
import pandas as pd
import os


class PictographDataMapper:
    def __init__(self, assets_path: str):
        self.assets_path = assets_path

    def map_csv_to_pictograph_data(
        self, csv_filename: str
    ) -> List[Dict[Union[str, Hashable], Any]]:
        filepath = os.path.join(self.assets_path, csv_filename)
        try:
            df = pd.read_csv(filepath)
            return df.to_dict("records")
        except FileNotFoundError:
            return []

    def get_box_pictograph_data(self) -> List[Dict[Union[str, Hashable], Any]]:
        return self.map_csv_to_pictograph_data("BoxPictographDataframe.csv")

    def get_diamond_pictograph_data(self) -> List[Dict[Union[str, Hashable], Any]]:
        return self.map_csv_to_pictograph_data("DiamondPictographDataframe.csv")


class CircleCoordinateMapper:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def load_circle_coordinates(self) -> Dict[str, Any]:
        import json

        filepath = os.path.join(self.config_path, "circle_coords.json")
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def map_coordinates_to_positions(
        self, coordinates: Dict[str, Any]
    ) -> Dict[str, tuple]:
        return {
            key: (coord.get("x", 0), coord.get("y", 0))
            for key, coord in coordinates.items()
        }
