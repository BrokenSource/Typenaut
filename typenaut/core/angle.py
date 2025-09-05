import math
from typing import Iterable, Self, overload

from attrs import define

from typenaut import Null
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

    @overload
    def degrees(cls, new: float) -> Self: ...
    @overload
    def degrees(self) -> float: ...

    @hybridmethod
    def degrees(self, new: float=Null):
        if (new is Null):
            return self._value
        self._value = new
        return self

    # -------------------------------- #
    # Radians

    @overload
    def radians(cls, new: float) -> Self: ...
    @overload
    def radians(self) -> float: ...

    @hybridmethod
    def radians(self, new: float=Null):
        if (new is not Null):
            self._value = math.degrees(new)
            return self
        return math.radians(self._value)

    # -------------------------------- #
    # Common values

    @hybridmethod
    def zero(self):
        return self.degrees(0.0)

    @hybridmethod
    def thirty(self):
        return self.degrees(30.0)

    @hybridmethod
    def diagonal(self):
        return self.degrees(45.0)

    @hybridmethod
    def sixty(self):
        return self.degrees(60.0)

    @hybridmethod
    def right(self):
        return self.degrees(90.0)

    @hybridmethod
    def straight(self):
        return self.degrees(180.0)
