__author__   = ["Tremeschin"]
__credits__  = ["Tim Voßhenrich <https://github.com/T1mVo>"]
__url__      = "https://typst.app/universe/package/shadowed"
__version__  = "0.2.0"
__license__  = "MIT"

from typing import Iterable

from attrs import Factory, define

from typenaut import Container
from typenaut.core.color import Color, color
from typenaut.core.length import Length, length


@define
class Shadowed(Container):

    version: str = "0.2.0"
    """Package version"""

    fill: Color = Factory(color.white)
    """Background color"""

    color: Color = Factory(lambda: color.rgb_u8(89, 85, 101, 76))
    """Shadow color"""

    radius: Length = Factory(lambda: length.pt(4))
    """Corners rounding length"""

    inset: Length = Factory(lambda: length.pt(6))
    """Inner padding of the content"""

    shadow: Length = Factory(lambda: length.pt(8))
    """Blur radius of the shadow, adds padding of the same size"""

    clip: bool = False
    """Truncates overflowing content"""

    dx: Length = Factory(lambda: length.pt(0))
    """Horizontal offset of the shadow"""

    dy: Length = Factory(lambda: length.pt(0))
    """Vertical offset of the shadow"""

    def imports(self) -> Iterable[str]:
        yield f'#import "@preview/shadowed:{self.version}": shadowed'

    def typst(self) -> Iterable[str]:
        yield f"#shadowed("
        yield   f"fill: {self.fill.code()},"
        yield   f"color: {self.color.code()},"
        yield   f"radius: {self.radius.code()},"
        yield   f"inset: {self.inset.code()},"
        yield   f"shadow: {self.shadow.code()},"
        yield   f"clip: {str(self.clip).lower()},"
        yield   f"dx: {self.dx.code()},"
        yield   f"dy: {self.dy.code()},"
        yield ")["
        for child in self.children:
            yield from child.typst()
        yield "]"
