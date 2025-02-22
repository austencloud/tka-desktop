from typing import TYPE_CHECKING, Union
from Enums.Enums import Letter
from Enums.PropTypes import PropType
from Enums.letters import LetterType




if TYPE_CHECKING:
    pass

from dataclasses import dataclass
from typing import Optional, Union


from dataclasses import dataclass, field

@dataclass
class PictographState:
    """Tracks various states of the pictograph."""
    
    pictograph_data: dict[str, Union[str, dict[str, str]]] = field(default_factory=dict)
    is_blank: bool = False
    disable_gold_overlay: bool = False
    blue_reversal: bool = False
    red_reversal: bool = False

    # Enums
    letter: Optional[Letter] = None
    letter_type: Optional[LetterType] = None
    prop_type: Optional[PropType] = None

    # Positional attributes
    open_close_state: str = ""
    vtg_mode: str = ""
    direction: str = ""
    start_pos: str = ""
    end_pos: str = ""
    timing: str = ""
    turns_tuple: str = ""
    grid_mode: str = ""
