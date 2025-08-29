from typing import Iterable, Self

from attrs import define
from typenaut import StaticClass
from typenaut.module import Composite


@define
class Length(Composite):
    ...

# ---------------------------------------------------------------------------- #

@define
class AutoLength(Length):
    def code(self) -> Iterable[str]:
        yield "auto"

# ---------------------------------------------------------------------------- #

@define
class RelativeLength(Length):
    """Percentage relative to the container"""
    value: float = 0.0

    def code(self) -> Iterable[str]:
        yield f"{self.value}%"

# ---------------------------------------------------------------------------- #

@define
class FractionLength(Length):
    """Flex length relative to the container and other items"""
    value: float = 1.0

    def code(self) -> Iterable[str]:
        yield f"{self.value}fr"

    def __add__(self, other: Self) -> Self:
        return FractionLength(self.value + other.value)

# ---------------------------------------------------------------------------- #

@define
class AbsoluteLength(Length):
    value: float = 0.0
    """Length value in centimeters"""

    def code(self) -> Iterable[str]:
        yield f'{self.value}cm'

    # ------------------------------------------ #
    # Centimeters

    @classmethod
    def from_cm(cls, value: float) -> Self:
        self = cls()
        self.cm = value
        return self

    @property
    def cm(self) -> float:
        return self.value

    @cm.setter
    def cm(self, value: float):
        self.value = value

    # ------------------------------------------ #
    # Points unit, common in typography

    @classmethod
    def from_pt(cls, value: float) -> Self:
        self = cls()
        self.pt = value
        return self

    @property
    def pt(self) -> float:
        return (self.value * 28.3465)

    @pt.setter
    def pt(self, value: float):
        self.value = (value / 28.3465)

# ---------------------------------------------------------------------------- #

class length(StaticClass):
    pt   = AbsoluteLength.from_pt
    cm   = AbsoluteLength.from_cm
    auto = AutoLength
