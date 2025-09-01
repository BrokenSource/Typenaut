import math
from typing import Iterable, Self

from attrs import define

from typenaut.module import CoreModule
from typenaut.utils import StaticClass, universal

# ---------------------------------------------------------------------------- #

@define
class Angle(CoreModule):

    _value: float = 0.0
    """Angle value in degrees"""

    def typst(self) -> Iterable[str]:
        yield f"{self._value}deg"

    # ------------------------------------------ #
    # Special functions

    def flip(self) -> Self:
        self._value *= -1
        return self

    def normalize(self) -> Self:
        self._value %= 360
        return self

    # ------------------------------------------ #
    # Degrees

    @universal
    def degrees(self, value: float) -> Self:
        self._value = value
        return self

    def as_degrees(self) -> float:
        return self._value

    # ------------------------------------------ #
    # Radians

    @universal
    def radians(self, value: float) -> Self:
        return self.degrees(math.degrees(value))

    def as_radians(self) -> float:
        return math.radians(self._value)

    # ------------------------------------------ #
    # Common values

    @universal
    def zero(self) -> Self:
        return self.degrees(0.0)

    @universal
    def thirty(self) -> Self:
        return self.degrees(30.0)

    @universal
    def diagonal(self) -> Self:
        return self.degrees(45.0)

    @universal
    def sixty(self) -> Self:
        return self.degrees(60.0)

    @universal
    def right(self) -> Self:
        return self.degrees(90.0)

    @universal
    def straight(self) -> Self:
        return self.degrees(180.0)

# ---------------------------------------------------------------------------- #

class angle(StaticClass):
    degrees  = Angle.degrees
    radians  = Angle.radians
    zero     = Angle.zero
    thirty   = Angle.thirty
    diagonal = Angle.diagonal
    sixty    = Angle.sixty
    right    = Angle.right
    straight = Angle.straight
