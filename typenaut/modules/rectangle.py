from typing import Iterable

from attrs import Factory, define

from typenaut import StaticClass
from typenaut.core.color import Color, color
from typenaut.core.function import Function
from typenaut.core.length import Length, length
from typenaut.core.stroke import Stroke, stroke
from typenaut.module import Composite

# ---------------------------------------------------------------------------- #

@define
class Rectangle(Composite):

    width: Length = Factory(length.auto)
    """Horizontal length of the rectangle"""

    height: Length = Factory(length.auto)
    """Vertical length of the rectangle"""

    fill: Color = Factory(color.none)
    """Fill color of the rectangle"""

    stroke: Stroke = Factory(stroke.default)
    """Stroke color of the rectangle"""

    # Todo: How to handle all borders + sides special mode?
    radius: Length = Factory(lambda: length.pt(6))
    """Corner radius of the rectangle"""

    inset: Length = Factory(length.auto)

    def typst(self) -> Iterable[str]:
        # yield f"#rect("
        # yield f"    width: {self.width.code()},"
        # yield f"    height: {self.height.code()},"
        # yield f"    fill: {self.fill.code()},"
        # yield f"    stroke: {self.stroke.code()},"
        # yield ")["
        # for child in self.children:
        #     yield from child.typst()
        # yield "]"
        yield from Function(
            name="rect",
            kwargs=dict(
                width=self.width,
                height=self.height,
                fill=self.fill,
                stroke=self.stroke,
                radius=self.radius,
                inset=self.inset,
            ),
            body=self.children,
        ).call()

# ---------------------------------------------------------------------------- #

class rectangle(StaticClass):
    ...
