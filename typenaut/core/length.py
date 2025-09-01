from typing import Iterable, Self

from attrs import define

from typenaut.module import CoreModule
from typenaut.utils import StaticClass, universal


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
    _value: float = 0.0

    def typst(self) -> Iterable[str]:
        yield f"{self._value}%"

# ---------------------------------------------------------------------------- #

@define
class FractionLength(Length):
    """Flex length relative to the container and other items"""
    _value: float = 1.0

    def typst(self) -> Iterable[str]:
        yield f"{self._value}fr"

    def __add__(self, other: Self) -> Self:
        return FractionLength(self._value + other._value)

# ---------------------------------------------------------------------------- #

@define
class AbsoluteLength(Length):

    _value: float = 0.0
    """Length value in points"""

    def typst(self) -> Iterable[str]:
        yield f'{self._value}pt'

    # ------------------------------------------ #
    # Points unit, common in typography

    @universal
    def pt(self, value: float) -> Self:
        self._value = value
        return self

    def as_pt(self) -> float:
        return self._value

    # ------------------------------------------ #
    # Centimeters

    @universal
    def cm(self, value: float) -> Self:
        self._value = (value * 28.3465)
        return self

    def as_cm(self) -> float:
        return (self._value / 28.3465)

    # ------------------------------------------ #
    # Milimeters

    @universal
    def mm(self, value: float) -> Self:
        return self.cm(value / 10)

    def as_mm(self) -> float:
        return (self.cm * 10)

    # ------------------------------------------ #
    # Inches

    @universal
    def inch(self, value: float) -> Self:
        return self.cm(value * 2.54)

    def as_inch(self) -> float:
        return (self.cm / 2.54)

    # ------------------------------------------ #
    # Common values

    @universal
    def zero(self) -> Self:
        return self.cm(0.0)

# ---------------------------------------------------------------------------- #

class length(StaticClass):
    auto = AutoLength
    rel  = RelativeLength
    fr   = FractionLength
    pt   = AbsoluteLength.pt
    cm   = AbsoluteLength.cm
    mm   = AbsoluteLength.mm
    inch = AbsoluteLength.inch
    zero = lambda: AbsoluteLength(_value=0)
