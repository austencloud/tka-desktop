from typing import TYPE_CHECKING
from ..CAP_type import CAPType


class WordLengthCalculator:
    @staticmethod
    def calculate(
        CAP_type: CAPType, slice_size: str, length: int, sequence_length: int
    ):
        sequence_length -= 2
        if CAP_type == CAPType.STRICT_ROTATED:
            word_length = length // 4 if slice_size == "quartered" else length // 2
        else:
            word_length = length // 2
        available_range = word_length - sequence_length
        return word_length, available_range
