from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from data.constants import *
from main_window.main_widget.grid_mode_checker import GridModeChecker
from objects.motion.managers.handpath_calculator import (
    HandpathCalculator,
)

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class BaseRotAngleCalculator(ABC):
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow
        self.rot_angle_key_generator = (
            self.arrow.pictograph.wasd_manager.rotation_angle_override_manager.key_generator
        )
        self.data_updater = (
            self.arrow.pictograph.arrow_placement_manager.special_positioner.data_updater
        )
        self.handpath_calculator = HandpathCalculator()

    def apply_rotation(self) -> None:
        angle = self.calculate_angle()
        self.arrow.setTransformOriginPoint(self.arrow.boundingRect().center())
        self.arrow.setRotation(angle)

    @abstractmethod
    def calculate_angle(self) -> int:
        pass

    def has_rotation_angle_override(self) -> bool:
        if self.arrow.motion.motion_type not in [DASH, STATIC]:
            return False

        special_placements = (
            self.arrow.pictograph.main_widget.special_placement_loader.special_placements
        )
        ori_key = self.data_updater._generate_ori_key(self.arrow.motion)
        letter = self.arrow.pictograph.letter.value

        letter_data: dict[str, dict] = (
            special_placements.get(
                GridModeChecker.get_grid_mode(
                    self.arrow.pictograph.pictograph_data
                )
            )
            .get(ori_key, {})
            .get(letter, {})
        )

        rot_angle_override_key = (
            self.rot_angle_key_generator.generate_rotation_angle_override_key(
                self.arrow
            )
        )

        return bool(
            letter_data.get(self.arrow.pictograph.turns_tuple, {}).get(
                rot_angle_override_key
            )
        )
