from typing import TYPE_CHECKING
from Enums.letters import LetterType
from data.constants import HEX_BLUE, HEX_RED
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from base_widgets.base_pictograph.glyphs.tka.tka_glyph import TKA_Glyph


class TurnsTupleInterpreter:
    def __init__(self, glyph: "TKA_Glyph"):
        self.glyph = glyph

    def interpret_turns_tuple(self, top_key: str, bottom_key: str) -> dict[str, str]:
        pictograph = self.glyph.pictograph
        generator_key = pictograph.main_widget.turns_tuple_generator._get_generator_key(
            pictograph
        )

        top_color = HEX_BLUE
        bot_color = HEX_RED

        def color_for_motion(m: Motion) -> str:
            return HEX_BLUE if m.color == "blue" else HEX_RED

        if generator_key == LetterType.Type2:
            shift_motion = pictograph.get.shift()
            static_motion = pictograph.get.static()
            top_color = color_for_motion(shift_motion)
            bot_color = color_for_motion(static_motion)

        elif generator_key == "Type1Hybrid":
            pro_motion = pictograph.get.pro()
            anti_motion = pictograph.get.anti()
            top_color = color_for_motion(pro_motion)
            bot_color = color_for_motion(anti_motion)

        elif generator_key == LetterType.Type3:
            shift_motion = pictograph.get.shift()
            dash_motion = pictograph.get.dash()
            top_color = color_for_motion(shift_motion)
            bot_color = color_for_motion(dash_motion)

        elif generator_key == LetterType.Type4 or generator_key == "Lambda":
            dash_motion = pictograph.get.dash()
            static_motion = pictograph.get.static()
            top_color = color_for_motion(dash_motion)
            bot_color = color_for_motion(static_motion)

        elif generator_key == "LeadState":
            leading_motion = pictograph.get.leading_motion()
            trailing_motion = pictograph.get.trailing_motion()
            if leading_motion and trailing_motion:
                top_color = color_for_motion(leading_motion)
                bot_color = color_for_motion(trailing_motion)

        return {top_key: top_color, bottom_key: bot_color}
