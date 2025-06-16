from typing import TYPE_CHECKING, Union
from enums.letter.letter_type import LetterType

from enums.letter.letter import LetterCondition

from .turns_tuple_generators.base_turns_tuple_generator import BaseTurnsTupleGenerator
from .turns_tuple_generators.color_turns_tuple_generator import ColorTurnsTupleGenerator
from .turns_tuple_generators.lambda_turns_tuple_generator import (
    LambdaTurnsTupleGenerator,
)
from .turns_tuple_generators.lead_state_turns_tuple_generator import (
    LeadStateTurnsTupleGenerator,
)
from .turns_tuple_generators.type1_hybrid_turns_tuple_generator import (
    Type1HybridTurnsTupleGenerator,
)
from .turns_tuple_generators.type2_turns_tuple_generator import Type2TurnsTupleGenerator
from .turns_tuple_generators.type3_turns_tuple_generator import Type3TurnsTupleGenerator
from .turns_tuple_generators.type4_turns_tuple_generator import Type4TurnsTupleGenerator
from .turns_tuple_generators.type56_turns_tuple_generator import (
    Type56TurnsTupleGenerator,
)
from .turns_tuple_generators.gamma_turns_tuple_generator import GammaTurnsTupleGenerator
from .turns_tuple_generators.lambda_dash_turns_tuple_generator import (
    LambdaDashTurnsTupleGenerator,
)

from .mirrored_turns_tuple_generator import MirroredTurnsTupleGenerator
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from legacy.src.base_widgets.pictograph.legacy_pictograph import LegacyPictograph


class TurnsTupleGenerator:
    """
    Manages the generation of turn tuples for different letter types in a pictograph.
    It delegates to specific generator classes based on letter type.

    Attributes:
        generators (dict): Maps generator keys to specialized generator instances for various letter types.
        mirrored_generator (MirroredTurnsTupleGenerator): Handles mirrored turn tuple generation.

    Methods:
        generate_turns_tuple(pictograph: "BasePictograph") -> str: Returns turn tuple for a pictograph based on its letter.
        generate_mirrored_tuple(arrow: "Arrow") -> Union[str, None]: Returns mirrored turn tuple for an arrow.

    The class ensures accurate and efficient generation of turn tuples, prioritizing special cases like S, T, Λ, Λ-, and Γ.
    """

    def __init__(self):
        self.generators: list[BaseTurnsTupleGenerator] = {
            "Type1Hybrid": Type1HybridTurnsTupleGenerator(),
            "Color": ColorTurnsTupleGenerator(),
            LetterType.Type2: Type2TurnsTupleGenerator(),
            LetterType.Type3: Type3TurnsTupleGenerator(),
            LetterType.Type4: Type4TurnsTupleGenerator(),
            LetterType.Type5: Type56TurnsTupleGenerator(),
            LetterType.Type6: Type56TurnsTupleGenerator(),
            "LeadState": LeadStateTurnsTupleGenerator(),
            "Lambda": LambdaTurnsTupleGenerator(),
            "LambdaDash": LambdaDashTurnsTupleGenerator(),
            "Gamma": GammaTurnsTupleGenerator(),
        }
        self.mirrored_generator = MirroredTurnsTupleGenerator(self)

    def generate_turns_tuple(self, pictograph: "LegacyPictograph") -> str:
        generator_key = self._get_generator_key(pictograph)
        if generator_key and generator_key in self.generators:
            generator = self.generators[generator_key]
            turns_tuple = generator.generate_turns_tuple(pictograph)
            if turns_tuple is None:
                raise ValueError(
                    f"Turns tuple is None for letter {pictograph.state.letter.value}."
                )
            return turns_tuple
        return ""

    def generate_mirrored_tuple(self, arrow: Arrow) -> Union[str, None]:
        mirrored_tuple = self.mirrored_generator.generate(arrow)
        return mirrored_tuple

    def _get_generator_key(
        self, pictograph: "LegacyPictograph"
    ) -> Union[str, LetterType]:
        letter = pictograph.state.letter
        if letter.value in [
            letter.value
            for letter in letter.get_letters_by_condition(LetterCondition.TYPE1_HYBRID)
        ]:
            return "Type1Hybrid"
        elif letter.value in [
            letter.value
            for letter in letter.get_letters_by_condition(
                LetterCondition.TYPE1_NON_HYBRID
            )
        ]:
            return "Color"
        special_cases = {
            "S": "LeadState",
            "T": "LeadState",
            "Λ": "Lambda",
            "Λ-": "LambdaDash",
            "Γ": "Gamma",
        }
        if letter.value in special_cases:
            return special_cases[letter.value]

        for letter_type in LetterType:
            if letter.value in letter_type.value[0]:
                return letter_type

        return None
