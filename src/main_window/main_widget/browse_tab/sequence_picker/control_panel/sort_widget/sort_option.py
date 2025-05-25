from typing import Callable, TYPE_CHECKING
from dataclasses import dataclass


@dataclass
class SortOption:
    """Represents a sorting option with an identifier, label, and action callback."""

    identifier: str
    label: str
    on_click: Callable[[], None]
