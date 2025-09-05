__author__   = ["Tremeschin"]
__credits__  = ["Chad Skeeters <https://github.com/cskeeters>"]
__url__      = "https://typst.app/universe/package/shadowed"
__version__  = "0.1.0"
__license__  = "MIT"

from typing import Iterable

from attrs import Factory, define

from typenaut import Angle, Color, Length, Module, color, length


@define
class ArcText(Module):
    value: str = "Curvly ArcText"

    width: Length = Factory(lambda: length.cm(5))
    """Horizontal space the text occupies"""

    angle: Angle = Factory(lambda: Angle.degrees(30.0))
    """Circle ratio the text spans"""

    rotate: bool = True
    """Rotate letters along the arc"""

    equidistant: bool = False
    """Separate characters evenly"""

    # Todo: dx, dy within a Block
    # Fixme: Use ephemeral #set text

    def imports(self) -> Iterable[str]:
        yield f'#import "@preview/curvly:{__version__}"'

    def typst(self) -> Iterable[str]:
        yield f"#curvly.text-on-arc("
        yield f'  "{self.value}",'
        yield f"  {self.width.code()},"
        yield f"  {self.angle.code()},"
        yield f"  rotate-letters: {str(self.rotate).lower()},"
        yield f"  equidistant: {str(self.equidistant).lower()},"
        yield f")"


@define
class CircleText(Module):
    top: str = "And Now for Something"
    """Top text displayed on the circle"""

    top_angle: Angle = Factory(lambda: Angle.degrees(130.0))
    """Circle ratio the top text spans"""

    bottom: str = "Completely Different"
    """Bottom text displayed on the circle"""

    bottom_angle: Angle = Factory(lambda: Angle.degrees(130.0))
    """Circle ratio the bottom text spans"""

    width: Length = Factory(lambda: length.cm(3.5))
    """Circle diameter"""

    circle_margin: Length = Factory(length.zero)
    """Circle ring thickness"""

    circle_color: Color = Factory(color.white)
    """Circle ring color"""

    equidistant: bool = False
    """Separate characters evenly"""

    def imports(self) -> Iterable[str]:
        yield f'#import "@preview/curvly:{__version__}"'

    def typst(self) -> Iterable[str]:
        yield f"#curvly.text-on-circle("
        yield f'  "{self.top}",'
        yield f'  "{self.bottom}",'
        yield f"  {self.width.code()},"
        yield f"  {self.top_angle.code()},"
        yield f"  {self.bottom_angle.code()},"
        yield f"  equidistant: {str(self.equidistant).lower()},"
        yield f"  circle-fill: {self.circle_color.code()},"
        yield f"  circle-margin: {self.circle_margin.code()},"
        yield f")"
