import math
from typing import Iterable, Self

from attrs import define

from typenaut import StaticClass
from typenaut.module import CoreModule

# ---------------------------------------------------------------------------- #

@define
class Angle(CoreModule):

    value: float = 0.0
    """Angle value in degrees"""

    def typst(self) -> Iterable[str]:
        yield f"{self.value}deg"

    # ------------------------------------------ #
    # Special functions

    def flip(self) -> Self:
        self.value *= -1
        return self

    def normalize(self) -> Self:
        self.value %= 360
        return self

    # ------------------------------------------ #
    # Degrees

    @classmethod
    def from_degrees(cls, value: float) -> Self:
        self = cls()
        self.value = value
        return self

    @property
    def degrees(self) -> float:
        return self.value

    @degrees.setter
    def degrees(self, degrees: float):
        self.value = degrees

    # ------------------------------------------ #
    # Radians

    @classmethod
    def from_radians(cls, value: float) -> Self:
        self = cls()
        self.radians = value
        return self

    @property
    def radians(self) -> float:
        return math.radians(self.value)

    @radians.setter
    def radians(self, radians: float):
        self.value = math.degrees(radians)

# ---------------------------------------------------------------------------- #

class angle(StaticClass):
    degrees  = Angle.from_degrees
    radians  = Angle.from_radians
    zero     = lambda: Angle(value=0.0)
    thirty   = lambda: Angle(value=30.0)
    diagonal = lambda: Angle(value=45.0)
    sixty    = lambda: Angle(value=60.0)
    right    = lambda: Angle(value=90.0)
    straight = lambda: Angle(value=180.0)
