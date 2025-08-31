__author__ = ["Tremeschin"]

from typing import Iterable

from attrs import Factory, define

from typenaut import Color, Length, Rectangle, color, length
from typenaut.module import Composite


@define
class Card(Composite):

    width: Length = Factory(lambda: length.rel(100))
    """Width of the card"""

    height: Length = Factory(lambda: length.rel(100))
    """Height of the card"""

    radius: Length = Factory(lambda: length.pt(6))
    """Rounding of the card corners"""

    fill: Color = Factory(lambda: color.luma_u8(35))
    """Base color of the card"""

    inset: Length = Factory(lambda: length.pt(6))
    """Inner contents padding"""

    margin = length.pt(1)
    """Size of the margin"""

    # Fixme (dict): Temporary inset until dict support
    def typst(self) -> Iterable[str]:

        # Note: Must be transparent to the document
        base = Rectangle(
            radius=self.radius,
            fill=self.fill,
        )

        with base.copy() as R1:
            R1.inset = f"(top: {self.margin.code()}, rest: 0pt)"
            R1.fill.brightness *= 1.21

            with base.copy(R1) as R2:
                R2.inset = f"(bottom: {self.margin.code()}, rest: 0pt)"
                R2.fill.luma /= 1.21

                with base.copy(R2,
                    width=self.width,
                    height=self.height,
                ) as R3:
                    R3.inset = self.inset
                    R3.children += self.children

                    # Fixme (block)
                    # with Block(R3) as B1:
                    #     ....

        yield from R1.typst()
