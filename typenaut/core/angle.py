import math
from typing import Iterable, Self

from attrs import define

from typenaut.module import CoreModule
from typenaut.utils import StaticClass, hybridmethod

# ---------------------------------------------------------------------------- #

@define
class Angle(CoreModule):

    _value: float = 0.0
    """Angle value in degrees"""

    def typst(self) -> Iterable[str]:
        yield f"{self._value}deg"

    # -------------------------------- #
    # Special functions

    def flip(self) -> Self:
        self._value *= -1
        return self

    def normalize(self) -> Self:
        self._value %= 360
        return self

    # -------------------------------- #
    # Degrees

    @hybridmethod
    def set_degrees(self, value: float) -> Self:
        self._value = value
        return self

    def get_degrees(self) -> float:
        return self._value

    degrees = property(get_degrees, set_degrees)

    # -------------------------------- #
    # Radians

    @hybridmethod
    def set_radians(self, value: float) -> Self:
        self._value = math.degrees(value)
        return self

    def get_radians(self) -> float:
        return math.radians(self._value)

    radians = property(get_radians, set_radians)

    # -------------------------------- #
    # Common values

    @hybridmethod
    def zero(self):
        return self.set_degrees(0.0)

    @hybridmethod
    def thirty(self):
        return self.set_degrees(30.0)

    @hybridmethod
    def diagonal(self):
        return self.set_degrees(45.0)

    @hybridmethod
    def sixty(self):
        return self.set_degrees(60.0)

    @hybridmethod
    def right(self):
        return self.set_degrees(90.0)

    @hybridmethod
    def straight(self):
        return self.set_degrees(180.0)

# ---------------------------------------------------------------------------- #

class angle(StaticClass):
    degrees  = Angle.set_degrees
    radians  = Angle.set_radians
    zero     = Angle.zero
    thirty   = Angle.thirty
    diagonal = Angle.diagonal
    sixty    = Angle.sixty
    right    = Angle.right
    straight = Angle.straight
