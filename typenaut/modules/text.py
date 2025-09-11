from collections.abc import Iterable
from enum import Enum
from functools import partial
from typing import Literal, Self, Union

from attrs import Factory, define

from typenaut.core import Color, Function, color
from typenaut.module import Module
from typenaut.utils import StaticClass


class Font(Enum):
    Libertinus: str = '"Libertinus Serif"'
    RobotoSlab: str = '"Roboto Slab"'
    Roboto:     str = '"Roboto"'
    Nunito:     str = '"Nunito"'

    def download(self) -> None:
        raise NotImplementedError


@define
class Text(Module):

    value: str = ""

    font: str = Font.Libertinus

    color: Color = Factory(color.black)

    weight: Union[Literal["regular", "bold"], int] = 'regular'

    def bold(self) -> Self:
        self.weight = 'bold'
        return self

    def typst(self) -> Iterable[str]:
        yield from Function(
            name="text",
            kwargs=dict(
                font=self.font,
                fill=self.color,
                weight=f'"{self.weight}"',
            ),
            body=[self.value],
        ).call()


class text(StaticClass):
    libertinus = partial(Text, font=Font.Libertinus)
