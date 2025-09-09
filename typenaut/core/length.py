from typing import Iterable, Self

from attrs import define

from typenaut.module import CoreModule
from typenaut.utils import StaticClass, hybridmethod


@define
class Length(CoreModule):
    ...

# ---------------------------------------------------------------------------- #

@define
class AutoLength(Length):
    def typst(self) -> Iterable[str]:
        yield "auto"

# ---------------------------------------------------------------------------- #

@define
class RelativeLength(Length):
    """Percentage relative to the container"""
    value: float = 0.0

    def typst(self) -> Iterable[str]:
        yield f"{self.value}%"

# ---------------------------------------------------------------------------- #

@define
class FractionLength(Length):
    """Flex length relative to the container and other items"""
    value: float = 1.0

    def typst(self) -> Iterable[str]:
        yield f"{self.value}fr"

    def __add__(self, other: Self) -> Self:
        return FractionLength(self.value + other.value)

# ---------------------------------------------------------------------------- #

@define
class AbsoluteLength(Length):

    _value: float = 0.0
    """Length value in points"""

    def typst(self) -> Iterable[str]:
        yield f"{self._value}pt"

    # -------------------------------- #
    # Points unit, common in typography

    @hybridmethod
    def set_pt(self, value: float) -> Self:
        self._value = value
        return self

    def get_pt(self) -> float:
        return self._value

    pt = property(get_pt, set_pt)

    # -------------------------------- #
    # Centimeters

    @hybridmethod
    def set_cm(self, value: float) -> Self:
        self._value = (value * 28.3465)
        return self

    def get_cm(self) -> float:
        return (self._value / 28.3465)

    cm = property(get_cm, set_cm)

    # -------------------------------- #
    # Milimeters

    @hybridmethod
    def set_mm(self, value: float) -> Self:
        return self.set_cm(value / 10.0)

    def get_mm(self) -> float:
        return (self.cm * 10.0)

    mm = property(get_mm, set_mm)

    # -------------------------------- #
    # Inches

    @hybridmethod
    def set_inch(self, value: float) -> Self:
        return self.set_cm(value * 2.54)

    def get_inch(self) -> float:
        return (self._value / 2.54)

    inch = property(get_inch, set_inch)

    # -------------------------------- #
    # Special

    @hybridmethod
    def zero(self) -> Self:
        return self.set_pt(0.0)

# ---------------------------------------------------------------------------- #

class length(StaticClass):
    auto = AutoLength
    rel  = RelativeLength
    fr   = FractionLength
    pt   = AbsoluteLength.set_pt
    cm   = AbsoluteLength.set_cm
    mm   = AbsoluteLength.set_mm
    inch = AbsoluteLength.set_inch
    zero = AbsoluteLength.zero
