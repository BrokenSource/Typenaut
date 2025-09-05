from typing import Iterable, Optional

from attrs import Factory, define

from typenaut.core.color import Color
from typenaut.core.function import Function
from typenaut.core.length import Length, length
from typenaut.core.stroke import Stroke
from typenaut.module import Composite
from typenaut.utils import StaticClass

# ---------------------------------------------------------------------------- #

@define
class Rectangle(Composite):

    width: Optional[Length] = Factory(length.auto)
    """Horizontal length of the rectangle"""

    height: Optional[Length] = Factory(length.auto)
    """Vertical length of the rectangle"""

    fill: Optional[Color] = None
    """Fill color of the rectangle"""

    stroke: Optional[Stroke] = None
    """Stroke color of the rectangle"""

    # Todo: How to handle all borders + sides special mode?
    radius: Optional[Length] = None
    """Corner radius of the rectangle"""

    inset: Optional[Length] = None
    """Inner padding of the content"""

    def typst(self) -> Iterable[str]:
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
