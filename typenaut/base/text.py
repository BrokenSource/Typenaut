from collections.abc import Iterable
from typing import Literal, Union

from attrs import define
from typenaut.base.color import Color
from typenaut.module import FinalModule


# Idea: Auto download fonts?
class Font:
    Libertinus: str = "Libertinus Serif"
    RobotoSlab: str = "Roboto Slab"
    Roboto:     str = "Roboto"
    Nunito:     str = "Nunito"


@define
class Text(FinalModule):
    value: str = ""

    # color: Color = Color.white()

    weight: Union[Literal["regular", "bold"], int] = "regular"
    """Whether to make the text thicker"""

    font: str = Font.Libertinus

    def code(self) -> Iterable[str]:
        yield '#text('
        yield f'    font: "{self.font}",'
        yield f'    weight: "{self.weight}",'
        yield f')[{self.value}]'
