from typing import Iterable, Self

from attrs import define
from typenaut import StaticClass
from typenaut.module import Module


@define
class Length(Module):
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

    value: float = 0.0
    """Length value in points"""

    def typst(self) -> Iterable[str]:
        yield f'{self.value}pt'

    # ------------------------------------------ #
    # Points unit, common in typography

    @classmethod
    def from_pt(cls, value: float) -> Self:
        self = cls()
        self.pt = value
        return self

    @property
    def pt(self) -> float:
        return self.value

    @pt.setter
    def pt(self, pt: float):
        self.value = pt

    # ------------------------------------------ #
    # Centimeters

    @classmethod
    def from_cm(cls, value: float) -> Self:
        self = cls()
        self.cm = value
        return self

    @property
    def cm(self) -> float:
        return (self.value / 28.3465)

    @cm.setter
    def cm(self, cm: float):
        self.value = (cm * 28.3465)

    # ------------------------------------------ #
    # Milimeters

    @classmethod
    def from_mm(cls, value: float) -> Self:
        self = cls()
        self.mm = value
        return self

    @property
    def mm(self) -> float:
        return (self.cm * 10)

    @mm.setter
    def mm(self, mm: float):
        self.cm = (mm / 10)

    # ------------------------------------------ #
    # Inches

    @classmethod
    def from_inch(cls, value: float) -> Self:
        self = cls()
        self.inch = value
        return self

    @property
    def inch(self) -> float:
        return (self.cm / 2.54)

    @inch.setter
    def inch(self, inch: float):
        self.cm = (inch * 2.54)

# ---------------------------------------------------------------------------- #

class length(StaticClass):
    auto = AutoLength
    rel  = RelativeLength
    fr   = FractionLength
    pt   = AbsoluteLength.from_pt
    cm   = AbsoluteLength.from_cm
    mm   = AbsoluteLength.from_mm
    inch = AbsoluteLength.from_inch
