import math
from typing import Iterable, Self

from attrs import define

from typenaut import StaticClass
from typenaut.module import Module

# ---------------------------------------------------------------------------- #

@define
class Angle(Module):

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
    degrees = Angle.from_degrees
    radians = Angle.from_radians

    @staticmethod
    def zero() -> Angle:
        return Angle(value=0.0)

    @staticmethod
    def diagonal() -> Angle:
        return Angle(value=45.0)

    @staticmethod
    def right() -> Angle:
        return Angle(value=90.0)

    @staticmethod
    def straight() -> Angle:
        return Angle(value=180.0)
