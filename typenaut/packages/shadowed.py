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
    fill:   Color  = Factory(color.white)
    color:  Color  = Factory(lambda: color.rgb_u8(89, 85, 101, 76))
    radius: Length = Factory(lambda: length.pt(4))
    inset:  Length = Factory(lambda: length.pt(6))
    shadow: Length = Factory(lambda: length.pt(8))
    clip:   bool   = False

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
        yield ")["
        for child in self.children:
            yield from child.typst()
        yield "]"
