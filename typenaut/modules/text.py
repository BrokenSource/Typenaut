from collections.abc import Iterable
from enum import Enum
from typing import Literal, Union

from attrs import Factory, define
from typenaut import StaticClass, denum
from typenaut.core.color import Color, color
from typenaut.module import Composite


class Font(Enum):
    Libertinus: str = "Libertinus Serif"
    RobotoSlab: str = "Roboto Slab"
    Roboto:     str = "Roboto"
    Nunito:     str = "Nunito"

    def download(self) -> None:
        raise NotImplementedError


@define
class Text(Composite):
    value: str = ""

    color: Color = Factory(color.black)

    weight: Union[Literal["regular", "bold"], int] = "regular"

    font: str = Font.Libertinus

    def code(self) -> Iterable[str]:
        yield '#text('
        yield f'    font: "{denum(self.font)}",'
        yield f'    fill: {self.color.ucode()},'
        yield f'    weight: "{self.weight}",'
        yield f')[{self.value}]'


class text(StaticClass):
    ...
