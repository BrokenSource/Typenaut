import math
from typing import Iterable, Self

from attrs import define
from typenaut import StaticClass
from typenaut.module import Module

# ---------------------------------------------------------------------------- #

@define
class Angle(Module):
    degrees: float = 0.0

    def code(self) -> Iterable[str]:
        yield f"{self.degrees}deg"

    @classmethod
    def from_degrees(cls, value: float) -> Self:
        return cls(degrees=value)

    # ------------------------------------------ #
    # Special functions

    def flip(self) -> Self:
        self.degrees *= -1
        return self

    def normalize(self) -> Self:
        self.degrees %= 360
        return self

    # ------------------------------------------ #
    # Radians

    @classmethod
    def from_radians(cls, value: float) -> Self:
        self = cls()
        self.radians = value
        return self

    @property
    def radians(self) -> float:
        return math.radians(self.degrees)

    @radians.setter
    def radians(self, value: float):
        self.degrees = math.degrees(value)

# ---------------------------------------------------------------------------- #

class angle(StaticClass):
    degrees = Angle.from_degrees
    radians = Angle.from_radians

    @staticmethod
    def zero() -> Angle:
        return Angle(degrees=0.0)

    @staticmethod
    def diagonal() -> Angle:
        return Angle(degrees=45.0)

    @staticmethod
    def right() -> Angle:
        return Angle(degrees=90.0)

    @staticmethod
    def straight() -> Angle:
        return Angle(degrees=180.0)
