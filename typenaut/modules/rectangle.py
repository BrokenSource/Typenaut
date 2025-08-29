from typing import Iterable

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

    def typst(self) -> Iterable[str]:
        yield f"#rect("
        yield f"    width: {self.width.code()},"
        yield f"    height: {self.height.code()},"
        yield f"    fill: {self.color.code()},"
        yield f"    stroke: {self.stroke.code()},"
        yield ")["
        for child in self.children:
            yield from child.typst()
        yield "]"

# ---------------------------------------------------------------------------- #

class rectangle(StaticClass):
    ...
