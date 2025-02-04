from typing import TYPE_CHECKING
from data.constants import *
from Enums.PropTypes import PropType

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


from objects.prop.prop import Prop


class Hand(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Hand
        super().__init__(pictograph, attributes, motion)


class Staff(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Staff
        super().__init__(pictograph, attributes, motion)


class BigStaff(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Bigstaff
        super().__init__(pictograph, attributes, motion)


class Triad(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Triad
        super().__init__(pictograph, attributes, motion)


class MiniHoop(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Minihoop
        super().__init__(pictograph, attributes, motion)


class Fan(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Fan
        super().__init__(pictograph, attributes, motion)


class Club(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Club
        super().__init__(pictograph, attributes, motion)


class Buugeng(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Buugeng
        super().__init__(pictograph, attributes, motion)


class BigBuugeng(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Bigbuugeng
        super().__init__(pictograph, attributes, motion)


class Fractalgeng(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Fractalgeng
        super().__init__(pictograph, attributes, motion)


class EightRings(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Eightrings
        super().__init__(pictograph, attributes, motion)


class BigEightRings(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.BigEightRings
        super().__init__(pictograph, attributes, motion)


class DoubleStar(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Doublestar
        super().__init__(pictograph, attributes, motion)


class BigHoop(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Bighoop
        super().__init__(pictograph, attributes, motion)


class BigDoubleStar(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Bigdoublestar
        super().__init__(pictograph, attributes, motion)


class Quiad(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Quiad
        super().__init__(pictograph, attributes, motion)


class Sword(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Sword
        super().__init__(pictograph, attributes, motion)


class Guitar(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Guitar
        super().__init__(pictograph, attributes, motion)


class Ukulele(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Ukulele
        super().__init__(pictograph, attributes, motion)


class Chicken(Prop):
    def __init__(
        self, pictograph: "BasePictograph", attributes, motion: "Motion"
    ) -> None:
        attributes[PROP_TYPE] = PropType.Chicken
        super().__init__(pictograph, attributes, motion)
