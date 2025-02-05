
from .base_loc_calculator import BaseLocationCalculator

class StaticLocationCalculator(BaseLocationCalculator):
    def calculate_location(self) -> str:
        return self.arrow.motion.start_loc
