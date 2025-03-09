import logging
from typing import TYPE_CHECKING



from placement_managers.arrow_placement_manager.arrow_placement_context import ArrowPlacementContext


from data.constants import (
    BLUE,
    CLOCK,
    COUNTER,
    IN,
    OUT,
    RED,
)
from objects.motion.motion import Motion

if TYPE_CHECKING:

    from base_widgets.pictograph.managers.getter.pictograph_getter import PictographGetter

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class OriKeyGenerator:
    def __init__(self, getter: "PictographGetter"):
        self.getter = getter

    def generate_ori_key_from_context(self, context: ArrowPlacementContext) -> str:
        """
        Generates an orientation key based on arrow placement context.

        :param context: ArrowPlacementContext object containing motion details.
        :return: Orientation key string.
        """
        # Instead of `motion`, use `context` directly.
        start_ori = context.start_ori
        color = context.arrow_color

        # Determine the other motion (assuming getter logic still applies)
        other_motion = self.getter.other_motion(
            self.getter.motion_by_color(context.arrow_color)
        )
        other_start_ori = other_motion.state.start_ori if other_motion else None

        if start_ori in [IN, OUT] and other_start_ori in [IN, OUT]:
            return "from_layer1"
        elif start_ori in [CLOCK, COUNTER] and other_start_ori in [CLOCK, COUNTER]:
            return "from_layer2"
        elif (
            color == RED
            and start_ori in [IN, OUT]
            and other_start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue2_red1"
        elif (
            color == RED
            and start_ori in [CLOCK, COUNTER]
            and other_start_ori in [IN, OUT]
        ):
            return "from_layer3_blue1_red2"
        elif (
            color == BLUE
            and start_ori in [IN, OUT]
            and other_start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue1_red2"
        elif (
            color == BLUE
            and start_ori in [CLOCK, COUNTER]
            and other_start_ori in [IN, OUT]
        ):
            return "from_layer3_blue2_red1"

    def generate_ori_key_from_motion(self, motion: Motion) -> str:
        other_motion: Motion = self.getter.other_motion(motion)
        if motion.state.start_ori in [IN, OUT] and other_motion.state.start_ori in [
            IN,
            OUT,
        ]:
            return "from_layer1"
        elif motion.state.start_ori in [
            CLOCK,
            COUNTER,
        ] and other_motion.state.start_ori in [
            CLOCK,
            COUNTER,
        ]:
            return "from_layer2"
        elif (
            motion.state.color == RED
            and motion.state.start_ori in [IN, OUT]
            and other_motion.state.start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue2_red1"
        elif (
            motion.state.color == RED
            and motion.state.start_ori in [CLOCK, COUNTER]
            and other_motion.state.start_ori in [IN, OUT]
        ):
            return "from_layer3_blue1_red2"
        elif (
            motion.state.color == BLUE
            and motion.state.start_ori in [IN, OUT]
            and other_motion.state.start_ori in [CLOCK, COUNTER]
        ):
            return "from_layer3_blue1_red2"
        elif (
            motion.state.color == BLUE
            and motion.state.start_ori in [CLOCK, COUNTER]
            and other_motion.state.start_ori in [IN, OUT]
        ):
            return "from_layer3_blue2_red1"

    def get_other_layer3_ori_key(self, ori_key: str) -> str:
        if ori_key == "from_layer3_blue1_red2":
            return "from_layer3_blue2_red1"
        elif ori_key == "from_layer3_blue2_red1":
            return "from_layer3_blue1_red2"
