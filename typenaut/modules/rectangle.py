import math
from typing import Iterable, Self

from attrs import Factory, define
from typenaut import StaticClass
from typenaut.core.color import Color, color
from typenaut.core.length import Length, length
from typenaut.core.stroke import Stroke, stroke
from typenaut.module import Container

# ---------------------------------------------------------------------------- #

@define
class Rectangle(Container):
    width: Length = Factory(length.auto)
    """Horizontal length of the rectangle"""

    height: Length = Factory(length.auto)
    """Vertical length of the rectangle"""

    color: Color = Factory(color.transparent)
    """Fill color of the rectangle"""

    stroke: Stroke = Factory(stroke.default)
    """Stroke color of the rectangle"""

    def code(self) -> Iterable[str]:
        yield f"#rect("
        yield f"    width: {self.width.ucode()},"
        yield f"    height: {self.height.ucode()},"
        yield f"    fill: {self.color.ucode()},"
        yield f"    stroke: {self.stroke.ucode()},"
        yield ")["
        for child in self.children:
            yield from child.code()
        yield "]"

# ---------------------------------------------------------------------------- #

class rectangle(StaticClass):
    ...
